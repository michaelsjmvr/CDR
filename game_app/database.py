"""SQLite connection helpers and the prototype account/character schema."""

import sqlite3

from flask import current_app, g


def _rename_legacy_column(
    db: sqlite3.Connection, table: str, old_name: str, new_name: str
) -> None:
    columns = {
        column["name"] for column in db.execute(f"PRAGMA table_info({table})")
    }
    if old_name in columns and new_name not in columns:
        db.execute(f"ALTER TABLE {table} RENAME COLUMN {old_name} TO {new_name}")


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        connection = sqlite3.connect(current_app.config["DATABASE"], timeout=15)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA busy_timeout = 15000")
        connection.execute("PRAGMA foreign_keys = ON")
        g.db = connection
    return g.db


def close_db(_error: BaseException | None = None) -> None:
    connection = g.pop("db", None)
    if connection is not None:
        connection.close()


def init_db(app) -> None:
    with app.app_context():
        db = get_db()
        db.execute("PRAGMA journal_mode = WAL")
        db.execute("PRAGMA synchronous = NORMAL")
        db.execute(
            """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL COLLATE NOCASE UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL,
                is_premium INTEGER NOT NULL DEFAULT 0,
                wallet_gold INTEGER NOT NULL DEFAULT 0 CHECK(wallet_gold >= 0)
            )"""
        )
        user_columns = {
            column["name"] for column in db.execute("PRAGMA table_info(users)").fetchall()
        }
        if "is_premium" not in user_columns:
            db.execute(
                "ALTER TABLE users ADD COLUMN is_premium INTEGER NOT NULL DEFAULT 0"
            )
        if "wallet_gold" not in user_columns:
            if "wallet_cents" in user_columns:
                db.execute(
                    "ALTER TABLE users RENAME COLUMN wallet_cents TO wallet_gold"
                )
            else:
                db.execute(
                    "ALTER TABLE users ADD COLUMN wallet_gold INTEGER NOT NULL DEFAULT 0 CHECK(wallet_gold >= 0)"
                )
            user_columns = {
                column["name"]
                for column in db.execute("PRAGMA table_info(users)").fetchall()
            }
        user_option_migrations = {
            "control_scheme": "TEXT NOT NULL DEFAULT 'mouse_keyboard'",
            "mouse_left_slot": "INTEGER NOT NULL DEFAULT 2",
            "mouse_right_slot": "INTEGER NOT NULL DEFAULT 2",
            "skill_slot_1": "TEXT NOT NULL DEFAULT 'basic'",
            "skill_slot_2": "TEXT NOT NULL DEFAULT 'rune_slash'",
            "skill_slot_3": "TEXT NOT NULL DEFAULT ''",
            "skill_slot_4": "TEXT NOT NULL DEFAULT ''",
            "control_options_version": "INTEGER NOT NULL DEFAULT 0",
        }
        for column_name, column_definition in user_option_migrations.items():
            if column_name not in user_columns:
                db.execute(
                    f"ALTER TABLE users ADD COLUMN {column_name} {column_definition}"
                )
        # Convert the old freely-mapped actions once into fixed key 1 plus
        # three spell slots. The version marker keeps later user remaps intact.
        for user in db.execute(
            """SELECT id, skill_slot_1, skill_slot_2, skill_slot_3, skill_slot_4,
                      mouse_left_slot, mouse_right_slot, control_options_version
               FROM users"""
        ).fetchall():
            if user["control_options_version"] >= 1:
                continue
            old_slots = [user[f"skill_slot_{index}"] for index in range(1, 5)]
            spells = []
            for action in old_slots:
                if action and action != "basic" and action not in spells:
                    spells.append(action)
            new_slots = ["basic", *(spells[:3])]
            new_slots.extend([""] * (4 - len(new_slots)))

            def remap_mouse_slot(old_slot):
                try:
                    slot_number = int(old_slot)
                except (TypeError, ValueError):
                    return 2
                if slot_number not in range(1, 5):
                    return 2
                old_action = old_slots[slot_number - 1]
                if old_action in spells[:3]:
                    return spells.index(old_action) + 2
                if old_action != "basic" and slot_number in range(2, 5):
                    return slot_number
                return 2

            left_slot = remap_mouse_slot(user["mouse_left_slot"])
            right_slot = remap_mouse_slot(user["mouse_right_slot"])
            db.execute(
                """UPDATE users SET skill_slot_1 = ?, skill_slot_2 = ?,
                   skill_slot_3 = ?, skill_slot_4 = ?, mouse_left_slot = ?,
                   mouse_right_slot = ?, control_options_version = 1 WHERE id = ?""",
                (*new_slots, left_slot, right_slot, user["id"]),
            )
        db.execute(
            """CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                name TEXT NOT NULL,
                name_key TEXT NOT NULL UNIQUE,
                class_id TEXT NOT NULL,
                specialization_id TEXT,
                talent_root_id TEXT,
                level INTEGER NOT NULL DEFAULT 1 CHECK(level >= 1),
                experience INTEGER NOT NULL DEFAULT 0 CHECK(experience >= 0),
                resets INTEGER NOT NULL DEFAULT 0 CHECK(resets >= 0),
                current_phase INTEGER NOT NULL DEFAULT 1 CHECK(current_phase >= 1),
                current_wave INTEGER NOT NULL DEFAULT 1 CHECK(current_wave >= 1),
                current_difficulty TEXT NOT NULL DEFAULT 'risk_low',
                gold INTEGER NOT NULL DEFAULT 0 CHECK(gold >= 0),
                legacy_points INTEGER NOT NULL DEFAULT 0 CHECK(legacy_points >= 0),
                card_experience INTEGER NOT NULL DEFAULT 0 CHECK(card_experience >= 0),
                pending_card_choices INTEGER NOT NULL DEFAULT 0 CHECK(pending_card_choices >= 0),
                card_offer_revision INTEGER NOT NULL DEFAULT 0 CHECK(card_offer_revision >= 0),
                current_health INTEGER NOT NULL DEFAULT 100 CHECK(current_health >= 0),
                current_mana INTEGER NOT NULL DEFAULT 60 CHECK(current_mana >= 0),
                phase_preparation_until REAL NOT NULL DEFAULT 0,
                phase_xp_budget INTEGER NOT NULL DEFAULT 0 CHECK(phase_xp_budget >= 0),
                phase_intermission INTEGER NOT NULL DEFAULT 0 CHECK(phase_intermission IN (0, 1)),
                death_intermission INTEGER NOT NULL DEFAULT 0 CHECK(death_intermission IN (0, 1)),
                campaign_complete INTEGER NOT NULL DEFAULT 0 CHECK(campaign_complete IN (0, 1)),
                agility INTEGER NOT NULL DEFAULT 0 CHECK(agility >= 0),
                strength INTEGER NOT NULL DEFAULT 0 CHECK(strength >= 0),
                vitality INTEGER NOT NULL DEFAULT 0 CHECK(vitality >= 0),
                energy INTEGER NOT NULL DEFAULT 0 CHECK(energy >= 0),
                attribute_points INTEGER NOT NULL DEFAULT 0 CHECK(attribute_points >= 0),
                auto_allocate_attributes INTEGER NOT NULL DEFAULT 0 CHECK(auto_allocate_attributes IN (0, 1)),
                auto_health_potion INTEGER NOT NULL DEFAULT 0 CHECK(auto_health_potion IN (0, 1)),
                auto_mana_potion INTEGER NOT NULL DEFAULT 0 CHECK(auto_mana_potion IN (0, 1)),
                health_potion_ready_at REAL NOT NULL DEFAULT 0,
                mana_potion_ready_at REAL NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            )"""
        )
        character_columns = {
            column["name"]
            for column in db.execute("PRAGMA table_info(characters)").fetchall()
        }
        character_migrations = {
            "specialization_id": "TEXT",
            "talent_root_id": "TEXT",
            "experience": "INTEGER NOT NULL DEFAULT 0 CHECK(experience >= 0)",
            "resets": "INTEGER NOT NULL DEFAULT 0 CHECK(resets >= 0)",
            "current_phase": "INTEGER NOT NULL DEFAULT 1 CHECK(current_phase >= 1)",
            "current_wave": "INTEGER NOT NULL DEFAULT 1 CHECK(current_wave >= 1)",
            "current_difficulty": "TEXT NOT NULL DEFAULT 'risk_low'",
            "gold": "INTEGER NOT NULL DEFAULT 0 CHECK(gold >= 0)",
            "legacy_points": "INTEGER NOT NULL DEFAULT 0 CHECK(legacy_points >= 0)",
            "card_experience": "INTEGER NOT NULL DEFAULT 0 CHECK(card_experience >= 0)",
            "pending_card_choices": "INTEGER NOT NULL DEFAULT 0 CHECK(pending_card_choices >= 0)",
            "card_offer_revision": "INTEGER NOT NULL DEFAULT 0 CHECK(card_offer_revision >= 0)",
            "current_health": "INTEGER NOT NULL DEFAULT 100 CHECK(current_health >= 0)",
            "current_mana": "INTEGER NOT NULL DEFAULT 60 CHECK(current_mana >= 0)",
            "phase_preparation_until": "REAL NOT NULL DEFAULT 0",
            "phase_xp_budget": "INTEGER NOT NULL DEFAULT 0 CHECK(phase_xp_budget >= 0)",
            "phase_intermission": "INTEGER NOT NULL DEFAULT 0 CHECK(phase_intermission IN (0, 1))",
            "death_intermission": "INTEGER NOT NULL DEFAULT 0 CHECK(death_intermission IN (0, 1))",
            "campaign_complete": "INTEGER NOT NULL DEFAULT 0 CHECK(campaign_complete IN (0, 1))",
            "agility": "INTEGER NOT NULL DEFAULT 0 CHECK(agility >= 0)",
            "strength": "INTEGER NOT NULL DEFAULT 0 CHECK(strength >= 0)",
            "vitality": "INTEGER NOT NULL DEFAULT 0 CHECK(vitality >= 0)",
            "energy": "INTEGER NOT NULL DEFAULT 0 CHECK(energy >= 0)",
            "attribute_points": "INTEGER NOT NULL DEFAULT 0 CHECK(attribute_points >= 0)",
            "auto_allocate_attributes": "INTEGER NOT NULL DEFAULT 0 CHECK(auto_allocate_attributes IN (0, 1))",
            "auto_health_potion": "INTEGER NOT NULL DEFAULT 0 CHECK(auto_health_potion IN (0, 1))",
            "auto_mana_potion": "INTEGER NOT NULL DEFAULT 0 CHECK(auto_mana_potion IN (0, 1))",
            "health_potion_ready_at": "REAL NOT NULL DEFAULT 0",
            "mana_potion_ready_at": "REAL NOT NULL DEFAULT 0",
        }
        # Keep the old counter only to credit characters' legacy Reset points.
        for column_name, column_definition in character_migrations.items():
            if column_name not in character_columns:
                db.execute(
                    f"ALTER TABLE characters ADD COLUMN {column_name} {column_definition}"
                )
        db.execute(
            """UPDATE characters SET campaign_complete = 1
               WHERE current_phase > 30 AND campaign_complete = 0"""
        )
        db.execute(
            """UPDATE characters
               SET legacy_points = MAX(
                   legacy_points,
                   resets + CAST(level / 10 AS INTEGER)
                       + CAST(level / 50 AS INTEGER)
                       + CAST(level / 25 AS INTEGER)
               )"""
        )
        db.execute(
            """CREATE TABLE IF NOT EXISTS mission_progress (
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                difficulty TEXT NOT NULL CHECK(difficulty IN (
                    'risk_low', 'risk_moderate', 'risk_high', 'risk_extreme'
                )),
                phase INTEGER NOT NULL CHECK(phase BETWEEN 1 AND 30),
                completed_at TEXT NOT NULL,
                best_time_seconds REAL,
                completion_count INTEGER NOT NULL DEFAULT 1 CHECK(completion_count > 0),
                PRIMARY KEY(user_id, difficulty, phase)
            )"""
        )
        db.execute(
            """CREATE TABLE IF NOT EXISTS mission_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                character_id INTEGER NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
                difficulty TEXT NOT NULL CHECK(difficulty IN (
                    'risk_low', 'risk_moderate', 'risk_high', 'risk_extreme'
                )),
                phase INTEGER NOT NULL CHECK(phase BETWEEN 1 AND 30),
                start_time REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'active' CHECK(status IN (
                    'active', 'completed', 'failed', 'abandoned'
                )),
                monster_gold INTEGER NOT NULL DEFAULT 0 CHECK(monster_gold >= 0),
                phase_bonus_gold INTEGER NOT NULL DEFAULT 0 CHECK(phase_bonus_gold >= 0),
                completion_time_seconds REAL,
                chest_count INTEGER NOT NULL DEFAULT 0 CHECK(chest_count >= 0),
                created_at TEXT NOT NULL,
                completed_at TEXT
            )"""
        )
        _rename_legacy_column(db, "mission_runs", "monster_money_cents", "monster_gold")
        _rename_legacy_column(db, "mission_runs", "phase_bonus_cents", "phase_bonus_gold")
        db.execute(
            """CREATE INDEX IF NOT EXISTS idx_mission_runs_active
               ON mission_runs(character_id, status, id DESC)"""
        )
        db.execute(
            """CREATE INDEX IF NOT EXISTS idx_mission_runs_active_user
               ON mission_runs(user_id, status, id DESC)"""
        )
        ledger_tables = {
            row["name"]
            for row in db.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }
        if "wallet_ledger" in ledger_tables and "gold_ledger" in ledger_tables:
            raise RuntimeError("Both legacy wallet and Ouro ledgers exist.")
        if "wallet_ledger" in ledger_tables:
            db.execute("ALTER TABLE wallet_ledger RENAME TO gold_ledger")
        db.execute(
            """CREATE TABLE IF NOT EXISTS gold_ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                mission_run_id INTEGER REFERENCES mission_runs(id) ON DELETE SET NULL,
                source_key TEXT NOT NULL,
                transaction_type TEXT NOT NULL CHECK(transaction_type IN (
                    'monster_drop', 'phase_bonus', 'item_sale'
                )),
                amount_gold INTEGER NOT NULL CHECK(amount_gold > 0),
                created_at TEXT NOT NULL,
                UNIQUE(user_id, source_key)
            )"""
        )
        _rename_legacy_column(db, "gold_ledger", "amount_cents", "amount_gold")
        db.execute(
            """CREATE TABLE IF NOT EXISTS inventory_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                item_name TEXT NOT NULL,
                rarity TEXT NOT NULL CHECK(rarity IN (
                    'common', 'rare', 'epic', 'legendary'
                )),
                salvage_value_gold INTEGER NOT NULL CHECK(salvage_value_gold >= 0),
                obtained_from_run_id INTEGER REFERENCES mission_runs(id) ON DELETE SET NULL,
                created_at TEXT NOT NULL
            )"""
        )
        _rename_legacy_column(
            db, "inventory_items", "salvage_value_cents", "salvage_value_gold"
        )
        db.execute(
            """CREATE TABLE IF NOT EXISTS staging_inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mission_run_id INTEGER NOT NULL REFERENCES mission_runs(id) ON DELETE CASCADE,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                chest_index INTEGER NOT NULL CHECK(chest_index > 0),
                item_name TEXT NOT NULL,
                rarity TEXT NOT NULL CHECK(rarity IN (
                    'common', 'rare', 'epic', 'legendary'
                )),
                salvage_value_gold INTEGER NOT NULL CHECK(salvage_value_gold >= 0),
                status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN (
                    'pending', 'claimed', 'discarded'
                )),
                inventory_item_id INTEGER REFERENCES inventory_items(id) ON DELETE SET NULL,
                created_at TEXT NOT NULL,
                UNIQUE(mission_run_id, chest_index)
            )"""
        )
        _rename_legacy_column(
            db, "staging_inventory", "salvage_value_cents", "salvage_value_gold"
        )
        db.execute(
            """CREATE INDEX IF NOT EXISTS idx_staging_inventory_pending
               ON staging_inventory(user_id, status, mission_run_id)"""
        )
        for existing_character in db.execute(
            """SELECT user_id, current_phase, campaign_complete
               FROM characters"""
        ).fetchall():
            completed_through = min(
                30,
                existing_character["current_phase"]
                if existing_character["campaign_complete"]
                else existing_character["current_phase"] - 1,
            )
            for phase in range(1, completed_through + 1):
                db.execute(
                    """INSERT OR IGNORE INTO mission_progress
                       (user_id, difficulty, phase, completed_at)
                       VALUES (?, 'risk_low', ?, CURRENT_TIMESTAMP)""",
                    (existing_character["user_id"], phase),
                )
        if "strength" not in character_columns:
            from .classes import CLASSES

            for class_id, class_info in CLASSES.items():
                base = class_info["base_attributes"]
                db.execute(
                    """UPDATE characters SET strength = ?, agility = MAX(agility, ?),
                       vitality = ?, energy = ? WHERE class_id = ?""",
                    (base["strength"], base["agility"], base["vitality"], base["energy"], class_id),
                )
        db.execute(
            """CREATE TABLE IF NOT EXISTS temporary_upgrades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                character_id INTEGER NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
                upgrade_key TEXT NOT NULL,
                stacks INTEGER NOT NULL DEFAULT 1 CHECK(stacks > 0),
                UNIQUE(character_id, upgrade_key)
            )"""
        )
        db.execute(
            """CREATE TABLE IF NOT EXISTS card_offers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                character_id INTEGER NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
                phase INTEGER NOT NULL CHECK(phase >= 1),
                wave INTEGER NOT NULL CHECK(wave >= 1),
                card_ids TEXT NOT NULL,
                recommended_card_id TEXT,
                auto_pick_at REAL,
                auto_pick_version INTEGER NOT NULL DEFAULT 0,
                selected_card_id TEXT,
                resolved INTEGER NOT NULL DEFAULT 0 CHECK(resolved IN (0, 1)),
                created_at TEXT NOT NULL,
                UNIQUE(character_id, phase, wave)
            )"""
        )
        db.execute(
            """CREATE TABLE IF NOT EXISTS card_offer_history (
                character_id INTEGER NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
                phase INTEGER NOT NULL CHECK(phase >= 1),
                wave INTEGER NOT NULL CHECK(wave >= 1),
                card_id TEXT NOT NULL,
                PRIMARY KEY(character_id, phase, wave, card_id)
            )"""
        )
        offer_columns = {
            column["name"]
            for column in db.execute("PRAGMA table_info(card_offers)").fetchall()
        }
        if "recommended_card_id" not in offer_columns:
            db.execute("ALTER TABLE card_offers ADD COLUMN recommended_card_id TEXT")
        if "auto_pick_at" not in offer_columns:
            db.execute("ALTER TABLE card_offers ADD COLUMN auto_pick_at REAL")
        if "auto_pick_version" not in offer_columns:
            db.execute("ALTER TABLE card_offers ADD COLUMN auto_pick_version INTEGER NOT NULL DEFAULT 0")
        db.execute(
            """UPDATE characters
               SET card_offer_revision = COALESCE(
                   (SELECT MAX(id) FROM card_offers WHERE character_id = characters.id), 0
               )
               WHERE card_offer_revision = 0"""
        )
        db.execute(
            """CREATE TABLE IF NOT EXISTS character_talents (
                character_id INTEGER NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
                talent_id TEXT NOT NULL,
                purchased_at TEXT NOT NULL,
                PRIMARY KEY(character_id, talent_id)
            )"""
        )
        db.execute(
            """CREATE TABLE IF NOT EXISTS card_xp_orbs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                character_id INTEGER NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
                phase INTEGER NOT NULL CHECK(phase >= 1),
                wave INTEGER NOT NULL CHECK(wave >= 1),
                world_x REAL NOT NULL,
                world_y REAL NOT NULL,
                xp_value INTEGER NOT NULL CHECK(xp_value > 0),
                collected INTEGER NOT NULL DEFAULT 0 CHECK(collected IN (0, 1)),
                source_key TEXT NOT NULL DEFAULT 'legacy'
            )"""
        )
        orb_schema = db.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='card_xp_orbs'").fetchone()[0]
        if "UNIQUE(character_id,phase,wave)" in orb_schema.replace(" ", ""):
            db.execute("ALTER TABLE card_xp_orbs RENAME TO card_xp_orbs_legacy")
            db.execute("""CREATE TABLE card_xp_orbs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                character_id INTEGER NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
                phase INTEGER NOT NULL CHECK(phase >= 1), wave INTEGER NOT NULL CHECK(wave >= 1),
                world_x REAL NOT NULL, world_y REAL NOT NULL,
                xp_value INTEGER NOT NULL CHECK(xp_value > 0),
                collected INTEGER NOT NULL DEFAULT 0 CHECK(collected IN (0, 1)),
                source_key TEXT NOT NULL DEFAULT 'legacy')""")
            db.execute("""INSERT INTO card_xp_orbs(id, character_id, phase, wave, world_x, world_y, xp_value, collected, source_key)
                SELECT id, character_id, phase, wave, world_x, world_y, xp_value, collected,
                       printf('legacy:%d:%d:%d', character_id, phase, wave) FROM card_xp_orbs_legacy""")
            db.execute("DROP TABLE card_xp_orbs_legacy")
        db.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_card_xp_orb_source ON card_xp_orbs(character_id, source_key)")
        # These rows came from the former wave-completion test drop, not from a monster death.
        db.execute("DELETE FROM card_xp_orbs WHERE source_key LIKE 'wave:%' OR source_key LIKE 'legacy:%'")
        db.execute(
            """CREATE TABLE IF NOT EXISTS wave_enemies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                character_id INTEGER NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
                phase INTEGER NOT NULL,
                wave INTEGER NOT NULL,
                enemy_index INTEGER NOT NULL,
                world_x REAL NOT NULL,
                world_y REAL NOT NULL,
                hp INTEGER NOT NULL,
                max_hp INTEGER NOT NULL,
                experience_reward INTEGER NOT NULL,
                alive INTEGER NOT NULL DEFAULT 1 CHECK(alive IN (0, 1)),
                UNIQUE(character_id, phase, wave, enemy_index)
            )"""
        )
        db.execute(
            """CREATE TABLE IF NOT EXISTS account_stashes (
                user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
                created_at TEXT NOT NULL
            )"""
        )
        db.commit()
