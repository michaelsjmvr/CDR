import json
import os
import tempfile
import time
import unittest
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import patch

from game_app import create_app
import game_app.socket_events as socket_events_module
from game_app.abilities import (
    CLASS_BASE_SKILLS,
    SKILLS,
    SPECIALIZATION_ABILITIES,
    SPECIALIZATION_EPIC_ABILITIES,
    active_class_skill,
    available_class_skills,
    epic_unlock_talent_id,
    keystone_talent_id,
    normalized_skill_slots,
    skill_upgrade_talent_id,
)
from game_app.cards import CARDS
from game_app.combat import (
    CRITICAL_DAMAGE_MULTIPLIER,
    boss_affinity,
    calculate_attack_damage,
    combat_summary,
    derived_combat_stats,
)
from game_app.classes import CLASSES
from game_app.database import get_db
from game_app.extensions import socketio
from game_app.progression import (
    CLASS_AUTO_DISTRIBUTION,
    MAX_LEVEL,
    legacy_points_for_level,
    phase_xp_budget_for_level,
)
from game_app.talents import CLASS_SPECIALIZATIONS, RADIAL_GRAPHS


class SpecializationOptionsParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.epic_skills = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "form" and "specialization-option" in attributes.get("class", "").split():
            self.epic_skills.append(json.loads(attributes["data-epic-skills"]))


class AttributePointsLocationParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.distribution_column_depth = None
        self.points_card_in_distribution_column = False

    def handle_starttag(self, tag, attrs):
        if tag != "div":
            return
        classes = dict(attrs).get("class", "").split()
        if "attribute-distribution-column" in classes:
            self.distribution_column_depth = self.depth + 1
        if "attribute-points-card" in classes:
            self.points_card_in_distribution_column = (
                self.distribution_column_depth is not None
            )
        self.depth += 1

    def handle_endtag(self, tag):
        if tag != "div":
            return
        self.depth -= 1
        if self.depth < (self.distribution_column_depth or 0):
            self.distribution_column_depth = None


class SpecializationAbilityTests(unittest.TestCase):
    def test_every_class_path_has_a_passive_and_a_signature_skill(self):
        self.assertEqual(set(CLASS_SPECIALIZATIONS), set(CLASS_BASE_SKILLS))
        for class_id, specializations in CLASS_SPECIALIZATIONS.items():
            self.assertEqual(len(specializations), 3)
            for specialization in specializations:
                with self.subTest(class_id=class_id, path=specialization["id"]):
                    self.assertIn(specialization["id"], SPECIALIZATION_ABILITIES)
                    self.assertTrue(specialization["passive"]["description"])
                    self.assertIn(specialization["skill"]["id"], SKILLS)
                    epic_count = len(
                        SPECIALIZATION_EPIC_ABILITIES[specialization["id"]]
                    )
                    self.assertEqual(
                        specialization["branch_cost"], 48 + 4 + 6 * epic_count
                    )
                    self.assertEqual(specialization["attribute_cost"], 42)
                    self.assertEqual(
                        specialization["epic_unlock_cost"], epic_count * 4
                    )
                    self.assertEqual(
                        specialization["spell_upgrade_cost"], (2 + epic_count) * 2
                    )
                    self.assertEqual(
                        specialization["combat_cost"],
                        2 + specialization["epic_unlock_cost"]
                        + specialization["spell_upgrade_cost"],
                    )
                    self.assertEqual(sum(specialization["attribute_gains"].values()), 15)

    def test_every_specialization_has_unique_functional_nodes_and_balanced_cost(self):
        names = []
        for class_id, graph in RADIAL_GRAPHS.items():
            path_nodes = [
                node for node in graph["nodes"]
                if node.get("specialization_id") and node["category"] != "starting"
            ]
            names.extend(node["name"] for node in path_nodes)
            self.assertEqual(
                sum(node["cost"] for node in path_nodes),
                sum(
                    specialization["branch_cost"]
                    for specialization in CLASS_SPECIALIZATIONS[class_id]
                ),
                class_id,
            )
            for node in path_nodes:
                if node["category"] in {"small", "notable"}:
                    self.assertTrue(node.get("combat_modifiers"), node["id"])
        self.assertEqual(len(names), len(set(names)))

    def test_level_400_legacy_points_cover_one_path_not_all_specializations(self):
        path_costs = [
            specialization["branch_cost"]
            for specializations in CLASS_SPECIALIZATIONS.values()
            for specialization in specializations
        ]

        self.assertEqual(len(path_costs), 12)
        self.assertEqual(sum(path_costs), 714)
        self.assertEqual(legacy_points_for_level(MAX_LEVEL), 64)
        self.assertEqual(min(path_costs), 58)
        self.assertEqual(max(path_costs), 64)

    def test_signature_skill_replaces_class_skill_only_after_keystone_purchase(self):
        for class_id, specializations in CLASS_SPECIALIZATIONS.items():
            for specialization in specializations:
                talent_id = keystone_talent_id(class_id, specialization["id"])
                with self.subTest(class_id=class_id, path=specialization["id"]):
                    self.assertEqual(
                        active_class_skill(class_id, specialization["id"], ()),
                        CLASS_BASE_SKILLS[class_id],
                    )
                    self.assertEqual(
                        active_class_skill(class_id, specialization["id"], {talent_id}),
                        specialization["skill"],
                    )
                    self.assertEqual(
                        active_class_skill(class_id, specialization["id"], {
                            keystone_talent_id(class_id, "not-this-path")
                        }),
                        CLASS_BASE_SKILLS[class_id],
                    )

    def test_selected_passive_changes_real_combat_stats(self):
        character = {
            "class_id": "guardian",
            "specialization_id": "berserker",
            "level": 100,
            "strength": 100,
            "agility": 0,
            "vitality": 0,
            "energy": 0,
        }
        stats = derived_combat_stats(character)
        base_stats = derived_combat_stats({**character, "specialization_id": None})
        self.assertGreater(stats["basic_damage"], base_stats["basic_damage"])

    def test_purchased_talent_modifiers_only_apply_to_their_active_specialization(self):
        character = {
            "class_id": "guardian",
            "specialization_id": "berserker",
            "level": 100,
            "strength": 100,
            "agility": 0,
            "vitality": 0,
            "energy": 0,
        }
        node_id = "guardian_v105_berserker_road_1"
        baseline = derived_combat_stats(character)
        improved = derived_combat_stats(character, purchased_talents={node_id})
        warlord = {**character, "specialization_id": "warlord"}
        other_path = derived_combat_stats(warlord, purchased_talents={node_id})
        self.assertGreater(improved["basic_damage"], baseline["basic_damage"])
        self.assertEqual(
            other_path["basic_damage"],
            derived_combat_stats(warlord)["basic_damage"],
        )

    def test_agility_adds_critical_and_dodge_chance_and_stacks_with_talents(self):
        character = {
            "class_id": "wild_scout",
            "specialization_id": "sharpshooter",
            "level": 100,
            "strength": 0,
            "agility": 100,
            "vitality": 0,
            "energy": 0,
        }
        base = derived_combat_stats({**character, "specialization_id": None})
        stats = derived_combat_stats(character)
        improved = derived_combat_stats(
            character, purchased_talents={"wild_scout_v105_sharpshooter_amplifier"}
        )

        self.assertAlmostEqual(base["critical_chance"], .01)
        self.assertAlmostEqual(base["dodge_chance"], .01)
        self.assertAlmostEqual(stats["critical_chance"], .07)
        self.assertAlmostEqual(stats["dodge_chance"], .01)
        self.assertAlmostEqual(improved["critical_chance"], .09)
        self.assertAlmostEqual(improved["dodge_chance"], .01)
        self.assertEqual(
            combat_summary(character)["critical_chance"],
            stats["critical_chance"],
        )
        self.assertEqual(
            combat_summary(character)["dodge_chance"],
            stats["dodge_chance"],
        )

    def test_agility_chances_respect_existing_combat_caps(self):
        character = {
            "class_id": "guardian",
            "specialization_id": None,
            "level": 400,
            "strength": 0,
            "agility": 10000,
            "vitality": 0,
            "energy": 0,
        }

        stats = derived_combat_stats(character)

        self.assertEqual(stats["critical_chance"], .50)
        self.assertEqual(stats["dodge_chance"], .35)

    def test_long_range_skills_have_damage_type_element_and_projectile_metadata(self):
        self.assertEqual(CLASS_BASE_SKILLS["ash_weaver"]["damage_type"], "magical")
        self.assertEqual(CLASS_BASE_SKILLS["ash_weaver"]["element"], "fire")
        self.assertTrue(CLASS_BASE_SKILLS["ash_weaver"]["projectile"])
        self.assertEqual(CLASS_BASE_SKILLS["wild_scout"]["damage_type"], "physical")
        self.assertTrue(CLASS_BASE_SKILLS["wild_scout"]["projectile"])
        for skill_id, skill in SKILLS.items():
            with self.subTest(skill=skill_id):
                self.assertIn(skill["damage_type"], {"physical", "magical"})
                self.assertIsInstance(skill["projectile"], bool)
                if skill["damage_type"] == "magical":
                    self.assertIn(skill["element"], {"fire", "ice", "lightning", "umbral"})

    def test_epic_abilities_are_unique_and_cover_functional_effect_categories(self):
        epic_skills = [
            skill
            for skills in SPECIALIZATION_EPIC_ABILITIES.values()
            for skill in skills
        ]
        self.assertEqual(len(epic_skills), 15)
        self.assertEqual(len({skill["id"] for skill in epic_skills}), 15)
        self.assertEqual(len({skill["name"] for skill in epic_skills}), 15)
        self.assertTrue(all(skill.get("ultimate") for skill in epic_skills))
        self.assertTrue(all(skill.get("effect_kind") for skill in epic_skills))
        self.assertTrue({
            "area_burst", "chain", "drain", "echo_strikes", "guard",
            "gravity_well", "precision", "repulse", "sanctuary", "evasion",
        }.issubset({skill["effect_kind"] for skill in epic_skills}))

    def test_spell_mastery_changes_only_its_skill_damage(self):
        character = {
            "class_id": "guardian",
            "specialization_id": "berserker",
            "level": 100,
            "strength": 100,
            "agility": 0,
            "vitality": 0,
            "energy": 0,
        }
        mastery_id = skill_upgrade_talent_id(
            "guardian", "berserker", CLASS_BASE_SKILLS["guardian"]["id"]
        )
        base_stats = derived_combat_stats(character)
        upgraded_stats = derived_combat_stats(
            character, purchased_talents={mastery_id}
        )
        base_skill_damage = calculate_attack_damage(
            base_stats, CLASS_BASE_SKILLS["guardian"], "physical", None, 1, 1
        )
        upgraded_skill_damage = calculate_attack_damage(
            upgraded_stats, CLASS_BASE_SKILLS["guardian"], "physical", None, 1, 1
        )
        self.assertEqual(upgraded_stats["skill_damage_by_id"]["shield_bash"], .12)
        self.assertGreater(upgraded_skill_damage, base_skill_damage)
        self.assertEqual(base_stats["skill_damage_by_id"], {})

    def test_available_skills_require_unlocks_and_hotbar_allows_one_ultimate(self):
        class_id = "guardian"
        specialization_id = "guardian_bastion"
        epics = SPECIALIZATION_EPIC_ABILITIES[specialization_id]
        self.assertEqual(
            [skill["id"] for skill in available_class_skills(
                class_id, specialization_id, ()
            )],
            [CLASS_BASE_SKILLS[class_id]["id"]],
        )
        purchased = {
            keystone_talent_id(class_id, specialization_id),
            *(
                epic_unlock_talent_id(class_id, specialization_id, skill["id"])
                for skill in epics
            ),
        }
        unlocked = available_class_skills(
            class_id, specialization_id, purchased
        )
        self.assertEqual(len(unlocked), 4)
        slots = normalized_skill_slots(
            class_id,
            specialization_id,
            purchased,
            [
                "basic", "shield_bash", epics[0]["id"], epics[1]["id"],
            ],
        )
        self.assertEqual(slots[0], "basic")
        self.assertEqual(sum(bool(SKILLS[skill_id].get("ultimate"))
                             for skill_id in slots[1:] if skill_id), 1)

    def test_each_epic_skill_has_its_own_unlock_and_mastery_talent(self):
        for class_id, specializations in CLASS_SPECIALIZATIONS.items():
            nodes = {
                node["id"]: node for node in RADIAL_GRAPHS[class_id]["nodes"]
            }
            for specialization in specializations:
                for skill in specialization["epic_skills"]:
                    unlock_id = epic_unlock_talent_id(
                        class_id, specialization["id"], skill["id"]
                    )
                    mastery_id = skill_upgrade_talent_id(
                        class_id, specialization["id"], skill["id"]
                    )
                    with self.subTest(path=specialization["id"], skill=skill["id"]):
                        self.assertEqual(nodes[unlock_id]["cost"], 4)
                        self.assertEqual(nodes[unlock_id]["grants_skill_id"], skill["id"])
                        self.assertEqual(nodes[mastery_id]["cost"], 2)
                        self.assertEqual(nodes[mastery_id]["skill_damage_bonus"], .15)


class TalentPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary_directory = tempfile.TemporaryDirectory()
        database_path = Path(cls.temporary_directory.name) / "talents.sqlite3"
        with patch.dict(os.environ, {
            "CRONICAS_DATABASE": str(database_path),
            "CRONICAS_SECRET_KEY": "test-key-not-for-production",
        }):
            cls.app = create_app()
        cls.app.config["TESTING"] = True
        with cls.app.app_context():
            db = get_db()
            db.execute(
                """INSERT INTO users (username, password_hash, created_at)
                   VALUES (?, ?, ?)""",
                ("talent-test", "not-a-real-password-hash", "test"),
            )
            cls.user_id = db.execute(
                "SELECT id FROM users WHERE username = ?", ("talent-test",)
            ).fetchone()["id"]
            cls.character_ids = {}
            for index, class_id in enumerate(CLASS_SPECIALIZATIONS):
                db.execute(
                    """INSERT INTO characters
                       (user_id, name, name_key, class_id, level, legacy_points, created_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (
                        cls.user_id, f"Talento {index}", f"talento-{index}",
                        class_id, 100, legacy_points_for_level(MAX_LEVEL), "test",
                    ),
                )
                cls.character_ids[class_id] = db.execute(
                    "SELECT last_insert_rowid()"
                ).fetchone()[0]
            db.commit()
        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        cls.client = None
        cls.temporary_directory.cleanup()

    def _create_combat_character(self, class_id, health=100, mana=100,
                                 phase=1, wave=1, card_id=None, enemy_hp=10000):
        with self.app.app_context():
            db = get_db()
            name = f"Combate {class_id} {time.time_ns()}"
            db.execute(
                """INSERT INTO characters
                   (user_id, name, name_key, class_id, level, current_phase,
                    current_wave, current_health, current_mana, phase_xp_budget, created_at)
                   VALUES (?, ?, ?, ?, 10, ?, ?, ?, ?, ?, ?)""",
                (
                    self.user_id, name, name.lower().replace(" ", "-"),
                    class_id, phase, wave, health, mana,
                    phase_xp_budget_for_level(10), "test",
                ),
            )
            character_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
            if card_id:
                db.execute(
                    "INSERT INTO temporary_upgrades (character_id, upgrade_key) VALUES (?, ?)",
                    (character_id, card_id),
                )
            db.execute(
                """INSERT INTO wave_enemies
                   (character_id, phase, wave, enemy_index, world_x, world_y,
                    hp, max_hp, experience_reward)
                   VALUES (?, ?, ?, 0, 1201, 900, ?, ?, 1)""",
                (character_id, phase, wave, enemy_hp, enemy_hp),
            )
            enemy_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
            character = db.execute(
                "SELECT * FROM characters WHERE id = ?", (character_id,)
            ).fetchone()
            db.execute(
                """UPDATE users SET skill_slot_2 = 'rune_slash',
                   skill_slot_3 = '', skill_slot_4 = '' WHERE id = ?""",
                (self.user_id,),
            )
            db.commit()
        with self.client.session_transaction() as client_session:
            client_session["user_id"] = self.user_id
            client_session["selected_character_id"] = character_id
            client_session["csrf_token"] = "combat-test-csrf"
        return character_id, enemy_id, dict(character)

    def _combat_socket(self):
        return socketio.test_client(self.app, flask_test_client=self.client)

    def _create_progression_character(self, class_id, level=100,
                                      legacy_points=0, attribute_points=0):
        with self.app.app_context():
            db = get_db()
            name = f"Fluxo {class_id} {time.time_ns()}"
            base = CLASSES[class_id]["base_attributes"]
            db.execute(
                """INSERT INTO characters
                   (user_id, name, name_key, class_id, level, legacy_points,
                    attribute_points, strength, agility, vitality, energy, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    self.user_id, name, name.lower().replace(" ", "-"), class_id,
                    level, legacy_points, attribute_points, base["strength"],
                    base["agility"], base["vitality"], base["energy"], "test",
                ),
            )
            character_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
            db.commit()
        return character_id

    def _select_character(self, character_id):
        with self.client.session_transaction() as client_session:
            client_session["user_id"] = self.user_id
            client_session["selected_character_id"] = character_id
            client_session["csrf_token"] = "integration-test-csrf"
            client_session["in_lobby"] = True

    def _set_user_premium(self, enabled):
        with self.app.app_context():
            db = get_db()
            db.execute(
                "UPDATE users SET is_premium = ? WHERE id = ?",
                (int(enabled), self.user_id),
            )
            db.commit()

    def _set_skill_slots(self, *skill_ids):
        slots = [*skill_ids[:3], *("" for _ in range(3 - min(3, len(skill_ids))))]
        with self.app.app_context():
            get_db().execute(
                """UPDATE users SET skill_slot_2 = ?, skill_slot_3 = ?,
                   skill_slot_4 = ? WHERE id = ?""",
                (*slots, self.user_id),
            )
            get_db().commit()

    def _create_full_card_offer(self, character_id):
        card_ids = list(CARDS)
        active_ids = card_ids[:8]
        offered_ids = card_ids[8:11]
        with self.app.app_context():
            db = get_db()
            db.executemany(
                """INSERT INTO temporary_upgrades (character_id, upgrade_key)
                   VALUES (?, ?)""",
                [(character_id, card_id) for card_id in active_ids],
            )
            db.execute(
                "UPDATE characters SET pending_card_choices = 1 WHERE id = ?",
                (character_id,),
            )
            cursor = db.execute(
                """INSERT INTO card_offers
                   (character_id, phase, wave, card_ids, recommended_card_id,
                    auto_pick_at, created_at)
                   VALUES (?, 1, 1, ?, ?, ?, ?)""",
                (
                    character_id, json.dumps(offered_ids), offered_ids[0],
                    time.time() + 3600, "test",
                ),
            )
            offer_id = cursor.lastrowid
            db.commit()
        return active_ids, offered_ids, offer_id

    def test_agility_critical_chance_causes_critical_damage_in_combat(self):
        character_id, enemy_id, _ = self._create_combat_character("guardian")
        with self.app.app_context():
            db = get_db()
            db.execute(
                "UPDATE characters SET agility = 100 WHERE id = ?", (character_id,)
            )
            character = dict(db.execute(
                "SELECT * FROM characters WHERE id = ?", (character_id,)
            ).fetchone())
            expected_damage = round(
                derived_combat_stats(character)["basic_damage"]
                * CRITICAL_DAMAGE_MULTIPLIER
            )
            db.commit()
        socket_client = self._combat_socket()
        try:
            with patch("game_app.socket_events.random.random", return_value=0):
                result = socket_client.emit(
                    "combat:attack",
                    {
                        "enemy_id": enemy_id,
                        "enemy_x": 1201,
                        "enemy_y": 900,
                        "player_x": 1200,
                        "player_y": 900,
                        "csrf_token": "combat-test-csrf",
                    },
                    callback=True,
                )
        finally:
            socket_client.disconnect()

        self.assertTrue(result["ok"])
        self.assertTrue(result["critical"])
        self.assertEqual(result["damage"], expected_damage)

    def test_agility_dodge_chance_avoids_enemy_damage_in_combat(self):
        character_id, enemy_id, _ = self._create_combat_character("guardian")
        with self.app.app_context():
            db = get_db()
            db.execute(
                "UPDATE characters SET agility = 100 WHERE id = ?", (character_id,)
            )
            db.commit()
        socket_client = self._combat_socket()
        try:
            telegraph = socket_client.emit(
                "combat:request_enemy_attack",
                {
                    "enemy_id": enemy_id,
                    "enemy_x": 1201,
                    "enemy_y": 900,
                    "target_x": 1200,
                    "target_y": 900,
                    "csrf_token": "combat-test-csrf",
                },
                callback=True,
            )
            self.assertTrue(telegraph["ok"])
            time.sleep(max(
                0.01,
                (telegraph["impact_at"] - int(time.time() * 1000) + 25) / 1000,
            ))
            with patch("game_app.socket_events.random.random", return_value=0):
                result = socket_client.emit(
                    "combat:resolve_enemy_attack",
                    {
                        "attack_id": telegraph["attack_id"],
                        "player_x": 1200,
                        "player_y": 900,
                        "csrf_token": "combat-test-csrf",
                    },
                    callback=True,
                )
        finally:
            socket_client.disconnect()

        self.assertTrue(result["ok"])
        self.assertTrue(result["dodged"])
        self.assertEqual(result["damage"], 0)

    def test_expired_unresolved_enemy_attack_does_not_block_future_attacks(self):
        character_id, enemy_id, _ = self._create_combat_character("guardian")
        socket_client = self._combat_socket()
        try:
            first_attack = socket_client.emit(
                "combat:request_enemy_attack",
                {
                    "enemy_id": enemy_id,
                    "enemy_x": 1201,
                    "enemy_y": 900,
                    "target_x": 1200,
                    "target_y": 900,
                    "csrf_token": "combat-test-csrf",
                },
                callback=True,
            )
            self.assertTrue(first_attack["ok"])
            socket_events_module._pending_enemy_attacks[
                first_attack["attack_id"]
            ]["expires_at"] = 0
            socket_events_module._enemy_attack_cooldowns[
                (character_id, enemy_id)
            ] = 0

            next_attack = socket_client.emit(
                "combat:request_enemy_attack",
                {
                    "enemy_id": enemy_id,
                    "enemy_x": 1201,
                    "enemy_y": 900,
                    "target_x": 1200,
                    "target_y": 900,
                    "csrf_token": "combat-test-csrf",
                },
                callback=True,
            )
        finally:
            socket_client.disconnect()
            for attack_id, attack in list(
                socket_events_module._pending_enemy_attacks.items()
            ):
                if attack["character_id"] == character_id:
                    socket_events_module._pending_enemy_attacks.pop(attack_id, None)
            socket_events_module._enemy_attack_cooldowns.pop(
                (character_id, enemy_id), None
            )
            socket_events_module._enemy_attack_cycles.pop(
                (character_id, enemy_id), None
            )

        self.assertTrue(next_attack["ok"])

    def test_each_class_page_explains_attributes_passive_and_replacement(self):
        for class_id, character_id in self.character_ids.items():
            with self.subTest(class_id=class_id):
                with self.client.session_transaction() as client_session:
                    client_session["user_id"] = self.user_id
                    client_session["selected_character_id"] = character_id
                    client_session["in_lobby"] = True
                response = self.client.get("/talentos")
                self.assertEqual(response.status_code, 200)
                page = response.get_data(as_text=True)
                options_parser = SpecializationOptionsParser()
                options_parser.feed(page)
                self.assertEqual(
                    [skill["id"] for skills in options_parser.epic_skills for skill in skills],
                    [
                        skill["id"]
                        for specialization in CLASS_SPECIALIZATIONS[class_id]
                        for skill in specialization["epic_skills"]
                    ],
                )
                for specialization in CLASS_SPECIALIZATIONS[class_id]:
                    self.assertIn(specialization["passive"]["name"], page)
                    self.assertIn(specialization["skill"]["name"], page)
                    self.assertIn(specialization["attribute_summary"], page)
                    for epic_skill in specialization["epic_skills"]:
                        self.assertIn(epic_skill["name"], page)
                    self.assertIn(
                        f"data-keystone-cost=\"{specialization['keystone_cost']}\"",
                        page,
                    )
                self.assertIn("PASSE O MOUSE OU FOQUE UMA OPÇÃO", page)
                costs = sorted({
                    specialization["branch_cost"] for specialization
                    in CLASS_SPECIALIZATIONS[class_id]
                })
                self.assertIn(
                    f"{' ou '.join(map(str, costs))} Pontos de Legado", page
                )
                self.assertIn("Pontos de Legado", page)
                self.assertNotIn("Keystone", page)
                self.assertNotIn("recarga-base", page)
                self.assertNotIn("aguarda integração", page)
                self.assertNotIn("Berserker", page)
                self.assertNotIn("Warlord", page)
                self.assertNotIn("Sharpshooter", page)
                self.assertNotIn("Beast Master", page)
                self.assertNotIn("Arcane Archer", page)
                self.assertNotIn("Archmage", page)
                self.assertNotIn("Spellblade", page)
                self.assertNotIn("Sage", page)
                self.assertNotIn("Premium/VIP", page)

    def test_opening_tree_refunds_purchased_v104_nodes_once(self):
        with self.app.app_context():
            db = get_db()
            db.execute(
                """INSERT INTO characters
                   (user_id, name, name_key, class_id, specialization_id, level,
                    legacy_points, strength, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    self.user_id, "Transição v104", "transicao-v104", "guardian",
                    "berserker", 120, 14, 11, "test",
                ),
            )
            character_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
            db.executemany(
                """INSERT INTO character_talents (character_id, talent_id, purchased_at)
                   VALUES (?, ?, ?)""",
                [
                    (character_id, "guardian_v104_berserker_road_1", "test"),
                    (character_id, "guardian_v104_berserker_keystone", "test"),
                ],
            )
            db.commit()
        with self.client.session_transaction() as client_session:
            client_session["user_id"] = self.user_id
            client_session["selected_character_id"] = character_id
            client_session["in_lobby"] = True

        response = self.client.get("/talentos")

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Seus antigos talentos e atributos foram devolvidos",
            response.get_data(as_text=True),
        )
        repeated_response = self.client.get("/talentos")
        self.assertEqual(repeated_response.status_code, 200)
        self.assertNotIn(
            "Seus antigos talentos e atributos foram devolvidos",
            repeated_response.get_data(as_text=True),
        )
        with self.app.app_context():
            db = get_db()
            character = db.execute(
                "SELECT strength, legacy_points, talent_root_id FROM characters WHERE id = ?",
                (character_id,),
            ).fetchone()
            remaining = db.execute(
                "SELECT COUNT(*) FROM character_talents WHERE character_id = ?",
                (character_id,),
            ).fetchone()[0]
        self.assertEqual(character["strength"], 10)
        self.assertEqual(character["legacy_points"], 14)
        self.assertTrue(character["talent_root_id"].endswith("_v105_core"))
        self.assertEqual(remaining, 0)

    def test_keystone_nodes_are_purchasable_and_describe_replacement(self):
        for class_id, specializations in CLASS_SPECIALIZATIONS.items():
            graph_nodes = {
                node["id"]: node for node in RADIAL_GRAPHS[class_id]["nodes"]
            }
            for specialization in specializations:
                with self.subTest(class_id=class_id, path=specialization["id"]):
                    keystone = graph_nodes[specialization["keystone_id"]]
                    self.assertTrue(keystone["allocatable"])
                    self.assertEqual(keystone["cost"], 4)
                    self.assertIn(specialization["base_skill"]["name"], keystone["effect"])
                    self.assertIn(specialization["skill"]["name"], keystone["effect"])

    def test_initial_specialization_unlocks_at_level_100(self):
        with self.app.app_context():
            db = get_db()
            db.execute(
                """INSERT INTO characters
                   (user_id, name, name_key, class_id, level, legacy_points, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (self.user_id, "Escolha de teste", "escolha-de-teste", "guardian", 99, 11, "test"),
            )
            character_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
            db.commit()
        with self.client.session_transaction() as client_session:
            client_session["user_id"] = self.user_id
            client_session["selected_character_id"] = character_id
            client_session["in_lobby"] = True
            client_session["csrf_token"] = "specialization-csrf-token"

        payload = {
            "specialization_id": "berserker",
            "csrf_token": "specialization-csrf-token",
        }
        response = self.client.post("/talentos/evolucao", data=payload)
        self.assertEqual(response.status_code, 302)
        with self.app.app_context():
            db = get_db()
            self.assertIsNone(db.execute(
                "SELECT specialization_id FROM characters WHERE id = ?",
                (character_id,),
            ).fetchone()["specialization_id"])
            db.execute(
                "UPDATE characters SET level = 100, legacy_points = 12 WHERE id = ?",
                (character_id,),
            )
            db.commit()

        response = self.client.post("/talentos/evolucao", data=payload)
        self.assertEqual(response.status_code, 302)
        with self.app.app_context():
            db = get_db()
            character = db.execute(
                "SELECT * FROM characters WHERE id = ?", (character_id,)
            ).fetchone()
            self.assertEqual(character["specialization_id"], "berserker")
            self.assertGreater(
                derived_combat_stats(character)["basic_damage"],
                derived_combat_stats({**dict(character), "specialization_id": None})["basic_damage"],
            )

    def test_keystone_purchase_uses_four_points_after_the_attribute_branch(self):
        class_id = "guardian"
        specialization_id = "berserker"
        with self.app.app_context():
            db = get_db()
            db.execute(
                """INSERT INTO characters
                   (user_id, name, name_key, class_id, specialization_id, level,
                    legacy_points, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    self.user_id, "Guardião do teste", "guardiao-do-teste",
                    class_id, specialization_id, 400, 48, "test",
                ),
            )
            character_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
            attribute_nodes = [
                node for node in RADIAL_GRAPHS[class_id]["nodes"]
                if node.get("specialization_id") == specialization_id
                and node["stat_bonuses"]
            ]
            self.assertEqual(sum(node["cost"] for node in attribute_nodes), 42)
            db.executemany(
                """INSERT INTO character_talents (character_id, talent_id, purchased_at)
                   VALUES (?, ?, ?)""",
                [
                    (character_id, node["id"], "test")
                    for node in attribute_nodes
                ],
            )
            db.commit()
        with self.client.session_transaction() as client_session:
            client_session["user_id"] = self.user_id
            client_session["selected_character_id"] = character_id
            client_session["in_lobby"] = True
            client_session["csrf_token"] = "purchase-csrf-token"

        response = self.client.post(
            "/talentos/comprar",
            data={
                "talent_id": keystone_talent_id(class_id, specialization_id),
                "csrf_token": "purchase-csrf-token",
            },
        )
        self.assertEqual(response.status_code, 302)
        with self.app.app_context():
            db = get_db()
            self.assertIsNotNone(db.execute(
                """SELECT 1 FROM character_talents
                   WHERE character_id = ? AND talent_id = ?""",
                (character_id, keystone_talent_id(class_id, specialization_id)),
            ).fetchone())
            owned = {
                row["talent_id"] for row in db.execute(
                    "SELECT talent_id FROM character_talents WHERE character_id = ?",
                    (character_id,),
                ).fetchall()
            }
        self.assertEqual(
            active_class_skill(class_id, specialization_id, owned)["id"],
            "frenzied_cleave",
        )

    def test_signature_skill_spends_mana_and_applies_its_healing_effect(self):
        with self.app.app_context():
            db = get_db()
            db.execute(
                """INSERT INTO characters
                   (user_id, name, name_key, class_id, specialization_id, level,
                    legacy_points, current_health, current_mana, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    self.user_id, "Necromante de teste", "necromante-de-teste",
                    "ash_weaver", "necromancer", 100, 12, 50, 100, "test",
                ),
            )
            character_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
            db.execute(
                """INSERT INTO temporary_upgrades (character_id, upgrade_key)
                   VALUES (?, ?)""",
                (character_id, "healing_resonance"),
            )
            keystone_id = keystone_talent_id("ash_weaver", "necromancer")
            db.execute(
                """INSERT INTO character_talents (character_id, talent_id, purchased_at)
                   VALUES (?, ?, ?)""",
                (character_id, keystone_id, "test"),
            )
            db.execute(
                """INSERT INTO wave_enemies
                   (character_id, phase, wave, enemy_index, world_x, world_y, hp, max_hp, experience_reward)
                   VALUES (?, 1, 1, 0, 1201, 900, 10000, 10000, 1)""",
                (character_id,),
            )
            enemy_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
            db.commit()
            character = db.execute(
                "SELECT * FROM characters WHERE id = ?", (character_id,)
            ).fetchone()
            expected_damage = round(
                derived_combat_stats(
                    character, {"healing_resonance"}, {keystone_id}
                )["skill_damage"]
                * SPECIALIZATION_ABILITIES["necromancer"]["skill"]["damage_multiplier"]
            )
            healing_stats = derived_combat_stats(
                character, {"healing_resonance"}, {keystone_id}
            )
            expected_healing = round(
                round(
                    expected_damage
                    * SPECIALIZATION_ABILITIES["necromancer"]["skill"]["heal_damage_fraction"]
                )
                * (1 + healing_stats["skill_healing"])
            )

        with self.client.session_transaction() as client_session:
            client_session["user_id"] = self.user_id
            client_session["selected_character_id"] = character_id
            client_session["csrf_token"] = "test-csrf-token"
        socket_client = socketio.test_client(self.app, flask_test_client=self.client)
        try:
            result = socket_client.emit(
                "combat:attack",
                {
                    "enemy_id": enemy_id,
                    "enemy_x": 1201,
                    "enemy_y": 900,
                    "player_x": 1200,
                    "player_y": 900,
                    "skill_id": "soul_drain",
                    "csrf_token": "test-csrf-token",
                },
                callback=True,
            )
        finally:
            socket_client.disconnect()

        self.assertTrue(result["ok"])
        self.assertEqual(result["skill_id"], "soul_drain")
        self.assertEqual(result["damage"], expected_damage)
        self.assertEqual(result["mana"], 74)
        self.assertEqual(result["health"], 50 + expected_healing)

    def test_hotbar_saves_only_unlocked_skills_and_one_ultimate(self):
        character_id, _, _ = self._create_combat_character("ash_weaver")
        epic_skills = SPECIALIZATION_EPIC_ABILITIES["archmage"]
        with self.app.app_context():
            db = get_db()
            db.execute(
                "UPDATE characters SET specialization_id = 'archmage' WHERE id = ?",
                (character_id,),
            )
            talents = [
                keystone_talent_id("ash_weaver", "archmage"),
                *(
                    epic_unlock_talent_id(
                        "ash_weaver", "archmage", skill["id"]
                    )
                    for skill in epic_skills
                ),
            ]
            db.executemany(
                """INSERT INTO character_talents (character_id, talent_id, purchased_at)
                   VALUES (?, ?, ?)""",
                [(character_id, talent_id, "test") for talent_id in talents],
            )
            db.commit()
        socket_client = self._combat_socket()
        try:
            base_slots = {
                "scheme": "mouse_keyboard",
                "mouse_left_slot": 2,
                "mouse_right_slot": 3,
                "csrf_token": "combat-test-csrf",
            }
            rejected = socket_client.emit(
                "options:update_controls",
                {
                    **base_slots,
                    "skill_slots": [
                        "basic", "cinder_bolt",
                        epic_skills[0]["id"], epic_skills[1]["id"],
                    ],
                },
                callback=True,
            )
            accepted = socket_client.emit(
                "options:update_controls",
                {
                    **base_slots,
                    "skill_slots": [
                        "basic", "cinder_bolt", epic_skills[0]["id"], "",
                    ],
                },
                callback=True,
            )
            unequipped = socket_client.emit(
                "combat:attack",
                {
                    "enemy_id": 1,
                    "enemy_x": 1201,
                    "enemy_y": 900,
                    "player_x": 1200,
                    "player_y": 900,
                    "skill_id": epic_skills[1]["id"],
                    "csrf_token": "combat-test-csrf",
                },
                callback=True,
            )
        finally:
            socket_client.disconnect()
        self.assertFalse(rejected["ok"])
        self.assertIn("apenas uma habilidade suprema", rejected["error"])
        self.assertTrue(accepted["ok"])
        self.assertFalse(unequipped["ok"])
        self.assertIn("não está equipada", unequipped["error"])

    def test_control_options_persist_across_game_page_reload(self):
        character_id, _, _ = self._create_combat_character("guardian")
        skill_id = CLASS_BASE_SKILLS["guardian"]["id"]
        self._set_skill_slots(skill_id)
        socket_client = self._combat_socket()
        try:
            result = socket_client.emit(
                "options:update_controls",
                {
                    "scheme": "keyboard_only",
                    "skill_slots": ["basic", skill_id, "", ""],
                    "mouse_left_slot": 3,
                    "mouse_right_slot": 4,
                    "csrf_token": "combat-test-csrf",
                },
                callback=True,
            )
        finally:
            socket_client.disconnect()

        self.assertTrue(result["ok"])
        self.assertEqual(result["scheme"], "keyboard_only")
        self.assertEqual(result["skill_slots"], ["basic", skill_id, "", ""])
        with self.app.app_context():
            user = get_db().execute(
                """SELECT control_scheme, mouse_left_slot, mouse_right_slot,
                          skill_slot_1, skill_slot_2, skill_slot_3, skill_slot_4
                   FROM users WHERE id = ?""",
                (self.user_id,),
            ).fetchone()
        self.assertEqual(user["control_scheme"], "keyboard_only")
        self.assertEqual((user["mouse_left_slot"], user["mouse_right_slot"]), (3, 4))
        self.assertEqual(
            [user[f"skill_slot_{index}"] for index in range(1, 5)],
            ["basic", skill_id, "", ""],
        )

        page = self.client.get("/jogo")
        self.assertEqual(page.status_code, 200)
        page_html = page.get_data(as_text=True)
        self.assertIn('data-control-scheme="keyboard_only"', page_html)
        self.assertIn('option value="keyboard_only" selected', page_html)
        self.assertIn('<div class="coordinates" id="coordinates">', page_html)
        self.assertNotIn('class="bottom-bar"', page_html)

    def test_full_vip_card_collection_replacement_persists(self):
        with self.app.app_context():
            previous_premium = get_db().execute(
                "SELECT is_premium FROM users WHERE id = ?", (self.user_id,)
            ).fetchone()["is_premium"]
        try:
            self._set_user_premium(True)
            character_id, _, _ = self._create_combat_character("guardian")
            active_ids, offered_ids, offer_id = self._create_full_card_offer(character_id)
            self._select_character(character_id)
            socket_client = self._combat_socket()
            try:
                opened = socket_client.emit(
                    "card:choose",
                    {
                        "offer_id": offer_id,
                        "card_id": offered_ids[0],
                        "csrf_token": "integration-test-csrf",
                    },
                    callback=True,
                )
                self.assertTrue(opened["ok"], opened)
                self.assertTrue(opened["replacement_required"])
                self.assertEqual(opened["selected_card"]["id"], offered_ids[0])

                replaced = socket_client.emit(
                    "card:choose",
                    {
                        "offer_id": offer_id,
                        "replacement_card_id": active_ids[0],
                        "csrf_token": "integration-test-csrf",
                    },
                    callback=True,
                )
            finally:
                socket_client.disconnect()

            expected_active = set(active_ids[1:] + [offered_ids[0]])
            self.assertTrue(replaced["ok"])
            self.assertTrue(replaced["offer_resolved"])
            self.assertEqual(replaced["pending_card_choices"], 0)
            self.assertEqual(
                {card["id"] for card in replaced["active_cards"]},
                expected_active,
            )
            with self.app.app_context():
                stored = {
                    row["upgrade_key"] for row in get_db().execute(
                        "SELECT upgrade_key FROM temporary_upgrades WHERE character_id = ?",
                        (character_id,),
                    ).fetchall()
                }
                offer = get_db().execute(
                    "SELECT resolved FROM card_offers WHERE id = ?", (offer_id,)
                ).fetchone()
                pending = get_db().execute(
                    "SELECT pending_card_choices FROM characters WHERE id = ?",
                    (character_id,),
                ).fetchone()["pending_card_choices"]
            self.assertEqual(stored, expected_active)
            self.assertTrue(offer["resolved"])
            self.assertEqual(pending, 0)
            page = self.client.get("/jogo")
            self.assertIn("8 / 8", page.get_data(as_text=True))
            self.assertIn(CARDS[offered_ids[0]]["name"], page.get_data(as_text=True))
        finally:
            self._set_user_premium(previous_premium)

    def test_full_vip_card_collection_can_keep_current_cards(self):
        with self.app.app_context():
            previous_premium = get_db().execute(
                "SELECT is_premium FROM users WHERE id = ?", (self.user_id,)
            ).fetchone()["is_premium"]
        try:
            self._set_user_premium(True)
            character_id, _, _ = self._create_combat_character("guardian")
            active_ids, _, offer_id = self._create_full_card_offer(character_id)
            self._select_character(character_id)
            socket_client = self._combat_socket()
            try:
                result = socket_client.emit(
                    "card:choose",
                    {
                        "offer_id": offer_id,
                        "action": "keep",
                        "csrf_token": "integration-test-csrf",
                    },
                    callback=True,
                )
            finally:
                socket_client.disconnect()

            self.assertTrue(result["ok"], result)
            self.assertTrue(result["offer_resolved"])
            self.assertEqual(result["pending_card_choices"], 0)
            self.assertEqual(
                {card["id"] for card in result["active_cards"]},
                set(active_ids),
            )
            with self.app.app_context():
                stored = {
                    row["upgrade_key"] for row in get_db().execute(
                        "SELECT upgrade_key FROM temporary_upgrades WHERE character_id = ?",
                        (character_id,),
                    ).fetchall()
                }
                offer = get_db().execute(
                    "SELECT resolved FROM card_offers WHERE id = ?", (offer_id,)
                ).fetchone()
                pending = get_db().execute(
                    "SELECT pending_card_choices FROM characters WHERE id = ?",
                    (character_id,),
                ).fetchone()["pending_card_choices"]
            self.assertEqual(stored, set(active_ids))
            self.assertTrue(offer["resolved"])
            self.assertEqual(pending, 0)
            page = self.client.get("/jogo")
            self.assertIn("8 / 8", page.get_data(as_text=True))
            for card_id in active_ids:
                self.assertIn(CARDS[card_id]["name"], page.get_data(as_text=True))
        finally:
            self._set_user_premium(previous_premium)

    def test_repulse_ultimate_damages_and_moves_only_nearby_enemies(self):
        character_id, primary_enemy_id, _ = self._create_combat_character("guardian")
        unlock_id = epic_unlock_talent_id(
            "guardian", "guardian_bastion", "firmament_impact"
        )
        with self.app.app_context():
            db = get_db()
            db.execute(
                """UPDATE characters SET specialization_id = 'guardian_bastion',
                   current_mana = 100 WHERE id = ?""",
                (character_id,),
            )
            db.executemany(
                """INSERT INTO character_talents (character_id, talent_id, purchased_at)
                   VALUES (?, ?, ?)""",
                [
                    (
                        character_id,
                        keystone_talent_id("guardian", "guardian_bastion"),
                        "test",
                    ),
                    (character_id, unlock_id, "test"),
                ],
            )
            for index, world_x in ((1, 1210), (2, 1250), (3, 1500)):
                db.execute(
                    """INSERT INTO wave_enemies
                       (character_id, phase, wave, enemy_index, world_x, world_y,
                        hp, max_hp, experience_reward)
                       VALUES (?, 1, 1, ?, ?, 900, 10000, 10000, 1)""",
                    (character_id, index, world_x),
                )
            db.commit()
            extra_ids = [
                row["id"] for row in db.execute(
                    """SELECT id FROM wave_enemies WHERE character_id = ?
                       AND enemy_index IN (1, 2, 3) ORDER BY enemy_index""",
                    (character_id,),
                ).fetchall()
            ]
        self._set_skill_slots("shield_bash", "", "firmament_impact")
        socket_client = self._combat_socket()
        try:
            with patch("game_app.socket_events.random.random", return_value=.99):
                result = socket_client.emit(
                    "combat:attack",
                    {
                        "enemy_id": primary_enemy_id,
                        "enemy_x": 1201,
                        "enemy_y": 900,
                        "player_x": 1200,
                        "player_y": 900,
                        "skill_id": "firmament_impact",
                        "nearby_enemies": [
                            {"id": primary_enemy_id, "x": 1201, "y": 900},
                            {"id": extra_ids[0], "x": 1210, "y": 900},
                            {"id": extra_ids[1], "x": 1250, "y": 900},
                            {"id": extra_ids[2], "x": 1500, "y": 900},
                        ],
                        "csrf_token": "combat-test-csrf",
                    },
                    callback=True,
                )
        finally:
            socket_client.disconnect()
        affected = {enemy["id"]: enemy for enemy in result["affected_enemies"]}
        self.assertTrue(result["ok"])
        self.assertEqual(result["effect_kind"], "repulse")
        self.assertEqual(result["hit_count"], 3)
        self.assertEqual(set(affected), {primary_enemy_id, *extra_ids[:2]})
        self.assertGreater(affected[primary_enemy_id]["world_x"], 1201)
        self.assertGreater(affected[extra_ids[0]]["world_x"], 1210)
        self.assertGreater(affected[extra_ids[1]]["world_x"], 1250)

    def test_chain_ultimate_hits_at_most_two_nearby_secondary_targets(self):
        character_id, primary_enemy_id, _ = self._create_combat_character("wild_scout")
        unlock_id = epic_unlock_talent_id(
            "wild_scout", "arcane_archer", "lightning_constellation"
        )
        with self.app.app_context():
            db = get_db()
            db.execute(
                """UPDATE characters SET specialization_id = 'arcane_archer',
                   current_mana = 100 WHERE id = ?""",
                (character_id,),
            )
            db.executemany(
                """INSERT INTO character_talents (character_id, talent_id, purchased_at)
                   VALUES (?, ?, ?)""",
                [
                    (
                        character_id,
                        keystone_talent_id("wild_scout", "arcane_archer"),
                        "test",
                    ),
                    (character_id, unlock_id, "test"),
                ],
            )
            for index, world_x in ((1, 1210), (2, 1250), (3, 1270)):
                db.execute(
                    """INSERT INTO wave_enemies
                       (character_id, phase, wave, enemy_index, world_x, world_y,
                        hp, max_hp, experience_reward)
                       VALUES (?, 1, 1, ?, ?, 900, 10000, 10000, 1)""",
                    (character_id, index, world_x),
                )
            db.commit()
            targets = [
                dict(row) for row in db.execute(
                    """SELECT id, enemy_index, world_x, world_y FROM wave_enemies
                       WHERE character_id = ? ORDER BY enemy_index""",
                    (character_id,),
                ).fetchall()
            ]
        self._set_skill_slots("", "", "lightning_constellation")
        socket_client = self._combat_socket()
        try:
            with patch("game_app.socket_events.random.random", return_value=.99):
                launch = socket_client.emit(
                    "combat:attack",
                    {
                        "enemy_id": primary_enemy_id,
                        "enemy_x": 1201, "enemy_y": 900,
                        "player_x": 1200, "player_y": 900,
                        "skill_id": "lightning_constellation",
                        "nearby_enemies": [
                            {"id": target["id"], "x": target["world_x"],
                             "y": target["world_y"]}
                            for target in targets
                        ],
                        "csrf_token": "combat-test-csrf",
                    },
                    callback=True,
                )
            self.assertTrue(launch["projectile_pending"])
            time.sleep(max(
                .01,
                (launch["impact_at"] - int(time.time() * 1000) + 25) / 1000,
            ))
            result = socket_client.emit(
                "combat:resolve_player_projectile",
                {
                    "attack_id": launch["attack_id"],
                    "csrf_token": "combat-test-csrf",
                },
                callback=True,
            )
        finally:
            socket_client.disconnect()
        affected = {target["id"]: target for target in result["affected_enemies"]}
        self.assertTrue(result["ok"])
        self.assertEqual(result["hit_count"], 3)
        self.assertEqual(
            set(affected),
            {primary_enemy_id, targets[1]["id"], targets[2]["id"]},
        )
        self.assertEqual(affected[targets[1]["id"]]["damage"],
                         round(result["damage"] * .60))

    def test_gravity_ultimate_pulls_and_roots_nearby_enemies(self):
        character_id, primary_enemy_id, _ = self._create_combat_character("ash_weaver")
        unlock_id = epic_unlock_talent_id(
            "ash_weaver", "archmage", "inertia_well"
        )
        with self.app.app_context():
            db = get_db()
            db.execute(
                """UPDATE characters SET specialization_id = 'archmage',
                   current_mana = 100 WHERE id = ?""",
                (character_id,),
            )
            db.executemany(
                """INSERT INTO character_talents (character_id, talent_id, purchased_at)
                   VALUES (?, ?, ?)""",
                [
                    (character_id, keystone_talent_id("ash_weaver", "archmage"), "test"),
                    (character_id, unlock_id, "test"),
                ],
            )
            for index, world_x in ((1, 1210), (2, 1250), (3, 1270)):
                db.execute(
                    """INSERT INTO wave_enemies
                       (character_id, phase, wave, enemy_index, world_x, world_y,
                        hp, max_hp, experience_reward)
                       VALUES (?, 1, 1, ?, ?, 900, 10000, 10000, 1)""",
                    (character_id, index, world_x),
                )
            db.commit()
            targets = [
                dict(row) for row in db.execute(
                    """SELECT id, enemy_index, world_x, world_y FROM wave_enemies
                       WHERE character_id = ? ORDER BY enemy_index""",
                    (character_id,),
                ).fetchall()
            ]
        self._set_skill_slots("inertia_well")
        socket_client = self._combat_socket()
        try:
            with patch("game_app.socket_events.random.random", return_value=.99):
                result = socket_client.emit(
                    "combat:attack",
                    {
                        "enemy_id": primary_enemy_id,
                        "enemy_x": 1201, "enemy_y": 900,
                        "player_x": 1200, "player_y": 900,
                        "skill_id": "inertia_well",
                        "nearby_enemies": [
                            {"id": target["id"], "x": target["world_x"],
                             "y": target["world_y"]}
                            for target in targets
                        ],
                        "csrf_token": "combat-test-csrf",
                    },
                    callback=True,
                )
        finally:
            socket_client.disconnect()
        affected = {target["id"]: target for target in result["affected_enemies"]}
        self.assertTrue(result["ok"])
        self.assertEqual(result["effect_kind"], "gravity_well")
        self.assertEqual(result["hit_count"], 4)
        self.assertEqual(set(affected), {target["id"] for target in targets})
        for target in targets:
            with self.subTest(enemy=target["id"]):
                self.assertEqual(affected[target["id"]]["root_duration_ms"], 1500)
                self.assertGreater(affected[target["id"]]["damage"], 0)
                if (
                    target["id"] != primary_enemy_id
                    and target["world_x"] - 1201 > 20
                ):
                    self.assertLess(
                        affected[target["id"]]["world_x"],
                        target["world_x"],
                    )

    def test_raise_shadow_summons_a_temporary_ally_after_a_kill(self):
        character_id, first_enemy_id, character = self._create_combat_character(
            "ash_weaver", enemy_hp=1
        )
        unlock_id = epic_unlock_talent_id(
            "ash_weaver", "necromancer", "harvest_echoes"
        )
        with self.app.app_context():
            db = get_db()
            db.execute(
                """UPDATE characters SET specialization_id = 'necromancer',
                   current_mana = 100 WHERE id = ?""",
                (character_id,),
            )
            db.execute(
                """INSERT INTO character_talents (character_id, talent_id, purchased_at)
                   VALUES (?, ?, ?)""",
                (
                    character_id,
                    keystone_talent_id("ash_weaver", "necromancer"),
                    "test",
                ),
            )
            db.execute(
                """INSERT INTO character_talents (character_id, talent_id, purchased_at)
                   VALUES (?, ?, ?)""",
                (character_id, unlock_id, "test"),
            )
            db.execute(
                """INSERT INTO wave_enemies
                   (character_id, phase, wave, enemy_index, world_x, world_y,
                    hp, max_hp, experience_reward)
                   VALUES (?, 1, 1, 1, 1220, 900, 10000, 10000, 1)""",
                (character_id,),
            )
            second_enemy_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
            character = dict(db.execute(
                "SELECT * FROM characters WHERE id = ?", (character_id,)
            ).fetchone())
            expected_basic_damage = calculate_attack_damage(
                derived_combat_stats(character), None, "physical", None, 1, 1
            )
            db.commit()
        self._set_skill_slots("harvest_echoes")
        socket_client = self._combat_socket()
        try:
            with patch("game_app.socket_events.random.random", return_value=.99):
                summon = socket_client.emit(
                    "combat:attack",
                    {
                        "enemy_id": first_enemy_id,
                        "enemy_x": 1201, "enemy_y": 900,
                        "player_x": 1200, "player_y": 900,
                        "skill_id": "harvest_echoes",
                        "csrf_token": "combat-test-csrf",
                    },
                    callback=True,
                )
                follow_up = socket_client.emit(
                    "combat:attack",
                    {
                        "enemy_id": second_enemy_id,
                        "enemy_x": 1220, "enemy_y": 900,
                        "player_x": 1200, "player_y": 900,
                        "csrf_token": "combat-test-csrf",
                    },
                    callback=True,
                )
        finally:
            socket_client.disconnect()
        self.assertTrue(summon["defeated"])
        self.assertTrue(summon["shadow_summoned"])
        self.assertEqual(summon["shadow_soldier_count"], 1)
        self.assertEqual(follow_up["shadow_support_damage"],
                         round(expected_basic_damage * .35))
        self.assertEqual(follow_up["shadow_soldier_count"], 1)
        self.assertGreater(follow_up["damage"], expected_basic_damage)

    def test_guard_ultimate_reduces_the_next_enemy_hit(self):
        character_id, enemy_id, _ = self._create_combat_character("guardian")
        unlock_id = epic_unlock_talent_id(
            "guardian", "guardian_bastion", "unyielding_wall"
        )
        with self.app.app_context():
            db = get_db()
            db.execute(
                """UPDATE characters SET specialization_id = 'guardian_bastion',
                   current_mana = 100 WHERE id = ?""",
                (character_id,),
            )
            db.executemany(
                """INSERT INTO character_talents (character_id, talent_id, purchased_at)
                   VALUES (?, ?, ?)""",
                [
                    (
                        character_id,
                        keystone_talent_id("guardian", "guardian_bastion"),
                        "test",
                    ),
                    (character_id, unlock_id, "test"),
                ],
            )
            db.commit()
        self._set_skill_slots("", "", "unyielding_wall")
        socket_client = self._combat_socket()
        try:
            activated = socket_client.emit(
                "combat:attack",
                {
                    "enemy_id": enemy_id, "enemy_x": 1201, "enemy_y": 900,
                    "player_x": 1200, "player_y": 900,
                    "skill_id": "unyielding_wall",
                    "csrf_token": "combat-test-csrf",
                },
                callback=True,
            )
            telegraph = socket_client.emit(
                "combat:request_enemy_attack",
                {
                    "enemy_id": enemy_id, "enemy_x": 1201, "enemy_y": 900,
                    "target_x": 1200, "target_y": 900,
                    "csrf_token": "combat-test-csrf",
                },
                callback=True,
            )
            time.sleep(max(
                .01,
                (telegraph["impact_at"] - int(time.time() * 1000) + 25) / 1000,
            ))
            with patch("game_app.socket_events.random.random", return_value=.99):
                incoming = socket_client.emit(
                    "combat:resolve_enemy_attack",
                    {
                        "attack_id": telegraph["attack_id"],
                        "player_x": 1200, "player_y": 900,
                        "csrf_token": "combat-test-csrf",
                    },
                    callback=True,
                )
        finally:
            socket_client.disconnect()
        self.assertTrue(activated["ok"])
        self.assertEqual(activated["active_effect"]["damage_reduction"], .35)
        self.assertTrue(telegraph["ok"])
        self.assertTrue(incoming["ok"])
        self.assertLess(incoming["damage"], telegraph["damage"])

    def test_precision_ultimate_forces_critical_damage_on_projectile_impact(self):
        character_id, enemy_id, _ = self._create_combat_character("wild_scout")
        unlock_id = epic_unlock_talent_id(
            "wild_scout", "sharpshooter", "horizon_line"
        )
        with self.app.app_context():
            db = get_db()
            db.execute(
                """UPDATE characters SET specialization_id = 'sharpshooter',
                   current_mana = 100 WHERE id = ?""",
                (character_id,),
            )
            db.executemany(
                """INSERT INTO character_talents (character_id, talent_id, purchased_at)
                   VALUES (?, ?, ?)""",
                [
                    (
                        character_id,
                        keystone_talent_id("wild_scout", "sharpshooter"),
                        "test",
                    ),
                    (character_id, unlock_id, "test"),
                ],
            )
            db.commit()
        self._set_skill_slots("", "", "horizon_line")
        socket_client = self._combat_socket()
        try:
            with patch("game_app.socket_events.random.random", return_value=.99):
                launch = socket_client.emit(
                    "combat:attack",
                    {
                        "enemy_id": enemy_id, "enemy_x": 1201, "enemy_y": 900,
                        "player_x": 1200, "player_y": 900,
                        "skill_id": "horizon_line",
                        "csrf_token": "combat-test-csrf",
                    },
                    callback=True,
                )
            self.assertTrue(launch["projectile_pending"])
            time.sleep(max(
                .01,
                (launch["impact_at"] - int(time.time() * 1000) + 25) / 1000,
            ))
            result = socket_client.emit(
                "combat:resolve_player_projectile",
                {
                    "attack_id": launch["attack_id"],
                    "csrf_token": "combat-test-csrf",
                },
                callback=True,
            )
        finally:
            socket_client.disconnect()
        self.assertTrue(result["ok"])
        self.assertTrue(result["critical"])
        self.assertEqual(result["skill_id"], "horizon_line")

    def test_mana_harvest_card_restores_mana_when_an_enemy_is_defeated(self):
        character_id, enemy_id, character = self._create_combat_character(
            "guardian", health=100, mana=0,
            card_id="mana_harvest", enemy_hp=1,
        )
        expected_mana = round(
            derived_combat_stats(character, {"mana_harvest"})["max_mana"] * .05
        )
        socket_client = self._combat_socket()
        try:
            result = socket_client.emit(
                "combat:attack",
                {
                    "enemy_id": enemy_id,
                    "enemy_x": 1201,
                    "enemy_y": 900,
                    "player_x": 1200,
                    "player_y": 900,
                    "csrf_token": "combat-test-csrf",
                },
                callback=True,
            )
        finally:
            socket_client.disconnect()

        self.assertTrue(result["ok"])
        self.assertTrue(result["defeated"])
        self.assertEqual(result["mana"], expected_mana)

    def test_projectile_waits_for_impact_and_applies_life_steal(self):
        character_id, enemy_id, character = self._create_combat_character(
            "ash_weaver", health=40, card_id="vital_siphon"
        )
        purchased_talents = {
            "ash_weaver_v105_archmage_road_2",
            "ash_weaver_v105_archmage_wheel_3",
        }
        character["specialization_id"] = "archmage"
        with self.app.app_context():
            db = get_db()
            db.execute(
                "UPDATE characters SET specialization_id = ? WHERE id = ?",
                ("archmage", character_id),
            )
            db.executemany(
                """INSERT INTO character_talents (character_id, talent_id, purchased_at)
                   VALUES (?, ?, ?)""",
                [(character_id, talent_id, "test") for talent_id in purchased_talents],
            )
            db.commit()
        socket_client = self._combat_socket()
        try:
            launch = socket_client.emit(
                "combat:attack",
                {
                    "enemy_id": enemy_id, "enemy_x": 1201, "enemy_y": 900,
                    "player_x": 1200, "player_y": 900,
                    "skill_id": "cinder_bolt", "csrf_token": "combat-test-csrf",
                },
                callback=True,
            )
            self.assertTrue(launch["ok"])
            self.assertTrue(launch["projectile_pending"])
            with self.app.app_context():
                db = get_db()
                self.assertEqual(
                    db.execute("SELECT hp FROM wave_enemies WHERE id = ?", (enemy_id,)).fetchone()["hp"],
                    10000,
                )
                self.assertEqual(
                    db.execute("SELECT current_health FROM characters WHERE id = ?", (character_id,)).fetchone()["current_health"],
                    40,
                )
                self.assertEqual(
                    db.execute("SELECT current_mana FROM characters WHERE id = ?", (character_id,)).fetchone()["current_mana"],
                    80,
                )

            time.sleep((launch["projectile"]["flight_ms"] + 25) / 1000)
            impact = socket_client.emit(
                "combat:resolve_player_projectile",
                {"attack_id": launch["attack_id"], "csrf_token": "combat-test-csrf"},
                callback=True,
            )
        finally:
            socket_client.disconnect()

        self.assertTrue(impact["ok"])
        self.assertGreater(impact["damage"], 0)
        self.assertEqual(
            combat_summary(
                character, {"vital_siphon"}, purchased_talents
            )["projectile_damage_exact"],
            impact["damage"],
        )
        summary = combat_summary(character, {"vital_siphon"}, purchased_talents)
        self.assertGreater(summary["projectile_damage_exact"], 0)
        self.assertGreater(summary["elemental_damage_exact"], 0)
        self.assertEqual(impact["life_stolen"], round(impact["damage"] * .05))
        with self.app.app_context():
            db = get_db()
            self.assertEqual(
                db.execute("SELECT hp FROM wave_enemies WHERE id = ?", (enemy_id,)).fetchone()["hp"],
                10000 - impact["damage"],
            )
            self.assertEqual(
                db.execute("SELECT current_health FROM characters WHERE id = ?", (character_id,)).fetchone()["current_health"],
                40 + impact["life_stolen"],
            )

    def test_matching_elemental_boss_affinity_reduces_magic_damage(self):
        _, enemy_id, character = self._create_combat_character(
            "ash_weaver", phase=10, wave=10
        )
        socket_client = self._combat_socket()
        try:
            with patch("game_app.socket_events.random.random", return_value=.99):
                launch = socket_client.emit(
                    "combat:attack",
                    {
                        "enemy_id": enemy_id, "enemy_x": 1201, "enemy_y": 900,
                        "player_x": 1200, "player_y": 900,
                        "skill_id": "cinder_bolt", "csrf_token": "combat-test-csrf",
                    },
                    callback=True,
                )
                time.sleep((launch["projectile"]["flight_ms"] + 25) / 1000)
                impact = socket_client.emit(
                    "combat:resolve_player_projectile",
                    {"attack_id": launch["attack_id"], "csrf_token": "combat-test-csrf"},
                    callback=True,
                )
        finally:
            socket_client.disconnect()

        base_damage = round(
            derived_combat_stats(character)["skill_damage"]
            * CLASS_BASE_SKILLS["ash_weaver"]["damage_multiplier"]
        )
        expected = max(1, round(base_damage * (1 - boss_affinity(10)["resistance"])))
        self.assertTrue(impact["ok"])
        self.assertEqual(
            combat_summary(character)["elemental_damage_exact"],
            base_damage,
        )
        self.assertEqual(impact["damage"], expected)

    def test_reflection_card_returns_ten_percent_of_damage_received(self):
        character_id, enemy_id, _ = self._create_combat_character(
            "guardian", health=100, card_id="mirror_ward"
        )
        socket_client = self._combat_socket()
        try:
            telegraph = socket_client.emit(
                "combat:request_enemy_attack",
                {
                    "enemy_id": enemy_id, "enemy_x": 1201, "enemy_y": 900,
                    "target_x": 1200, "target_y": 900,
                    "csrf_token": "combat-test-csrf",
                },
                callback=True,
            )
            self.assertTrue(telegraph["ok"])
            time.sleep((telegraph["impact_at"] - int(time.time() * 1000) + 25) / 1000)
            result = socket_client.emit(
                "combat:resolve_enemy_attack",
                {
                    "attack_id": telegraph["attack_id"],
                    "player_x": 1200, "player_y": 900,
                    "csrf_token": "combat-test-csrf",
                },
                callback=True,
            )
        finally:
            socket_client.disconnect()

        self.assertTrue(result["ok"])
        expected_reflection = round(result["damage"] * .10)
        self.assertEqual(result["reflected_damage"], expected_reflection)
        with self.app.app_context():
            db = get_db()
            self.assertEqual(
                db.execute("SELECT hp FROM wave_enemies WHERE id = ?", (enemy_id,)).fetchone()["hp"],
                10000 - expected_reflection,
            )

    def test_lethal_reflection_finishes_enemy_and_advances_the_wave(self):
        character_id, enemy_id, _ = self._create_combat_character(
            "guardian", health=100, card_id="mirror_ward", enemy_hp=2
        )
        socket_client = self._combat_socket()
        try:
            telegraph = socket_client.emit(
                "combat:request_enemy_attack",
                {
                    "enemy_id": enemy_id, "enemy_x": 1201, "enemy_y": 900,
                    "target_x": 1200, "target_y": 900,
                    "csrf_token": "combat-test-csrf",
                },
                callback=True,
            )
            time.sleep((telegraph["impact_at"] - int(time.time() * 1000) + 25) / 1000)
            result = socket_client.emit(
                "combat:resolve_enemy_attack",
                {
                    "attack_id": telegraph["attack_id"],
                    "player_x": 1200, "player_y": 900,
                    "csrf_token": "combat-test-csrf",
                },
                callback=True,
            )
        finally:
            socket_client.disconnect()

        self.assertTrue(result["ok"])
        self.assertEqual(result["reflected_damage"], 2)
        with self.app.app_context():
            db = get_db()
            defeated = db.execute(
                "SELECT hp, alive FROM wave_enemies WHERE id = ?", (enemy_id,)
            ).fetchone()
            character = db.execute(
                "SELECT current_wave FROM characters WHERE id = ?", (character_id,)
            ).fetchone()
            self.assertEqual((defeated["hp"], defeated["alive"]), (0, 0))
            self.assertEqual(character["current_wave"], 2)
            self.assertIsNotNone(db.execute(
                "SELECT 1 FROM card_xp_orbs WHERE character_id = ? AND source_key = ?",
                (character_id, f"enemy:{enemy_id}"),
            ).fetchone())

    def test_completing_phase_30_marks_season_complete_without_advancing_to_31(self):
        character_id, _, _ = self._create_combat_character(
            "guardian", phase=30, wave=10
        )
        socket_client = self._combat_socket()
        try:
            result = socket_client.emit(
                "game:complete_wave",
                {"csrf_token": "combat-test-csrf"},
                callback=True,
            )
        finally:
            socket_client.disconnect()

        with self.app.app_context():
            saved = get_db().execute(
                """SELECT current_phase, current_wave, campaign_complete,
                          phase_intermission
                   FROM characters WHERE id = ?""",
                (character_id,),
            ).fetchone()
        self.assertTrue(result["ok"])
        self.assertEqual(tuple(saved), (30, 10, 1, 0))

    def test_combat_summary_shows_active_and_elemental_effects_in_player_terms(self):
        character = {
            "class_id": "ash_weaver",
            "specialization_id": None,
            "level": 10,
            "strength": 0,
            "agility": 0,
            "vitality": 0,
            "energy": 0,
        }
        summary = combat_summary(character, {"vital_siphon", "mirror_ward"})
        self.assertEqual(summary["life_steal"], .05)
        self.assertEqual(summary["damage_reflection"], .10)
        self.assertEqual(summary["elemental_name"], "Fogo")
        self.assertGreater(summary["projectile_damage_exact"], 0)

    def test_attributes_page_displays_the_new_effects_in_portuguese(self):
        self._create_combat_character(
            "ash_weaver", card_id="vital_siphon"
        )
        with self.client.session_transaction() as client_session:
            client_session["in_lobby"] = True
        response = self.client.get("/jogo/atributos")
        self.assertEqual(response.status_code, 200)
        page = response.get_data(as_text=True)
        self.assertIn("Dano da habilidade com projétil", page)
        self.assertIn("Dano elemental da habilidade", page)
        self.assertIn("Vida recuperada pelo dano causado", page)
        self.assertIn("Dano devolvido ao atacante", page)
        self.assertIn("A cada ponto: +0,01% de chance crítica", page)
        self.assertIn("Chance de acerto crítico", page)
        self.assertIn("Chance de esquiva", page)
        self.assertIn(">5,0%</strong>", page)

    def test_free_attribute_points_card_is_in_the_left_column(self):
        self._create_combat_character("guardian")
        with self.client.session_transaction() as client_session:
            client_session["in_lobby"] = True
        response = self.client.get("/jogo/atributos")
        self.assertEqual(response.status_code, 200)

        parser = AttributePointsLocationParser()
        parser.feed(response.get_data(as_text=True))
        self.assertTrue(parser.points_card_in_distribution_column)

    def test_attributes_page_keeps_specialization_effects_after_reload(self):
        character_id, _, _ = self._create_combat_character("guardian")
        talent_id = "guardian_v105_berserker_road_1"
        with self.app.app_context():
            db = get_db()
            db.execute(
                "UPDATE characters SET specialization_id = 'berserker' WHERE id = ?",
                (character_id,),
            )
            db.execute(
                """INSERT INTO character_talents
                   (character_id, talent_id, purchased_at) VALUES (?, ?, ?)""",
                (character_id, talent_id, "test"),
            )
            character = dict(db.execute(
                "SELECT * FROM characters WHERE id = ?", (character_id,)
            ).fetchone())
            expected_damage = combat_summary(
                character, purchased_talents={talent_id}
            )["basic_damage_exact"]
            db.commit()
        with self.client.session_transaction() as client_session:
            client_session["in_lobby"] = True

        response = self.client.get("/jogo/atributos")

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            f'data-combat-value="basic_damage_exact">{expected_damage:.1f}'.replace(".", ",") + "</strong>",
            response.get_data(as_text=True),
        )

    def test_talent_purchase_branch_lock_and_vip_swap_persist_for_every_class(self):
        with self.app.app_context():
            previous_premium = get_db().execute(
                "SELECT is_premium FROM users WHERE id = ?", (self.user_id,)
            ).fetchone()["is_premium"]
        try:
            for class_id, specializations in CLASS_SPECIALIZATIONS.items():
                with self.subTest(class_id=class_id):
                    character_id = self._create_progression_character(
                        class_id, legacy_points=legacy_points_for_level(MAX_LEVEL)
                    )
                    self._select_character(character_id)
                    self._set_user_premium(True)
                    selected, alternate = specializations[:2]
                    graph = RADIAL_GRAPHS[class_id]
                    selected_node = next(
                        node for node in graph["nodes"]
                        if node.get("specialization_id") == selected["id"]
                        and node["id"] in graph["adjacency"][graph["root_id"]]
                    )
                    alternate_node = next(
                        node for node in graph["nodes"]
                        if node.get("specialization_id") == alternate["id"]
                        and node["id"] in graph["adjacency"][graph["root_id"]]
                    )
                    csrf = "integration-test-csrf"

                    chosen = self.client.post(
                        "/talentos/evolucao",
                        data={"csrf_token": csrf, "specialization_id": selected["id"]},
                        follow_redirects=True,
                    )
                    self.assertIn(
                        f"Caminho escolhido: {selected['name']}.",
                        chosen.get_data(as_text=True),
                    )

                    blocked = self.client.post(
                        "/talentos/comprar",
                        data={"csrf_token": csrf, "talent_id": alternate_node["id"]},
                        follow_redirects=True,
                    )
                    self.assertIn(
                        "Esse ramo pertence a outra evolução",
                        blocked.get_data(as_text=True),
                    )
                    with self.app.app_context():
                        self.assertIsNone(get_db().execute(
                            """SELECT 1 FROM character_talents
                               WHERE character_id = ? AND talent_id = ?""",
                            (character_id, alternate_node["id"]),
                        ).fetchone())

                    purchased = self.client.post(
                        "/talentos/comprar",
                        data={"csrf_token": csrf, "talent_id": selected_node["id"]},
                        follow_redirects=True,
                    )
                    self.assertIn(
                        f"Talento adquirido: {selected_node['name']}.",
                        purchased.get_data(as_text=True),
                    )
                    self.assertIn(
                        f"{selected_node['cost']} Pontos de Legado usados",
                        purchased.get_data(as_text=True),
                    )
                    with self.app.app_context():
                        db = get_db()
                        character = db.execute(
                            "SELECT * FROM characters WHERE id = ?", (character_id,)
                        ).fetchone()
                        self.assertEqual(character["specialization_id"], selected["id"])
                        for attribute, bonus in selected_node["stat_bonuses"].items():
                            self.assertEqual(
                                character[attribute],
                                CLASSES[class_id]["base_attributes"][attribute] + bonus,
                            )

                    self._set_user_premium(False)
                    denied_swap = self.client.post(
                        "/talentos/evolucao",
                        data={"csrf_token": csrf, "specialization_id": alternate["id"]},
                        follow_redirects=True,
                    )
                    self.assertIn(
                        "É preciso ter o benefício especial ativo",
                        denied_swap.get_data(as_text=True),
                    )
                    with self.app.app_context():
                        character = get_db().execute(
                            "SELECT specialization_id FROM characters WHERE id = ?",
                            (character_id,),
                        ).fetchone()
                        self.assertEqual(character["specialization_id"], selected["id"])

                    self._set_user_premium(True)
                    swapped = self.client.post(
                        "/talentos/evolucao",
                        data={"csrf_token": csrf, "specialization_id": alternate["id"]},
                        follow_redirects=True,
                    )
                    self.assertIn(
                        f"Caminho alterado para {alternate['name']}.",
                        swapped.get_data(as_text=True),
                    )
                    reloaded = self.client.get("/talentos")
                    self.assertEqual(reloaded.status_code, 200)
                    with self.app.app_context():
                        db = get_db()
                        character = db.execute(
                            "SELECT * FROM characters WHERE id = ?", (character_id,)
                        ).fetchone()
                        owned = {
                            row["talent_id"] for row in db.execute(
                                "SELECT talent_id FROM character_talents WHERE character_id = ?",
                                (character_id,),
                            ).fetchall()
                        }
                    self.assertEqual(character["specialization_id"], alternate["id"])
                    self.assertEqual(
                        character["talent_root_id"], graph["root_id"]
                    )
                    self.assertEqual(character["legacy_points"], legacy_points_for_level(MAX_LEVEL))
                    self.assertNotIn(selected_node["id"], owned)
                    self.assertIn(
                        "0 Pontos de Legado usados", reloaded.get_data(as_text=True)
                    )
                    self.assertTrue(all(
                        character[key] == value
                        for key, value in CLASSES[class_id]["base_attributes"].items()
                    ))
                    self.assertIn(alternate["name"], reloaded.get_data(as_text=True))
        finally:
            self._set_user_premium(previous_premium)

    def test_socket_attribute_allocation_updates_all_four_stats_and_notifies(self):
        character_id = self._create_progression_character(
            "guardian", level=10, attribute_points=4
        )
        self._select_character(character_id)
        with self.app.app_context():
            initial = dict(get_db().execute(
                "SELECT * FROM characters WHERE id = ?", (character_id,)
            ).fetchone())
        base_summary = combat_summary(initial)
        socket_client = self._combat_socket()
        try:
            cases = (
                ("strength", "Força", "basic_damage_exact"),
                ("agility", "Agilidade", "critical_chance"),
                ("vitality", "Vitalidade", "max_health"),
                ("energy", "Energia", "max_mana"),
            )
            previous_summary = base_summary
            for index, (attribute, label, changed_stat) in enumerate(cases):
                with self.subTest(attribute=attribute):
                    result = socket_client.emit(
                        "attributes:allocate",
                        {
                            "attribute": attribute,
                            "amount": 1,
                            "csrf_token": "integration-test-csrf",
                        },
                        callback=True,
                    )
                    self.assertTrue(result["ok"])
                    self.assertEqual(result["attribute_points"], 3 - index)
                    self.assertEqual(
                        result["attributes"][attribute],
                        initial[attribute] + 1,
                    )
                    self.assertGreater(
                        result["combat_summary"][changed_stat],
                        previous_summary[changed_stat],
                    )
                    self.assertEqual(
                        result["message"],
                        f"1 ponto adicionado em {label}.",
                    )
                    updates = [
                        event for event in socket_client.get_received()
                        if event["name"] == "attributes:updated"
                    ]
                    self.assertEqual(len(updates), 1)
                    self.assertEqual(
                        updates[0]["args"][0]["message"], result["message"]
                    )
                    previous_summary = result["combat_summary"]

            insufficient = socket_client.emit(
                "attributes:allocate",
                {
                    "attribute": "strength",
                    "amount": 1,
                    "csrf_token": "integration-test-csrf",
                },
                callback=True,
            )
            self.assertFalse(insufficient["ok"])
            self.assertEqual(
                insufficient["error"],
                "Você não possui pontos livres suficientes.",
            )
            self.assertFalse(socket_client.get_received())
        finally:
            socket_client.disconnect()

        with self.app.app_context():
            character = get_db().execute(
                "SELECT * FROM characters WHERE id = ?", (character_id,)
            ).fetchone()
        self.assertEqual(character["attribute_points"], 0)
        for attribute, _, _ in cases:
            self.assertEqual(character[attribute], initial[attribute] + 1)

    def test_vip_auto_distribution_persists_and_notifies_for_every_class(self):
        with self.app.app_context():
            previous_premium = get_db().execute(
                "SELECT is_premium FROM users WHERE id = ?", (self.user_id,)
            ).fetchone()["is_premium"]
        try:
            self._set_user_premium(True)
            for class_id in CLASS_SPECIALIZATIONS:
                with self.subTest(class_id=class_id):
                    character_id = self._create_progression_character(
                        class_id, level=10, attribute_points=20
                    )
                    self._select_character(character_id)
                    socket_client = self._combat_socket()
                    try:
                        result = socket_client.emit(
                            "attributes:auto_toggle",
                            {"enabled": 1, "csrf_token": "integration-test-csrf"},
                            callback=True,
                        )
                        self.assertTrue(result["ok"])
                        self.assertEqual(result["attribute_points"], 0)
                        self.assertTrue(result["auto_allocate_attributes"])
                        self.assertEqual(
                            result["class_distribution"],
                            CLASS_AUTO_DISTRIBUTION[class_id],
                        )
                        self.assertIn(
                            f"Distribuição automática ativada para {CLASSES[class_id]['name']}",
                            result["message"],
                        )
                        growth = {
                            key: result["attributes"][key]
                            - CLASSES[class_id]["base_attributes"][key]
                            for key in ("strength", "agility", "vitality", "energy")
                        }
                        self.assertEqual(sum(growth.values()), 20)
                        highest_weight = max(CLASS_AUTO_DISTRIBUTION[class_id].values())
                        lowest_weight = min(CLASS_AUTO_DISTRIBUTION[class_id].values())
                        self.assertGreaterEqual(
                            max(
                                growth[key] for key, weight
                                in CLASS_AUTO_DISTRIBUTION[class_id].items()
                                if weight == highest_weight
                            ),
                            max(
                                growth[key] for key, weight
                                in CLASS_AUTO_DISTRIBUTION[class_id].items()
                                if weight == lowest_weight
                            ),
                        )
                        updates = [
                            event for event in socket_client.get_received()
                            if event["name"] == "attributes:updated"
                        ]
                        self.assertEqual(len(updates), 1)
                        self.assertEqual(
                            updates[0]["args"][0]["message"], result["message"]
                        )
                        page = self.client.get("/jogo/atributos")
                        self.assertEqual(page.status_code, 200)
                        self.assertIn('data-auto-enabled="1"', page.get_data(as_text=True))

                        with self.app.app_context():
                            stored = get_db().execute(
                                "SELECT * FROM characters WHERE id = ?", (character_id,)
                            ).fetchone()
                        attributes_after_activation = {
                            key: stored[key]
                            for key in ("strength", "agility", "vitality", "energy")
                        }
                        self.assertTrue(stored["auto_allocate_attributes"])
                        self.assertEqual(stored["attribute_points"], 0)

                        disabled = socket_client.emit(
                            "attributes:auto_toggle",
                            {"enabled": 0, "csrf_token": "integration-test-csrf"},
                            callback=True,
                        )
                        self.assertTrue(disabled["ok"])
                        self.assertFalse(disabled["auto_allocate_attributes"])
                        self.assertEqual(
                            disabled["message"],
                            "Distribuição automática desativada. Os atributos já distribuídos permanecem como estão.",
                        )
                        self.assertEqual(disabled["attributes"], attributes_after_activation)
                        updates = [
                            event for event in socket_client.get_received()
                            if event["name"] == "attributes:updated"
                        ]
                        self.assertEqual(len(updates), 1)
                        self.assertEqual(
                            updates[0]["args"][0]["message"], disabled["message"]
                        )
                        page = self.client.get("/jogo/atributos")
                        self.assertEqual(page.status_code, 200)
                        self.assertIn('data-auto-enabled="0"', page.get_data(as_text=True))
                    finally:
                        socket_client.disconnect()

            denied_character = self._create_progression_character(
                "guardian", level=10, attribute_points=3
            )
            self._select_character(denied_character)
            self._set_user_premium(False)
            socket_client = self._combat_socket()
            try:
                denied = socket_client.emit(
                    "attributes:auto_toggle",
                    {"enabled": 1, "csrf_token": "integration-test-csrf"},
                    callback=True,
                )
                self.assertFalse(denied["ok"])
                self.assertEqual(
                    denied["error"],
                    "A distribuição automática exige o benefício especial.",
                )
                self.assertFalse(socket_client.get_received())
                with self.app.app_context():
                    stored = get_db().execute(
                        "SELECT attribute_points, auto_allocate_attributes FROM characters WHERE id = ?",
                        (denied_character,),
                    ).fetchone()
                self.assertEqual(stored["attribute_points"], 3)
                self.assertFalse(stored["auto_allocate_attributes"])
            finally:
                socket_client.disconnect()
        finally:
            self._set_user_premium(previous_premium)


if __name__ == "__main__":
    unittest.main()
