"""Protected character attribute allocation for the current progression cycle."""

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from .classes import CLASSES
from .combat import combat_summary as build_combat_summary, derived_combat_stats
from .database import get_db
from .progression import MAX_ATTRIBUTE_VALUE, MAX_LEVEL, experience_needed
from .security import validate_csrf

attributes_blueprint = Blueprint("attributes", __name__)
ATTRIBUTE_LABELS = {
    "strength": "Força",
    "agility": "Agilidade",
    "vitality": "Vitalidade",
    "energy": "Energia",
}


def _character():
    character_id = session.get("selected_character_id")
    if not g.user or character_id is None:
        return None
    return get_db().execute(
        """SELECT id, name, class_id, specialization_id, level, experience,
                  strength, agility, vitality, energy, attribute_points, auto_allocate_attributes,
                  current_health, current_mana FROM characters
           WHERE id = ? AND user_id = ?""",
        (character_id, g.user["id"]),
    ).fetchone()


@attributes_blueprint.route("/jogo/atributos", methods=["GET", "POST"])
def allocate():
    if not g.user:
        flash("Entre na sua conta para distribuir atributos.", "info")
        return redirect(url_for("auth.home"))
    if not session.get("in_lobby"):
        flash("Os atributos só podem ser ajustados na Sala de Espera.", "info")
        return redirect(url_for("game.lobby"))
    character = _character()
    if character is None:
        flash("Selecione um personagem antes de distribuir atributos.", "info")
        return redirect(url_for("characters.index"))

    if request.method == "POST":
        validate_csrf(request.form.get("csrf_token", ""))
        if request.form.get("action") == "toggle_auto":
            if not g.user["is_premium"]:
                flash("A distribuição automática exige o benefício especial.", "error")
                return redirect(url_for("attributes.allocate"))
            enabled = 1 if request.form.get("enabled") == "1" else 0
            db = get_db()
            db.execute(
                "UPDATE characters SET auto_allocate_attributes = ? WHERE id = ? AND user_id = ?",
                (enabled, character["id"], g.user["id"]),
            )
            db.commit()
            flash("Distribuição automática ativada." if enabled else "Distribuição automática desativada.", "success")
            return redirect(url_for("attributes.allocate"))
        attribute = request.form.get("attribute", "")
        try:
            amount = int(request.form.get("amount", "1"))
        except (TypeError, ValueError):
            amount = 0
        if attribute not in ATTRIBUTE_LABELS or amount < 1:
            flash("Selecione um atributo e uma quantidade válida.", "error")
            return redirect(url_for("attributes.allocate"))

        db = get_db()
        db.execute("BEGIN IMMEDIATE")
        current = db.execute(
            """SELECT id, class_id, specialization_id, level, attribute_points, strength, agility,
                      vitality, energy, current_health, current_mana
               FROM characters WHERE id = ? AND user_id = ?""",
            (character["id"], g.user["id"]),
        ).fetchone()
        if current is None:
            db.rollback()
            session.pop("selected_character_id", None)
            flash("Selecione um personagem válido.", "error")
            return redirect(url_for("characters.index"))
        if amount > current["attribute_points"]:
            db.rollback()
            flash("Você não possui pontos livres suficientes.", "error")
            return redirect(url_for("attributes.allocate"))
        if current[attribute] + amount > MAX_ATTRIBUTE_VALUE:
            db.rollback()
            flash(f"{ATTRIBUTE_LABELS[attribute]} atingiu o limite de {MAX_ATTRIBUTE_VALUE}.", "error")
            return redirect(url_for("attributes.allocate"))

        active_card_ids = {
            row["upgrade_key"] for row in db.execute(
                "SELECT upgrade_key FROM temporary_upgrades WHERE character_id = ?",
                (character["id"],),
            ).fetchall()
        }
        purchased_talents = {
            row["talent_id"] for row in db.execute(
                "SELECT talent_id FROM character_talents WHERE character_id = ?",
                (character["id"],),
            ).fetchall()
        }
        old_stats = derived_combat_stats(current, active_card_ids, purchased_talents)
        current_health = min(max(0, current["current_health"]), old_stats["max_health"])
        current_mana = min(max(0, current["current_mana"]), old_stats["max_mana"])
        db.execute(
            f"UPDATE characters SET {attribute} = {attribute} + ?, "
            "attribute_points = attribute_points - ? WHERE id = ? AND user_id = ?",
            (amount, amount, character["id"], g.user["id"]),
        )
        updated = db.execute(
            "SELECT * FROM characters WHERE id = ? AND user_id = ?",
            (character["id"], g.user["id"]),
        ).fetchone()
        new_stats = derived_combat_stats(updated, active_card_ids, purchased_talents)
        health = min(
            new_stats["max_health"],
            current_health + max(0, new_stats["max_health"] - old_stats["max_health"]),
        )
        mana = min(
            new_stats["max_mana"],
            current_mana + max(0, new_stats["max_mana"] - old_stats["max_mana"]),
        )
        db.execute(
            "UPDATE characters SET current_health = ?, current_mana = ? WHERE id = ?",
            (health, mana, character["id"]),
        )
        db.commit()
        flash(f"{amount} ponto(s) adicionados em {ATTRIBUTE_LABELS[attribute]}.", "success")
        return redirect(url_for("attributes.allocate"))

    class_info = CLASSES[character["class_id"]]
    base = class_info["base_attributes"]
    stats = [
        {"key": key, "label": ATTRIBUTE_LABELS[key], "value": character[key], "base": base[key]}
        for key in ATTRIBUTE_LABELS
    ]
    active_card_ids = {
        row["upgrade_key"] for row in get_db().execute(
            "SELECT upgrade_key FROM temporary_upgrades WHERE character_id = ?",
            (character["id"],),
        ).fetchall()
    }
    purchased_talents = {
        row["talent_id"] for row in get_db().execute(
            "SELECT talent_id FROM character_talents WHERE character_id = ?",
            (character["id"],),
        ).fetchall()
    }
    combat_summary = build_combat_summary(
        character, active_card_ids, purchased_talents
    )
    xp_to_next_level = (
        max(0, experience_needed(character["level"]) - character["experience"])
        if character["level"] < MAX_LEVEL else None
    )
    return render_template("attributes.html", character=character, class_info=class_info, stats=stats,
                           max_attribute=MAX_ATTRIBUTE_VALUE,
                           combat_summary=combat_summary,
                           xp_to_next_level=xp_to_next_level,
                           max_level=MAX_LEVEL,
                           is_premium=bool(g.user["is_premium"]))
