import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from flask import Flask

from game_app.database import close_db, get_db, init_db


class LegacyPointsMigrationTests(unittest.TestCase):
    def test_migration_credits_old_characters_idempotently(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "test.sqlite3"
            app = Flask(__name__)
            app.config["DATABASE"] = str(database_path)
            app.teardown_appcontext(close_db)

            init_db(app)
            with app.app_context():
                db = get_db()
                db.execute(
                    """INSERT INTO users (username, password_hash, created_at)
                       VALUES (?, ?, ?)""",
                    ("tester", "not-a-real-password-hash", "test"),
                )
                user_id = db.execute(
                    "SELECT id FROM users WHERE username = ?", ("tester",)
                ).fetchone()["id"]
                db.execute(
                    """INSERT INTO characters
                       (user_id, name, name_key, class_id, level, resets,
                        legacy_points, created_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (user_id, "Legado", "legado", "guardian", 100, 2, 0, "test"),
                )
                db.execute(
                    """INSERT INTO characters
                       (user_id, name, name_key, class_id, level, resets,
                        legacy_points, created_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (user_id, "Saldo preservado", "saldo-preservado", "guardian",
                     100, 0, 99, "test"),
                )
                db.execute(
                    """INSERT INTO characters
                       (user_id, name, name_key, class_id, level, resets,
                        legacy_points, created_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (user_id, "Nível máximo", "nivel-maximo", "guardian",
                     400, 0, 0, "test"),
                )
                db.commit()

            init_db(app)
            init_db(app)

            with closing(sqlite3.connect(database_path)) as db:
                balances = db.execute(
                    "SELECT name, legacy_points FROM characters ORDER BY name"
                ).fetchall()

        self.assertEqual(
            balances,
            [("Legado", 18), ("Nível máximo", 64), ("Saldo preservado", 99)],
        )

    def test_legacy_mission_currency_schema_migrates_to_gold_without_losing_values(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "gold-migration.sqlite3"
            app = Flask(__name__)
            app.config["DATABASE"] = str(database_path)
            app.teardown_appcontext(close_db)
            init_db(app)

            with app.app_context():
                db = get_db()
                db.execute(
                    """INSERT INTO users (username, password_hash, created_at, wallet_gold)
                       VALUES ('gold-migration', 'unused', 'test', 12345)"""
                )
                user_id = db.execute(
                    "SELECT id FROM users WHERE username = 'gold-migration'"
                ).fetchone()["id"]
                db.execute(
                    """INSERT INTO characters
                       (user_id, name, name_key, class_id, created_at)
                       VALUES (?, 'Gold Tester', 'gold-tester', 'guardian', 'test')""",
                    (user_id,),
                )
                character_id = db.execute(
                    "SELECT id FROM characters WHERE name_key = 'gold-tester'"
                ).fetchone()["id"]
                run_cursor = db.execute(
                    """INSERT INTO mission_runs
                       (user_id, character_id, difficulty, phase, start_time,
                        monster_gold, phase_bonus_gold, created_at)
                       VALUES (?, ?, 'risk_low', 1, 1, 25, 50, 'test')""",
                    (user_id, character_id),
                )
                run_id = run_cursor.lastrowid
                db.execute(
                    """INSERT INTO gold_ledger
                       (user_id, mission_run_id, source_key, transaction_type,
                        amount_gold, created_at)
                       VALUES (?, ?, 'migration-test', 'phase_bonus', 50, 'test')""",
                    (user_id, run_id),
                )
                db.execute(
                    """INSERT INTO inventory_items
                       (user_id, item_name, rarity, salvage_value_gold,
                        obtained_from_run_id, created_at)
                       VALUES (?, 'Baú comum', 'common', 25, ?, 'test')""",
                    (user_id, run_id),
                )
                db.execute(
                    """INSERT INTO staging_inventory
                       (mission_run_id, user_id, chest_index, item_name, rarity,
                        salvage_value_gold, created_at)
                       VALUES (?, ?, 1, 'Baú raro', 'rare', 75, 'test')""",
                    (run_id, user_id),
                )
                db.commit()

            with closing(sqlite3.connect(database_path)) as db:
                db.execute("PRAGMA foreign_keys = ON")
                db.execute(
                    "ALTER TABLE users RENAME COLUMN wallet_gold TO wallet_cents"
                )
                db.execute(
                    "ALTER TABLE mission_runs RENAME COLUMN monster_gold TO monster_money_cents"
                )
                db.execute(
                    "ALTER TABLE mission_runs RENAME COLUMN phase_bonus_gold TO phase_bonus_cents"
                )
                db.execute(
                    "ALTER TABLE gold_ledger RENAME COLUMN amount_gold TO amount_cents"
                )
                db.execute("ALTER TABLE gold_ledger RENAME TO wallet_ledger")
                db.execute(
                    "ALTER TABLE inventory_items RENAME COLUMN salvage_value_gold TO salvage_value_cents"
                )
                db.execute(
                    "ALTER TABLE staging_inventory RENAME COLUMN salvage_value_gold TO salvage_value_cents"
                )
                db.commit()

            init_db(app)

            with app.app_context():
                db = get_db()
                user_balance = db.execute(
                    "SELECT wallet_gold FROM users WHERE id = ?", (user_id,)
                ).fetchone()[0]
                run = db.execute(
                    """SELECT monster_gold, phase_bonus_gold FROM mission_runs
                       WHERE id = ?""",
                    (run_id,),
                ).fetchone()
                ledger_amount = db.execute(
                    "SELECT amount_gold FROM gold_ledger WHERE source_key = 'migration-test'"
                ).fetchone()[0]
                inventory_value = db.execute(
                    "SELECT salvage_value_gold FROM inventory_items WHERE user_id = ?",
                    (user_id,),
                ).fetchone()[0]
                staging_value = db.execute(
                    "SELECT salvage_value_gold FROM staging_inventory WHERE user_id = ?",
                    (user_id,),
                ).fetchone()[0]
                tables = {
                    row["name"]
                    for row in db.execute(
                        "SELECT name FROM sqlite_master WHERE type = 'table'"
                    )
                }

        self.assertEqual(user_balance, 12345)
        self.assertEqual(tuple(run), (25, 50))
        self.assertEqual(ledger_amount, 50)
        self.assertEqual(inventory_value, 25)
        self.assertEqual(staging_value, 75)
        self.assertIn("gold_ledger", tables)
        self.assertNotIn("wallet_ledger", tables)

    def test_characters_past_season_one_are_marked_complete_without_resetting_progress(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            database_path = Path(temporary_directory) / "campaign.sqlite3"
            app = Flask(__name__)
            app.config["DATABASE"] = str(database_path)
            app.teardown_appcontext(close_db)

            init_db(app)
            with app.app_context():
                db = get_db()
                db.execute(
                    """INSERT INTO users (username, password_hash, created_at)
                       VALUES (?, ?, ?)""",
                    ("campaign-tester", "not-a-real-password-hash", "test"),
                )
                user_id = db.execute(
                    "SELECT id FROM users WHERE username = ?",
                    ("campaign-tester",),
                ).fetchone()["id"]
                db.execute(
                    """INSERT INTO characters
                       (user_id, name, name_key, class_id, level, experience,
                        current_phase, current_wave, legacy_points, created_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        user_id, "Campanha antiga", "campanha-antiga", "guardian",
                        170, 321, 31, 4, 26, "test",
                    ),
                )
                db.commit()

            init_db(app)
            with app.app_context():
                character = get_db().execute(
                    """SELECT level, experience, current_phase, current_wave,
                              legacy_points, campaign_complete
                       FROM characters WHERE name = ?""",
                    ("Campanha antiga",),
                ).fetchone()

        self.assertEqual(tuple(character), (170, 321, 31, 4, 26, 1))


if __name__ == "__main__":
    unittest.main()
