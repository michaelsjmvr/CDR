"""Account character selection, creation, play, and deletion routes."""

import sqlite3
import unicodedata
from datetime import datetime, timezone

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from .classes import CLASSES
from .combat import derived_combat_stats
from .database import get_db
from .security import validate_csrf


characters_blueprint = Blueprint("characters", __name__)
FREE_CHARACTER_LIMIT = 4
PREMIUM_CHARACTER_LIMIT = 6
MIN_CHARACTER_NAME_LENGTH = 3
MAX_CHARACTER_NAME_LENGTH = 20


def _owned_character(character_id: int):
    return get_db().execute(
        """SELECT id, user_id, name, class_id, level
           FROM characters WHERE id = ? AND user_id = ?""",
        (character_id, g.user["id"]),
    ).fetchone()


def _character_limit() -> int:
    return PREMIUM_CHARACTER_LIMIT if g.user["is_premium"] else FREE_CHARACTER_LIMIT


def _character_count() -> int:
    row = get_db().execute(
        "SELECT COUNT(*) AS total FROM characters WHERE user_id = ?",
        (g.user["id"],),
    ).fetchone()
    return row["total"]


def _normalize_name(raw_name: str) -> tuple[str, str] | None:
    display_name = unicodedata.normalize("NFKC", raw_name).strip()
    if not MIN_CHARACTER_NAME_LENGTH <= len(display_name) <= MAX_CHARACTER_NAME_LENGTH:
        return None
    if display_name.startswith((" ", "-", "_")) or display_name.endswith((" ", "-", "_")):
        return None
    if "  " in display_name:
        return None
    if not all(char.isalnum() or char in " _-" for char in display_name):
        return None
    if not any(char.isalpha() for char in display_name):
        return None
    return display_name, display_name.casefold()


@characters_blueprint.get("/personagens")
def index():
    if not g.user:
        flash("Entre na sua conta para escolher um personagem.", "info")
        return redirect(url_for("auth.home"))

    characters = get_db().execute(
        """SELECT id, name, class_id, level
           FROM characters WHERE user_id = ? ORDER BY created_at, id""",
        (g.user["id"],),
    ).fetchall()
    selected_id = session.get("selected_character_id")
    if selected_id not in {character["id"] for character in characters}:
        selected_id = None
        session.pop("selected_character_id", None)
    selected_character = next(
        (character for character in characters if character["id"] == selected_id),
        None,
    )
    character_limit = _character_limit()

    return render_template(
        "characters.html",
        characters=characters,
        classes=CLASSES,
        selected_id=selected_id,
        selected_character=selected_character,
        character_count=len(characters),
        character_limit=character_limit,
        is_premium=bool(g.user["is_premium"]),
        show_create_form=(request.args.get("criar") == "1" and len(characters) < character_limit),
    )


