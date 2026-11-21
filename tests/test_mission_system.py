import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from flask import Flask

from game_app.database import close_db, get_db, init_db
from game_app import create_app
from game_app.extensions import socketio
from game_app.mission_system import (
    DIFFICULTIES,
    InventoryCapacityError,
    can_access_mission,
    complete_mission,
    credit_gold_monster_drop,
    difficulty_state,
    format_gold,
    gold_for_monster,
    phase_gold_bonus,
    resolve_staging_inventory,
    roll_chest_rarities,
    sell_inventory_item,
)


class FixedRng:
    def random(self):
        return 1.0

    def choices(self, population, weights=None, k=1):
        return [population[0]] * k


class RecordingRng:
    def __init__(self, value=1.0, choice_index=0):
        self.value = value
        self.choice_index = choice_index
        self.weights = []

    def random(self):
        return self.value

    def choices(self, population, weights=None, k=1):
        self.weights.append(tuple(weights))
        return [population[self.choice_index]] * k


class MissionSystemTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.app = Flask(__name__)
        self.app.config["DATABASE"] = str(
            Path(self.temporary_directory.name) / "missions.sqlite3"
        )
        self.app.teardown_appcontext(close_db)
        init_db(self.app)
        with self.app.app_context():
            db = get_db()
            db.execute(
                """INSERT INTO users (username, password_hash, created_at)
                   VALUES ('mission-test', 'unused', 'test')"""
            )
            self.user_id = db.execute(
                "SELECT id FROM users WHERE username = 'mission-test'"
            ).fetchone()["id"]
            db.execute(
                """INSERT INTO characters
                   (user_id, name, name_key, class_id, created_at)
                   VALUES (?, 'Tester', 'mission-tester', 'guardian', 'test')""",
                (self.user_id,),
            )
            self.character_id = db.execute(
                "SELECT id FROM characters WHERE name_key = 'mission-tester'"
            ).fetchone()["id"]
            db.commit()

    def tearDown(self):
        self.temporary_directory.cleanup()

    def test_gold_formatter_uses_whole_units_with_portuguese_grouping(self):
        self.assertEqual(format_gold(0), "0")
        self.assertEqual(format_gold(12), "12")
        self.assertEqual(format_gold(1234567), "1.234.567")

    def test_gold_rewards_and_boss_chest_profiles_cover_every_difficulty(self):
        expected = (
            ("risk_low", 12, 100, 150, 0.15, (75, 20, 4, 1)),
            ("risk_moderate", 17, 200, 300, 0.35, (58, 28, 12, 2)),
            ("risk_high", 27, 350, 500, 0.60, (34, 36, 25, 5)),
            ("risk_extreme", 37, 500, 800, 0.85, (12, 23, 40, 25)),
        )
        for difficulty, monster_gold, phase_bonus, boss_bonus, third_chest, weights in expected:
            with self.subTest(difficulty=difficulty):
                self.assertEqual(gold_for_monster(difficulty, 71), monster_gold)
                self.assertEqual(
                    phase_gold_bonus(difficulty, boss_phase=False),
                    phase_bonus,
                )
                self.assertEqual(
                    phase_gold_bonus(difficulty, boss_phase=True),
                    phase_bonus + boss_bonus,
                )

                before_threshold = RecordingRng(third_chest / 2)
                boss_loot = roll_chest_rarities(
                    difficulty, 10, rng=before_threshold
                )
                self.assertEqual(len(boss_loot), 3)
                self.assertEqual(before_threshold.weights, [weights] * 3)

                at_threshold = RecordingRng(third_chest)
                boss_loot = roll_chest_rarities(
                    difficulty, 10, rng=at_threshold
                )
                self.assertEqual(len(boss_loot), 2)
                self.assertEqual(at_threshold.weights, [weights] * 2)

    def test_common_and_miniboss_rarity_chances_apply_in_all_difficulties(self):
        for difficulty in DIFFICULTIES:
            with self.subTest(difficulty=difficulty):
                self.assertEqual(
                    roll_chest_rarities(
                        difficulty, 1, rng=RecordingRng(0.14)
                    ),
                    ["rare"],
                )
                self.assertEqual(
                    roll_chest_rarities(
                        difficulty, 1, rng=RecordingRng(0.15)
                    ),
                    ["common"],
                )
                self.assertEqual(
                    roll_chest_rarities(
                        difficulty, 5, rng=RecordingRng(0.29)
                    ),
                    ["rare"],
                )
                self.assertEqual(
                    roll_chest_rarities(
                        difficulty, 5, rng=RecordingRng(0.30)
                    ),
                    ["common"],
                )

    def _create_run(self, difficulty="risk_low", phase=1):
        with self.app.app_context():
            db = get_db()
            cursor = db.execute(
                """INSERT INTO mission_runs
                   (user_id, character_id, difficulty, phase, start_time, created_at)
                   VALUES (?, ?, ?, ?, 100, 'test')""",
                (self.user_id, self.character_id, difficulty, phase),
            )
            db.commit()
            return cursor.lastrowid

    def test_difficulty_and_phase_unlocks_are_cascading(self):
        with self.app.app_context():
            db = get_db()
            self.assertTrue(can_access_mission(db, self.user_id, "risk_low", 1))
            self.assertFalse(can_access_mission(db, self.user_id, "risk_low", 2))
            self.assertFalse(can_access_mission(db, self.user_id, "risk_moderate", 1))
            db.executemany(
                """INSERT INTO mission_progress
                   (user_id, difficulty, phase, completed_at)
                   VALUES (?, 'risk_low', ?, 'test')""",
                [(self.user_id, phase) for phase in range(1, 31)],
            )
            self.assertTrue(can_access_mission(
                db, self.user_id, "risk_moderate", 1
            ))
            self.assertFalse(can_access_mission(
                db, self.user_id, "risk_moderate", 2
            ))
            db.execute(
                """INSERT INTO mission_progress
                   (user_id, difficulty, phase, completed_at)
                   VALUES (?, 'risk_moderate', 1, 'test')""",
                (self.user_id,),
            )
            states = difficulty_state(db, self.user_id)
            self.assertEqual(states[1]["available_phases"], [1, 2])

    def test_monster_gold_is_credited_once_and_completion_creates_staging(self):
        run_id = self._create_run("risk_low")
        with self.app.app_context():
            db = get_db()
            first = credit_gold_monster_drop(
                db, self.user_id, self.character_id, 71, 1
            )
            duplicate = credit_gold_monster_drop(
                db, self.user_id, self.character_id, 71, 1
            )
            summary = complete_mission(
                db, self.user_id, self.character_id, 1, now=145, rng=FixedRng()
            )
            db.commit()
            wallet = db.execute(
                "SELECT wallet_gold FROM users WHERE id = ?", (self.user_id,)
            ).fetchone()[0]
            staged = db.execute(
                """SELECT rarity, status FROM staging_inventory
                   WHERE mission_run_id = ?""",
                (run_id,),
            ).fetchone()
        self.assertEqual((first, duplicate), (5, 0))
        self.assertEqual(summary["elapsed_seconds"], 45)
        self.assertEqual(summary["total_gold"], 105)
        self.assertEqual(wallet, 105)
        self.assertEqual(tuple(staged), ("common", "pending"))

    def test_staging_transfer_enforces_capacity_and_selling_frees_a_slot(self):
        run_id = self._create_run()
        with self.app.app_context():
            db = get_db()
            db.execute(
                """UPDATE mission_runs SET status = 'completed' WHERE id = ?""",
                (run_id,),
            )
            db.executemany(
                """INSERT INTO inventory_items
                   (user_id, item_name, rarity, salvage_value_gold, created_at)
                   VALUES (?, ?, 'common', 25, 'test')""",
                [(self.user_id, f"Item {index}") for index in range(30)],
            )
            db.executemany(
                """INSERT INTO staging_inventory
                   (mission_run_id, user_id, chest_index, item_name, rarity,
                    salvage_value_gold, created_at)
                   VALUES (?, ?, ?, ?, 'rare', 75, 'test')""",
                [
                    (run_id, self.user_id, 1, "Baú raro 1"),
                    (run_id, self.user_id, 2, "Baú raro 2"),
                ],
            )
            item_id = db.execute(
                "SELECT id FROM inventory_items WHERE user_id = ? ORDER BY id LIMIT 1",
                (self.user_id,),
            ).fetchone()["id"]
            with self.assertRaises(InventoryCapacityError):
                resolve_staging_inventory(db, self.user_id, run_id, {1})
            sold = sell_inventory_item(db, self.user_id, item_id)
            result = resolve_staging_inventory(db, self.user_id, run_id, {1})
            count = db.execute(
                "SELECT COUNT(*) FROM inventory_items WHERE user_id = ?",
                (self.user_id,),
            ).fetchone()[0]
            statuses = db.execute(
                """SELECT status FROM staging_inventory
                   WHERE mission_run_id = ? ORDER BY chest_index""",
                (run_id,),
            ).fetchall()
            db.commit()
        self.assertEqual(sold, 25)
        self.assertEqual(result["inventory_count"], 30)
        self.assertEqual(count, 30)
        self.assertEqual([row["status"] for row in statuses], ["claimed", "discarded"])


class MissionRouteTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.environment = patch.dict(
            "os.environ",
            {
                "CRONICAS_DATABASE": str(
                    Path(self.temporary_directory.name) / "routes.sqlite3"
                ),
                "CRONICAS_SECRET_KEY": "mission-test-key",
            },
        )
        self.environment.start()
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()
        with self.app.app_context():
            db = get_db()
            db.execute(
                """INSERT INTO users (username, password_hash, created_at)
                   VALUES ('mission-route-test', 'unused', 'test')"""
            )
            self.user_id = db.execute(
                "SELECT id FROM users WHERE username = 'mission-route-test'"
            ).fetchone()["id"]
            db.execute(
                """INSERT INTO characters
                   (user_id, name, name_key, class_id, created_at)
                   VALUES (?, 'Route Tester', 'mission-route-tester', 'guardian', 'test')""",
                (self.user_id,),
            )
            self.character_id = db.execute(
                "SELECT id FROM characters WHERE name_key = 'mission-route-tester'"
            ).fetchone()["id"]
            db.commit()
        with self.client.session_transaction() as browser_session:
            browser_session["user_id"] = self.user_id
            browser_session["selected_character_id"] = self.character_id
            browser_session["csrf_token"] = "mission-route-csrf"

    def tearDown(self):
        self.client = None
        self.environment.stop()
        self.temporary_directory.cleanup()

    def _create_character(self, name, name_key):
        with self.app.app_context():
            db = get_db()
            db.execute(
                """INSERT INTO characters
                   (user_id, name, name_key, class_id, created_at)
                   VALUES (?, ?, ?, 'guardian', 'test')""",
                (self.user_id, name, name_key),
            )
            character_id = db.execute(
                "SELECT id FROM characters WHERE name_key = ?", (name_key,)
            ).fetchone()["id"]
            db.commit()
        return character_id

    def test_lobby_renders_balance_profile_for_all_four_difficulties(self):
        response = self.client.get("/sala-de-espera")
        self.assertEqual(response.status_code, 200)

        profiles = (
            ("Risco Baixo", "1,00", "1,00", 0, 5, 100, 150, 15, "75/20/4/1"),
            ("Risco Moderado", "1,20", "1,25", 1, 10, 200, 300, 35, "58/28/12/2"),
            ("Risco Alto", "1,75", "1,80", 0, 20, 350, 500, 60, "34/36/25/5"),
            ("Risco Extremo", "2,40", "2,50", 0, 30, 500, 800, 85, "12/23/40/25"),
        )
        for label, health, damage, extra, per_kill, phase, boss, third, weights in profiles:
            with self.subTest(difficulty=label):
                for text in (
                    label,
                    f"×{health} · <strong>Dano:</strong> ×{damage}",
                    f"+{extra} por onda comum.",
                    f"{per_kill} base por abate",
                    f"+{phase} por fase e +{boss} extras em fase com chefe.",
                    f"{third}% de chance de terceiro baú. Pesos C/R/E/L: {weights}%.",
                ):
                    self.assertIn(text.encode("utf-8"), response.data)
        self.assertIn(
            b"Raro em fase comum 15%, semichefe 30%",
            response.data,
        )
        self.assertIn(b"candidatos de balanceamento, n\xc3\xa3o regras finais", response.data)

    def test_server_rejects_locked_mission_and_starts_allowed_mission_with_countdown(self):
        lobby = self.client.get("/sala-de-espera")
        self.assertEqual(lobby.status_code, 200)
        self.assertIn(b"Risco Baixo", lobby.data)
        self.assertNotIn(b"Ouro da conta", lobby.data)
        self.assertNotIn(b"Invent\xc3\xa1rio: 0 / 30", lobby.data)
        for label in (
            "Ato 1 — Fases 1 a 10",
            "Ato 2 — Fases 11 a 20",
            "Ato 3 — Fases 21 a 30",
        ):
            self.assertIn(label.encode("utf-8"), lobby.data)
        self.assertNotIn(b"R$", lobby.data)

        inventory = self.client.get("/inventario")
        self.assertEqual(inventory.status_code, 200)
        self.assertIn(b"Ouro da conta", inventory.data)
        self.assertIn(b"Invent\xc3\xa1rio: 0 / 30", inventory.data)

        rejected = self.client.post(
            "/sala-de-espera/iniciar",
            data={
                "csrf_token": "mission-route-csrf",
                "difficulty": "risk_high",
                "phase": "1",
            },
        )
        self.assertEqual(rejected.status_code, 302)
        with self.app.app_context():
            db = get_db()
            self.assertEqual(
                db.execute("SELECT COUNT(*) FROM mission_runs").fetchone()[0],
                0,
            )

        started = self.client.post(
            "/sala-de-espera/iniciar",
            data={
                "csrf_token": "mission-route-csrf",
                "difficulty": "risk_low",
                "phase": "1",
            },
        )
        self.assertEqual(started.status_code, 302)
        game_page = self.client.get("/jogo")
        self.assertEqual(game_page.status_code, 200)
        with self.app.app_context():
            db = get_db()
            run = db.execute(
                "SELECT * FROM mission_runs WHERE character_id = ?",
                (self.character_id,),
            ).fetchone()
            enemy = db.execute(
                "SELECT id, hp FROM wave_enemies WHERE character_id = ? AND alive = 1",
                (self.character_id,),
            ).fetchone()
            saved_character = db.execute(
                """SELECT phase_preparation_until, current_difficulty, current_phase
                   FROM characters WHERE id = ?""",
                (self.character_id,),
            ).fetchone()
        self.assertEqual((run["difficulty"], run["phase"]), ("risk_low", 1))
        self.assertEqual(saved_character["current_difficulty"], "risk_low")
        self.assertGreaterEqual(saved_character["phase_preparation_until"], time.time() + 4)

        socket_client = socketio.test_client(
            self.app, flask_test_client=self.client
        )
        try:
            attack = socket_client.emit(
                "combat:attack",
                {
                    "enemy_id": enemy["id"],
                    "skill_id": "basic",
                    "csrf_token": "mission-route-csrf",
                },
                callback=True,
            )
        finally:
            socket_client.disconnect()
        self.assertFalse(attack["ok"])
        self.assertIn("preparação", attack["error"])
        with self.app.app_context():
            health = get_db().execute(
                "SELECT hp FROM wave_enemies WHERE id = ?", (enemy["id"],)
            ).fetchone()["hp"]
        self.assertEqual(health, enemy["hp"])

    def test_account_cannot_start_a_second_active_mission_on_another_character(self):
        second_character_id = self._create_character(
            "Second Tester", "mission-route-second"
        )
        started = self.client.post(
            "/sala-de-espera/iniciar",
            data={
                "csrf_token": "mission-route-csrf",
                "difficulty": "risk_low",
                "phase": "1",
            },
        )
        self.assertEqual(started.status_code, 302)

        with self.client.session_transaction() as browser_session:
            browser_session["selected_character_id"] = second_character_id
        blocked = self.client.post(
            "/sala-de-espera/iniciar",
            data={
                "csrf_token": "mission-route-csrf",
                "difficulty": "risk_low",
                "phase": "1",
            },
            follow_redirects=True,
        )
        self.assertEqual(blocked.status_code, 200)
        self.assertIn(b"J\xc3\xa1 existe uma miss\xc3\xa3o ativa nesta conta", blocked.data)

        with self.app.app_context():
            runs = get_db().execute(
                """SELECT character_id, status FROM mission_runs
                   WHERE user_id = ? AND status = 'active'""",
                (self.user_id,),
            ).fetchall()
        self.assertEqual(len(runs), 1)
        self.assertEqual(runs[0]["character_id"], self.character_id)

    def test_pending_loot_pauses_an_active_mission_on_another_character(self):
        active_character_id = self._create_character(
            "Active Tester", "mission-route-active"
        )
        with self.app.app_context():
            db = get_db()
            completed = db.execute(
                """INSERT INTO mission_runs
                   (user_id, character_id, difficulty, phase, start_time,
                    status, created_at)
                   VALUES (?, ?, 'risk_low', 1, 100, 'completed', 'test')""",
                (self.user_id, self.character_id),
            )
            active = db.execute(
                """INSERT INTO mission_runs
                   (user_id, character_id, difficulty, phase, start_time,
                    status, created_at)
                   VALUES (?, ?, 'risk_low', 1, 100, 'active', 'test')""",
                (self.user_id, active_character_id),
            )
            db.execute(
                """INSERT INTO staging_inventory
                   (mission_run_id, user_id, chest_index, item_name, rarity,
                    salvage_value_gold, status, created_at)
                   VALUES (?, ?, 1, 'Baú comum', 'common', 5, 'pending', 'test')""",
                (completed.lastrowid, self.user_id),
            )
            db.commit()
            active_run_id = active.lastrowid

        with self.client.session_transaction() as browser_session:
            browser_session["selected_character_id"] = active_character_id
        game_page = self.client.get("/jogo")
        self.assertEqual(game_page.status_code, 302)
        self.assertIn("/jogo/pos-fase", game_page.headers["Location"])
        self.assertIn(f"run_id={completed.lastrowid}", game_page.headers["Location"])

        self.app.config["TESTING"] = False
        socket_client = socketio.test_client(
            self.app, flask_test_client=self.client
        )
        try:
            result = socket_client.emit(
                "combat:attack",
                {"enemy_id": 1, "csrf_token": "mission-route-csrf"},
                callback=True,
            )
        finally:
            socket_client.disconnect()
            self.app.config["TESTING"] = True
        self.assertFalse(result["ok"])
        self.assertEqual(result["error"], "Nenhuma missão ativa.")

        with self.app.app_context():
            active_status = get_db().execute(
                "SELECT status FROM mission_runs WHERE id = ?", (active_run_id,)
            ).fetchone()["status"]
        self.assertEqual(active_status, "active")

    def test_final_wave_kill_completes_mission_and_records_rewards(self):
        started = self.client.post(
            "/sala-de-espera/iniciar",
            data={
                "csrf_token": "mission-route-csrf",
                "difficulty": "risk_low",
                "phase": "1",
            },
        )
        self.assertEqual(started.status_code, 302)
        with self.app.app_context():
            db = get_db()
            db.execute(
                """UPDATE characters SET current_wave = 10,
                   phase_preparation_until = 0, pending_card_choices = 0
                   WHERE id = ?""",
                (self.character_id,),
            )
            db.execute(
                """UPDATE mission_runs SET start_time = ? WHERE character_id = ?""",
                (time.time() - 60, self.character_id),
            )
            db.execute(
                "DELETE FROM wave_enemies WHERE character_id = ?",
                (self.character_id,),
            )
            db.execute(
                """INSERT INTO wave_enemies
                   (character_id, phase, wave, enemy_index, world_x, world_y,
                    hp, max_hp, experience_reward)
                   VALUES (?, 1, 10, 0, 1201, 900, 1, 1, 1)""",
                (self.character_id,),
            )
            enemy_id = db.execute(
                "SELECT id FROM wave_enemies WHERE character_id = ?",
                (self.character_id,),
            ).fetchone()["id"]
            db.commit()
        socket_client = socketio.test_client(
            self.app, flask_test_client=self.client
        )
        try:
            result = socket_client.emit(
                "combat:attack",
                {
                    "enemy_id": enemy_id,
                    "enemy_x": 1201,
                    "enemy_y": 900,
                    "player_x": 1200,
                    "player_y": 900,
                    "csrf_token": "mission-route-csrf",
                },
                callback=True,
            )
        finally:
            socket_client.disconnect()
        self.assertTrue(result["ok"])
        self.assertTrue(result["mission_complete"])
        with self.app.app_context():
            db = get_db()
            run = db.execute(
                "SELECT status, chest_count FROM mission_runs WHERE character_id = ?",
                (self.character_id,),
            ).fetchone()
            progress = db.execute(
                """SELECT 1 FROM mission_progress
                   WHERE user_id = ? AND difficulty = 'risk_low' AND phase = 1""",
                (self.user_id,),
            ).fetchone()
            loot_count = db.execute(
                "SELECT COUNT(*) FROM staging_inventory WHERE user_id = ?",
                (self.user_id,),
            ).fetchone()[0]
            wallet = db.execute(
                "SELECT wallet_gold FROM users WHERE id = ?", (self.user_id,)
            ).fetchone()[0]
        self.assertEqual(run["status"], "completed")
        self.assertEqual(run["chest_count"], 1)
        self.assertIsNotNone(progress)
        self.assertEqual(loot_count, 1)
        self.assertGreater(wallet, 0)
        result_page = self.client.get("/jogo/pos-fase")
        self.assertEqual(result_page.status_code, 200)
        self.assertIn(b'id="mission-completion-dialog"', result_page.data)
        self.assertIn(b"Continuar para os esp\xc3\xb3lios", result_page.data)
        self.assertIn(b"SALDO DE OURO DA CONTA", result_page.data)
        self.assertIn(b"Ouro", result_page.data)
        self.assertNotIn(b"R$", result_page.data)
        self.assertIn(b"Sala de Espera bloqueada", result_page.data)
        lobby_redirect = self.client.get("/sala-de-espera")
        self.assertEqual(lobby_redirect.status_code, 302)
        self.assertIn("/jogo/pos-fase", lobby_redirect.headers["Location"])


if __name__ == "__main__":
    unittest.main()
