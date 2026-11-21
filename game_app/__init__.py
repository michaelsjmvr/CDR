"""Flask application factory and shared request setup."""

import os
import secrets
from pathlib import Path

from flask import Flask, g, session

from .auth import auth_blueprint
from .attributes import attributes_blueprint
from .characters import characters_blueprint
from .database import close_db, get_db, init_db
from .extensions import socketio
from .game import game_blueprint
from .security import csrf_token
from .talent_routes import talents_blueprint
from . import socket_events as _socket_events


def _load_secret_key(instance_path: str) -> str:
    configured_key = os.environ.get("CRONICAS_SECRET_KEY")
    if configured_key:
        return configured_key

    instance_dir = Path(instance_path)
    instance_dir.mkdir(parents=True, exist_ok=True)
    secret_file = instance_dir / "session.key"
    if not secret_file.exists():
        secret_file.write_text(secrets.token_hex(32), encoding="utf-8")
    return secret_file.read_text(encoding="utf-8").strip()


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    app.config.from_mapping(
        SECRET_KEY=_load_secret_key(app.instance_path),
        DATABASE=os.environ.get(
            "CRONICAS_DATABASE",
            str(Path(app.instance_path) / "users.sqlite3"),
        ),
        MAX_CONTENT_LENGTH=16 * 1024,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=os.environ.get("CRONICAS_COOKIE_SECURE", "0") == "1",
        PERMANENT_SESSION_LIFETIME=60 * 60 * 12,
        ENABLE_PREMIUM_TEST_TOGGLE=os.environ.get("CRONICAS_ENABLE_PREMIUM_TEST_TOGGLE", "1") == "1",
    )

    app.jinja_env.globals["csrf_token"] = csrf_token
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(attributes_blueprint)
    app.register_blueprint(characters_blueprint)
    app.register_blueprint(game_blueprint)
    app.register_blueprint(talents_blueprint)
    app.teardown_appcontext(close_db)

    socketio.init_app(app, async_mode="threading")

    @app.before_request
    def load_current_user() -> None:
        user_id = session.get("user_id")
        g.user = None
        if user_id is not None:
            g.user = get_db().execute(
                """SELECT id, username, is_premium, control_scheme,
                          mouse_left_slot, mouse_right_slot,
                          skill_slot_1, skill_slot_2, skill_slot_3, skill_slot_4
                   FROM users WHERE id = ?""",
                (user_id,),
            ).fetchone()
            if g.user is None:
                session.clear()

    init_db(app)
    return app