@characters_blueprint.post("/personagens/criar")
def create():
    if not g.user:
        return redirect(url_for("auth.home"))
    validate_csrf(request.form.get("csrf_token", ""))

    name_result = _normalize_name(request.form.get("name", ""))
    class_id = request.form.get("class_id", "")
    if name_result is None:
        flash(
            "Use um nome de 3 a 20 caracteres: letras, números, espaços, hífen ou _.",
            "error",
        )
        return redirect(url_for("characters.index"))
    if class_id not in CLASSES:
        flash("Escolha uma classe válida.", "error")
        return redirect(url_for("characters.index"))

    db = get_db()
    limit = _character_limit()
    db.execute("BEGIN IMMEDIATE")
    current_count = _character_count()
    if current_count >= limit:
        db.rollback()
        flash(f"Sua conta já atingiu o limite de {limit} personagens.", "error")
        return redirect(url_for("characters.index"))

    display_name, name_key = name_result
    base_attributes = CLASSES[class_id]["base_attributes"]
    initial_stats = derived_combat_stats(
        {"class_id": class_id, "level": 1, **base_attributes}
    )
    try:
        cursor = db.execute(
            """INSERT INTO characters
               (user_id, name, name_key, class_id, level,
                strength, agility, vitality, energy, attribute_points,
                current_health, current_mana, created_at)
               VALUES (?, ?, ?, ?, 1, ?, ?, ?, ?, 0, ?, ?, ?)""",
            (
                g.user["id"],
                display_name,
                name_key,
                class_id,
                base_attributes["strength"],
                base_attributes["agility"],
                base_attributes["vitality"],
                base_attributes["energy"],
                initial_stats["max_health"],
                initial_stats["max_mana"],
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        if current_count == 0:
            db.execute(
                "INSERT OR IGNORE INTO account_stashes (user_id, created_at) VALUES (?, ?)",
                (g.user["id"], datetime.now(timezone.utc).isoformat()),
            )
        db.commit()
    except sqlite3.IntegrityError:
        db.rollback()
        flash("Esse nome de personagem já está em uso. Escolha outro.", "error")
        return redirect(url_for("characters.index"))

    session["selected_character_id"] = cursor.lastrowid
    flash(f"{display_name} foi criado.", "success")
    return redirect(url_for("characters.index"))


@characters_blueprint.post("/personagens/<int:character_id>/selecionar")
def select(character_id: int):
    if not g.user:
        return redirect(url_for("auth.home"))
    validate_csrf(request.form.get("csrf_token", ""))
    character = _owned_character(character_id)
    if character is None:
        flash("Esse personagem não pertence à sua conta.", "error")
        return redirect(url_for("characters.index"))

    session["selected_character_id"] = character["id"]
    return redirect(url_for("characters.index"))


@characters_blueprint.post("/personagens/jogar")
def play():
    if not g.user:
        return redirect(url_for("auth.home"))
    validate_csrf(request.form.get("csrf_token", ""))
    selected_id = session.get("selected_character_id")
    if selected_id is None or _owned_character(selected_id) is None:
        flash("Selecione um personagem antes de jogar.", "error")
        return redirect(url_for("characters.index"))
    return redirect(url_for("game.lobby"))


@characters_blueprint.route(
    "/personagens/<int:character_id>/deletar", methods=["GET", "POST"]
)
def delete(character_id: int):
    if not g.user:
        return redirect(url_for("auth.home"))
    character = _owned_character(character_id)
    if character is None:
        flash("Esse personagem não pertence à sua conta.", "error")
        return redirect(url_for("characters.index"))

    db = get_db()
    if request.method == "GET":
        is_last_character = _character_count() == 1
        return render_template(
            "delete_character.html",
            character=character,
            class_info=CLASSES[character["class_id"]],
            is_last_character=is_last_character,
        )

    validate_csrf(request.form.get("csrf_token", ""))
    db.execute("BEGIN IMMEDIATE")
    character = _owned_character(character_id)
    if character is None:
        db.rollback()
        flash("Esse personagem não pertence à sua conta.", "error")
        return redirect(url_for("characters.index"))
    is_last_character = _character_count() == 1
    previously_confirmed_last = request.form.get("is_last_character") == "1"
    if previously_confirmed_last != is_last_character:
        db.rollback()
        return render_template(
            "delete_character.html",
            character=character,
            class_info=CLASSES[character["class_id"]],
            is_last_character=is_last_character,
        ), 409

    db.execute(
        "DELETE FROM characters WHERE id = ? AND user_id = ?",
        (character_id, g.user["id"]),
    )
    if is_last_character:
        db.execute("DELETE FROM account_stashes WHERE user_id = ?", (g.user["id"],))
    db.commit()

    if session.get("selected_character_id") == character_id:
        session.pop("selected_character_id", None)
    if is_last_character:
        flash(
            f"{character['name']} e o Baú da Conta foram deletados. "
            "Você ainda pode criar um novo personagem.",
            "success",
        )
    else:
        flash(f"{character['name']} e os dados vinculados foram deletados.", "success")
    return redirect(url_for("characters.index"))
