"""Registration, login, and logout routes."""

import re
import secrets
import sqlite3
from datetime import datetime, timezone

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from .database import get_db
from .security import validate_csrf
from .extensions import socketio


auth_blueprint = Blueprint("auth", __name__)


def _render_auth(mode: str, *, username: str = "", error: str | None = None):
    return render_template("auth.html", mode=mode, username=username, error=error)


@auth_blueprint.get("/")
def home():
    if g.user:
        return redirect(url_for("characters.index"))
    return _render_auth("login")


@auth_blueprint.route("/cadastro", methods=["GET", "POST"])
def register():
    if g.user:
        return redirect(url_for("characters.index"))
    if request.method == "GET":
        return _render_auth("register")

    validate_csrf(request.form.get("csrf_token", ""))
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    confirmation = request.form.get("password_confirmation", "")

    if not re.fullmatch(r"[A-Za-z0-9_]{3,24}", username):
        return _render_auth(
            "register",
            username=username,
            error="Use um nome de 3 a 24 caracteres: letras, números ou _.",
        ), 400
    if len(password) < 10 or len(password) > 128:
        return _render_auth(
            "register",
            username=username,
            error="A senha precisa ter entre 10 e 128 caracteres.",
        ), 400
    if password != confirmation:
        return _render_auth(
            "register", username=username, error="As senhas não conferem."
        ), 400

    db = get_db()
    try:
        cursor = db.execute(
            "INSERT INTO users (username, password_hash, created_at, control_options_version) VALUES (?, ?, ?, 1)",
            (
                username,
                generate_password_hash(password),
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        db.commit()
        user_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        db.rollback()
        return _render_auth(
            "register",
            username=username,
            error="Esse nome de usuário já está em uso.",
        ), 409

    session.clear()
    session["user_id"] = user_id
    session["csrf_token"] = secrets.token_urlsafe(32)
    session.permanent = True
    flash("Conta criada. Sua jornada começa agora.", "success")
    return redirect(url_for("characters.index"))


@auth_blueprint.post("/login")
def login():
    if g.user:
        return redirect(url_for("characters.index"))
    validate_csrf(request.form.get("csrf_token", ""))
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    user = get_db().execute(
        "SELECT id, username, password_hash FROM users WHERE username = ?", (username,)
    ).fetchone()

    if user is None or not check_password_hash(user["password_hash"], password):
        return _render_auth(
            "login", username=username, error="Usuário ou senha inválidos."
        ), 401

    session.clear()
    session["user_id"] = user["id"]
    session["csrf_token"] = secrets.token_urlsafe(32)
    session.permanent = True
    flash("Acesso realizado. Bem-vindo de volta.", "success")
    return redirect(url_for("characters.index"))


@auth_blueprint.post("/sair")
def logout():
    validate_csrf(request.form.get("csrf_token", ""))
    user_id = session.get("user_id")
    if user_id is not None:
        socketio.emit("auth:logout", {}, to=f"user:{user_id}")
    session.clear()
    flash("Você saiu da sua conta.", "success")
    return redirect(url_for("auth.home"))
