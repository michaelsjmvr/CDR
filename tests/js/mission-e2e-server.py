"""Temporary authenticated Flask server for browser-level mission tests."""

import argparse
import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from game_app import create_app
from game_app.database import get_db
from game_app.extensions import socketio
from game_app.mission_system import DIFFICULTY_ORDER


def seed_scenario(app, mode: str, difficulty: str | None) -> tuple[int, int]:
    with app.app_context():
        db = get_db()
        db.execute(
            """INSERT INTO users
               (username, password_hash, created_at, control_scheme)
               VALUES ('mission-e2e', 'unused', 'test', 'keyboard_only')"""
        )
        user_id = db.execute(
            "SELECT id FROM users WHERE username = 'mission-e2e'"
        ).fetchone()["id"]
        db.execute(
            """INSERT INTO characters
               (user_id, name, name_key, class_id, created_at)
               VALUES (?, 'E2E Tester', 'mission-e2e-character', 'guardian', 'test')""",
            (user_id,),
        )
        character_id = db.execute(
            "SELECT id FROM characters WHERE name_key = 'mission-e2e-character'"
        ).fetchone()["id"]

        if mode in {"mission", "full_mission"}:
            difficulty_index = DIFFICULTY_ORDER.index(difficulty)
            for previous_difficulty in DIFFICULTY_ORDER[:difficulty_index]:
                db.executemany(
                    """INSERT INTO mission_progress
                       (user_id, difficulty, phase, completed_at)
                       VALUES (?, ?, ?, 'test')""",
                    [
                        (user_id, previous_difficulty, phase)
                        for phase in range(1, 31)
                    ],
                )
            if mode == "full_mission":
                db.executemany(
                    """INSERT INTO mission_progress
                       (user_id, difficulty, phase, completed_at)
                       VALUES (?, ?, ?, 'test')""",
                    [
                        (user_id, difficulty, phase)
                        for phase in range(1, 10)
                    ],
                )
                db.execute(
                    """UPDATE characters
                       SET level = 400, strength = 10000, agility = 10000,
                           vitality = 10000, energy = 10000
                       WHERE id = ?""",
                    (character_id,),
                )
        else:
            run = db.execute(
                """INSERT INTO mission_runs
                   (user_id, character_id, difficulty, phase, start_time,
                    status, completion_time_seconds, chest_count, created_at)
                   VALUES (?, ?, 'risk_low', 1, 100, 'completed', 65, 1, 'test')""",
                (user_id, character_id),
            )
            db.execute(
                """INSERT INTO staging_inventory
                   (mission_run_id, user_id, chest_index, item_name, rarity,
                    salvage_value_gold, status, created_at)
                   VALUES (?, ?, 1, 'Baú E2E', 'rare', 75, 'pending', 'test')""",
                (run.lastrowid, user_id),
            )
            db.executemany(
                """INSERT INTO inventory_items
                   (user_id, item_name, rarity, salvage_value_gold, created_at)
                   VALUES (?, ?, 'common', 25, 'test')""",
                [
                    (user_id, f"Item ocupado {index}")
                    for index in range(30)
                ],
            )
        db.commit()
        return user_id, character_id


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("mission", "full_mission", "inventory"),
        required=True,
    )
    parser.add_argument("--difficulty", choices=DIFFICULTY_ORDER)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--database", required=True)
    parser.add_argument("--session-cookie", required=True)
    args = parser.parse_args()
    if args.mode in {"mission", "full_mission"} and args.difficulty is None:
        parser.error("--difficulty is required in mission modes")

    os.environ["CRONICAS_DATABASE"] = args.database
    os.environ["CRONICAS_SECRET_KEY"] = "mission-e2e-only-secret"
    os.environ["CRONICAS_ENABLE_PREMIUM_TEST_TOGGLE"] = "0"
    app = create_app()
    user_id, character_id = seed_scenario(app, args.mode, args.difficulty)
    session_serializer = app.session_interface.get_signing_serializer(app)
    cookie_value = session_serializer.dumps(
        {
            "user_id": user_id,
            "selected_character_id": character_id,
            "csrf_token": "mission-e2e-csrf",
            "in_lobby": True,
        }
    )
    Path(args.session_cookie).write_text(
        json.dumps(
            {
                "name": app.config["SESSION_COOKIE_NAME"],
                "value": cookie_value,
            }
        ),
        encoding="utf-8",
    )
    print("READY", flush=True)
    socketio.run(
        app,
        host="127.0.0.1",
        port=args.port,
        use_reloader=False,
        allow_unsafe_werkzeug=True,
        log_output=False,
    )


if __name__ == "__main__":
    main()
