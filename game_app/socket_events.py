"""Authenticated real-time game events for the browser prototype."""

import hmac
import json
import math
import random
import secrets
import sqlite3
import time

from flask import current_app, request, session
from flask_socketio import join_room

from .abilities import (
    CLASS_BASE_SKILLS,
    SKILLS,
    available_class_skills,
    normalized_skill_slots,
)
from .cards import CARDS, card_recommendation_score, draw_card_offer, recommend_card
from .campaign import SEASON_1_PHASES, encounter_type
from .classes import CLASSES
from .combat import (
    BASIC_ATTACK_DAMAGE,
    BASIC_ATTACK_COOLDOWN,
    DASH_COOLDOWN,
    calculate_attack_damage,
    cooldown_for_agility,
    ENEMY_ATTACKS,
    AUTO_POTION_HEALTH_THRESHOLD,
    AUTO_POTION_HEALTH_RESTORE,
    AUTO_POTION_HEALTH_COOLDOWN,
    AUTO_POTION_MANA_THRESHOLD,
    AUTO_POTION_MANA_RESTORE,
    AUTO_POTION_MANA_COOLDOWN,
    PHASE_PREPARATION_SECONDS,
    combat_summary,
    enemy_level,
    enemy_name,
    enemy_attack_style,
    enemy_spawn_positions,
    boss_affinity,
    derived_combat_stats,
    enemy_max_health,
    scale_enemy_attack_damage,
)
from .database import get_db
from .extensions import socketio
from .map_geometry import clamp_map_position, terminal_vilar_collides
from .mission_system import (
    active_mission_run,
    complete_mission,
    credit_gold_monster_drop,
)
from .progression import (
    ATTRIBUTE_POINTS_PER_LEVEL,
    CLASS_AUTO_DISTRIBUTION,
    CARD_XP_PER_ORB,
    CARD_XP_PER_ORB_PREMIUM,
    CARD_AUTO_PICK_SECONDS,
    card_xp_needed,
    MAX_ATTRIBUTE_VALUE,
    MAX_LEVEL,
    WAVES_PER_PHASE,
    enemies_in_wave,
    phase_xp_budget_for_level,
    add_experience,
    award_attribute_points,
    distribute_attribute_points,
    enemy_experience_reward,
    experience_needed,
    award_legacy_points,
    wave_experience_reward,
)

_skill_cooldowns: dict[tuple[int, str], float] = {}
_basic_attack_cooldowns: dict[int, float] = {}
_dash_cooldowns: dict[int, float] = {}
_enemy_attack_cooldowns: dict[tuple[int, int], float] = {}
_pending_enemy_attacks: dict[str, dict] = {}
_pending_player_attacks: dict[str, dict] = {}
_enemy_attack_cycles: dict[tuple[int, int], int] = {}
_card_attack_streaks: dict[int, tuple[int, float]] = {}
_temporary_player_effects: dict[int, dict] = {}
_shadow_summons: dict[int, list[dict]] = {}
_ATTRIBUTE_LABELS = {
    "strength": "Força",
    "agility": "Agilidade",
    "vitality": "Vitalidade",
    "energy": "Energia",
}


def reset_character_combat_state(character_id: int) -> None:
    for cooldowns in (
        _skill_cooldowns,
        _basic_attack_cooldowns,
        _dash_cooldowns,
        _card_attack_streaks,
        _temporary_player_effects,
        _shadow_summons,
    ):
        cooldowns.pop(character_id, None)
    for cooldowns in (_enemy_attack_cooldowns, _enemy_attack_cycles):
        for key in [key for key in cooldowns if key[0] == character_id]:
            cooldowns.pop(key, None)
    for attacks in (_pending_enemy_attacks, _pending_player_attacks):
        for attack_id in [
            attack_id for attack_id, attack in attacks.items()
            if attack.get("character_id") == character_id
        ]:
            attacks.pop(attack_id, None)


def _begin_write(db) -> bool:
    """Wait for SQLite's writer slot and turn a persistent lock into an ACK error."""
    try:
        db.execute("BEGIN IMMEDIATE")
        return True
    except sqlite3.OperationalError as error:
        if "locked" not in str(error).lower():
            raise
        return False


def _room(character_id: int) -> str:
    return f"character:{character_id}"


def _character():
    user_id = session.get("user_id")
    character_id = session.get("selected_character_id")
    if user_id is None or character_id is None:
        return None
    return get_db().execute(
        "SELECT * FROM characters WHERE id = ? AND user_id = ?",
        (character_id, user_id),
    ).fetchone()


def _activate_skill_effect(character_id: int, skill: dict) -> dict | None:
    """Apply temporary defensive effects granted by an active ability."""
    duration = max(0, float(skill.get("effect_duration", 0)))
    reduction = min(.50, max(0, float(skill.get("damage_reduction_bonus", 0))))
    dodge = min(.65, max(0, float(skill.get("dodge_chance_bonus", 0))))
    if not duration or not (reduction or dodge):
        return None
    now = time.monotonic()
    expires_at = now + duration
    effect = _temporary_player_effects.setdefault(character_id, {})
    if effect.get("expires_at", 0) <= now:
        effect.clear()
    effect["expires_at"] = max(effect.get("expires_at", 0), expires_at)
    effect["damage_reduction"] = max(
        effect.get("damage_reduction", 0), reduction
    )
    effect["dodge_chance"] = max(effect.get("dodge_chance", 0), dodge)
    return {
        "kind": skill["effect_kind"],
        "duration": duration,
        "damage_reduction": effect["damage_reduction"],
        "dodge_chance": effect["dodge_chance"],
    }


def _consume_shadow_summons(character_id: int, base_damage: int) -> dict:
    now = time.monotonic()
    soldiers = [
        soldier for soldier in _shadow_summons.get(character_id, [])
        if soldier["expires_at"] > now and soldier["attacks_remaining"] > 0
    ]
    damage = round(
        base_damage * sum(
            soldier["damage_fraction"] for soldier in soldiers
        )
    )
    attacking_count = len(soldiers)
    for soldier in soldiers:
        soldier["attacks_remaining"] -= 1
    soldiers = [
        soldier for soldier in soldiers
        if soldier["attacks_remaining"] > 0
    ]
    if soldiers:
        _shadow_summons[character_id] = soldiers
    else:
        _shadow_summons.pop(character_id, None)
    return {"count": attacking_count, "damage": damage}


def _raise_shadow_soldier(character_id: int, skill: dict, source_name: str) -> int:
    now = time.monotonic()
    soldiers = [
        soldier for soldier in _shadow_summons.get(character_id, [])
        if soldier["expires_at"] > now and soldier["attacks_remaining"] > 0
    ]
    soldiers.append({
        "name": source_name,
        "attacks_remaining": max(1, int(skill.get("summon_attacks", 1))),
        "expires_at": now + max(1, float(skill.get("summon_duration", 1))),
        "damage_fraction": max(0, float(skill.get("summon_damage_fraction", 0))),
    })
    limit = max(1, int(skill.get("summon_limit", 1)))
    _shadow_summons[character_id] = soldiers[-limit:]
    return len(_shadow_summons[character_id])


def _skill_area_targets(db, character, skill, nearby_enemies, target_x, target_y,
                        player_x, player_y, primary_enemy_id):
    """Resolve extra targets from live client positions against this character's wave."""
    effect_kind = skill.get("effect_kind")
    if effect_kind not in {
        "chain", "area_burst", "gravity_well", "repulse", "sanctuary",
    }:
        return []
    if not isinstance(nearby_enemies, list):
        return []
    radius = min(350, max(0, float(skill.get("area_radius", 0))))
    center_x, center_y = (
        (player_x, player_y)
        if effect_kind == "repulse" or skill.get("area_center") == "player"
        else (target_x, target_y)
    )
    candidates = []
    seen = {primary_enemy_id}
    for candidate in nearby_enemies[:64]:
        if not isinstance(candidate, dict):
            continue
        try:
            candidate_id = int(candidate.get("id"))
            x, y = float(candidate.get("x")), float(candidate.get("y"))
        except (TypeError, ValueError):
            continue
        if candidate_id in seen or not math.isfinite(x) or not math.isfinite(y):
            continue
        seen.add(candidate_id)
        row = db.execute(
            """SELECT * FROM wave_enemies
               WHERE id = ? AND character_id = ? AND phase = ? AND wave = ?
                 AND alive = 1""",
            (
                candidate_id, character["id"], character["current_phase"],
                character["current_wave"],
            ),
        ).fetchone()
        if row is None:
            continue
        distance = math.hypot(x - center_x, y - center_y)
        if distance <= radius:
            candidates.append({"enemy": row, "x": x, "y": y, "distance": distance})
    if effect_kind == "chain":
        candidates.sort(key=lambda candidate: candidate["distance"])
        return candidates[:max(0, int(skill.get("chain_count", 1)) - 1)]
    return candidates


def _is_premium() -> bool:
    user_id = session.get("user_id")
    if user_id is None:
        return False
    user = get_db().execute(
        "SELECT is_premium FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    return bool(user and user["is_premium"])


def _try_auto_potion(db, character, resource: str, value: int, maximum: int):
    """Apply one server-authoritative VIP auto-potion when enabled and ready."""
    if not _is_premium() or maximum <= 0:
        return value, False
    if resource == "health":
        enabled = character["auto_health_potion"]
        ready_at = character["health_potion_ready_at"]
        threshold = AUTO_POTION_HEALTH_THRESHOLD
        restore = AUTO_POTION_HEALTH_RESTORE
        cooldown = AUTO_POTION_HEALTH_COOLDOWN
    else:
        enabled = character["auto_mana_potion"]
        ready_at = character["mana_potion_ready_at"]
        threshold = AUTO_POTION_MANA_THRESHOLD
        restore = AUTO_POTION_MANA_RESTORE
        cooldown = AUTO_POTION_MANA_COOLDOWN
    now = time.time()
    if not enabled or value <= 0 or value > maximum * threshold or ready_at > now:
        return value, False
    value = min(maximum, value + round(maximum * restore))
    ready_column = "health_potion_ready_at" if resource == "health" else "mana_potion_ready_at"
    value_column = "current_health" if resource == "health" else "current_mana"
    db.execute(
        f"UPDATE characters SET {value_column} = ?, {ready_column} = ? WHERE id = ?",
        (value, now + cooldown, character["id"]),
    )
    return value, True


def _valid_csrf(data) -> bool:
    submitted = data.get("csrf_token", "") if isinstance(data, dict) else ""
    expected = session.get("csrf_token", "")
    return bool(submitted and expected and hmac.compare_digest(submitted, expected))


def _active_ids(character_id: int) -> set[str]:
    return {
        row["upgrade_key"]
        for row in get_db().execute(
            "SELECT upgrade_key FROM temporary_upgrades WHERE character_id = ?",
            (character_id,),
        ).fetchall()
    }


def _purchased_talents(character_id: int) -> set[str]:
    return {
        row["talent_id"]
        for row in get_db().execute(
            "SELECT talent_id FROM character_talents WHERE character_id = ?",
            (character_id,),
        ).fetchall()
    }


def _combat_stats(character, active_card_ids=None) -> dict:
    """Calculate combat values with the character's current cards and talents."""
    if active_card_ids is None:
        active_card_ids = _active_ids(character["id"])
    return derived_combat_stats(
        character, active_card_ids, _purchased_talents(character["id"])
    )


def _card_data(card_id: str) -> dict:
    return dict(CARDS[card_id])


def _ensure_offer(character) -> dict | None:
    db = get_db()
    phase, wave = character["current_phase"], character["current_wave"]
    db.execute(
        """DELETE FROM card_offer_history WHERE character_id = ?
           AND (phase != ? OR wave != ?)""",
        (character["id"], phase, wave),
    )
    offer = db.execute(
        """SELECT id, card_ids, recommended_card_id, auto_pick_at, auto_pick_version,
                  selected_card_id, resolved FROM card_offers
           WHERE character_id = ? AND phase = ? AND wave = ?""",
        (character["id"], character["current_phase"], character["current_wave"]),
    ).fetchone()
    if offer is not None and offer["resolved"]:
        db.execute("DELETE FROM card_offers WHERE id = ?", (offer["id"],))
        offer = None
    purchased_talents = _purchased_talents(character["id"])
    if offer is None:
        active_ids = _active_ids(character["id"])
        previously_shown = {
            row["card_id"] for row in db.execute(
                """SELECT card_id FROM card_offer_history
                   WHERE character_id = ? AND phase = ? AND wave = ?""",
                (character["id"], phase, wave),
            ).fetchall()
        }
        ids = draw_card_offer(active_ids, excluded_card_ids=previously_shown)
        stats = _combat_stats(character, active_ids)
        recommendation = recommend_card(
            ids, character["class_id"],
            character["current_health"] / max(1, stats["max_health"]),
            character["current_wave"],
            character["specialization_id"], purchased_talents,
        )
        db.execute(
            "UPDATE characters SET card_offer_revision = card_offer_revision + 1 WHERE id = ?",
            (character["id"],),
        )
        db.execute(
            """INSERT INTO card_offers
               (character_id, phase, wave, card_ids, recommended_card_id,
                auto_pick_at, auto_pick_version, created_at)
               VALUES (?, ?, ?, ?, ?, ?, 1, datetime('now'))""",
            (
                character["id"], character["current_phase"],
                character["current_wave"], json.dumps(ids), recommendation,
                time.time() + CARD_AUTO_PICK_SECONDS if _is_premium() else None,
            ),
        )
        offer = db.execute(
            """SELECT id, card_ids, recommended_card_id, auto_pick_at,
                      auto_pick_version, selected_card_id, resolved FROM card_offers
               WHERE character_id = ? AND phase = ? AND wave = ?""",
            (character["id"], phase, wave),
        ).fetchone()
    else:
        ids = json.loads(offer["card_ids"])
        active_ids = _active_ids(character["id"])
        stats = _combat_stats(character, active_ids)
        recommendation = recommend_card(
            ids, character["class_id"],
            character["current_health"] / max(1, stats["max_health"]),
            character["current_wave"],
            character["specialization_id"], purchased_talents,
        )
        deadline = offer["auto_pick_at"]
        timer_version = offer["auto_pick_version"] or 0
        if _is_premium() and timer_version < 1:
            deadline = max(time.time(), float(deadline) - CARD_AUTO_PICK_SECONDS) if deadline else time.time() + CARD_AUTO_PICK_SECONDS
            timer_version = 1
        elif _is_premium() and not deadline:
            deadline = time.time() + CARD_AUTO_PICK_SECONDS
        elif not _is_premium():
            deadline = None
            timer_version = 1
        if (recommendation != offer["recommended_card_id"]
                or deadline != offer["auto_pick_at"]
                or timer_version != offer["auto_pick_version"]):
            db.execute(
                "UPDATE card_offers SET recommended_card_id = ?, auto_pick_at = ?, auto_pick_version = ? WHERE id = ?",
                (recommendation, deadline, timer_version, offer["id"]),
            )
            offer = db.execute(
                """SELECT id, card_ids, recommended_card_id, auto_pick_at, auto_pick_version,
                      selected_card_id, resolved FROM card_offers WHERE id = ?""",
                (offer["id"],),
            ).fetchone()
    ids = json.loads(offer["card_ids"])
    db.executemany(
        """INSERT OR IGNORE INTO card_offer_history
           (character_id, phase, wave, card_id) VALUES (?, ?, ?, ?)""",
        [(character["id"], phase, wave, card_id) for card_id in ids],
    )
    return {
        "id": offer["id"],
        "recommended_card_id": offer["recommended_card_id"],
        "auto_pick_at": offer["auto_pick_at"],
        "selected_card": _card_data(offer["selected_card_id"])
        if offer["selected_card_id"] else None,
        "cards": [_card_data(card_id) for card_id in ids if card_id in CARDS],
    }


def _active_card_data(character_id: int) -> list[dict]:
    return [
        _card_data(row["upgrade_key"])
        for row in get_db().execute(
            "SELECT upgrade_key FROM temporary_upgrades WHERE character_id = ? ORDER BY id",
            (character_id,),
        ).fetchall()
        if row["upgrade_key"] in CARDS
    ]


def _base_state(character) -> dict:
    db = get_db()
    active_cards = _active_card_data(character["id"])
    stats = _combat_stats(character, {card["id"] for card in active_cards})
    current_offer = db.execute(
        """SELECT id, recommended_card_id, auto_pick_at, resolved FROM card_offers
           WHERE character_id = ? AND phase = ? AND wave = ?""",
        (character["id"], character["current_phase"], character["current_wave"]),
    ).fetchone()
    return {
        "card_experience": character["card_experience"],
        "card_experience_needed": card_xp_needed(len(_active_ids(character["id"]))),
        "pending_card_choices": character["pending_card_choices"],
        "active_cards": active_cards,
        "card_limit": 8 if _is_premium() else 6,
        "is_premium": _is_premium(),
        "offer_id": current_offer["id"] if current_offer and not current_offer["resolved"] else 0,
        "offer_revision": character["card_offer_revision"],
        "recommended_card_id": current_offer["recommended_card_id"] if current_offer else None,
        "auto_pick_at": current_offer["auto_pick_at"] if current_offer else None,
        "offer_resolved": current_offer is None or bool(current_offer["resolved"]),
        "health": character["current_health"],
        "max_health": stats["max_health"],
        "mana": character["current_mana"],
        "max_mana": stats["max_mana"],
        "move_speed_multiplier": stats["move_speed_multiplier"],
        "attack_range_multiplier": stats["attack_range_multiplier"],
        "cooldown_multiplier": stats["cooldown_multiplier"],
    }


@socketio.on("connect")
def on_connect(auth=None):
    character = _character()
    if character is None:
        return False
    join_room(f"user:{session['user_id']}")
    join_room(_room(character["id"]))


@socketio.on("options:update_controls")
def update_control_options(data):
    """Persist the authenticated account's control scheme and current hotbar."""
    if not _valid_csrf(data):
        return {"ok": False, "error": "Sua sessão expirou. Atualize a página."}
    user_id = session.get("user_id")
    if user_id is None:
        return {"ok": False, "error": "Entre na sua conta para salvar as opções."}
    scheme = data.get("scheme") if isinstance(data, dict) else None
    slots = data.get("skill_slots") if isinstance(data, dict) else None
    mouse_left = data.get("mouse_left_slot") if isinstance(data, dict) else None
    mouse_right = data.get("mouse_right_slot") if isinstance(data, dict) else None
    if not isinstance(scheme, str) or scheme not in {"mouse_keyboard", "keyboard_only"}:
        return {"ok": False, "error": "Esquema de controle inválido."}
    character = _character()
    if character is None:
        return {"ok": False, "error": "Personagem inválido."}
    purchased_talents = _purchased_talents(character["id"])
    available_skills = {
        skill["id"]: skill
        for skill in available_class_skills(
            character["class_id"], character["specialization_id"],
            purchased_talents,
        )
    }
    if (not isinstance(slots, list) or len(slots) != 4 or slots[0] != "basic"
            or any(not isinstance(slot, str) or slot not in {"", *available_skills}
                   for slot in slots[1:])):
        return {"ok": False, "error": "O espaço 1 é fixo no Ataque básico; confira as três magias equipadas."}
    equipped = [skill_id for skill_id in slots[1:] if skill_id]
    if len(equipped) != len(set(equipped)):
        return {"ok": False, "error": "Equipe cada habilidade em apenas um espaço."}
    if sum(bool(available_skills[skill_id].get("ultimate")) for skill_id in equipped) > 1:
        return {"ok": False, "error": "Você pode equipar apenas uma habilidade suprema por vez."}
    try:
        mouse_left, mouse_right = int(mouse_left), int(mouse_right)
    except (TypeError, ValueError):
        return {"ok": False, "error": "Escolha espaços válidos para os botões do mouse."}
    if mouse_left not in range(2, 5) or mouse_right not in range(2, 5):
        return {"ok": False, "error": "Os botões do mouse precisam apontar para uma magia nos espaços 2 a 4."}

    db = get_db()
    if not _begin_write(db):
        return {"ok": False, "busy": True, "error": "O banco está ocupado. Tente salvar as opções novamente."}
    db.execute(
        """UPDATE users SET control_scheme = ?, mouse_left_slot = ?, mouse_right_slot = ?,
           skill_slot_1 = ?, skill_slot_2 = ?, skill_slot_3 = ?, skill_slot_4 = ?,
           control_options_version = 1
           WHERE id = ?""",
        (scheme, mouse_left, mouse_right, *slots, user_id),
    )
    db.commit()
    payload = {
        "scheme": scheme,
        "mouse_left_slot": mouse_left,
        "mouse_right_slot": mouse_right,
        "skill_slots": slots,
    }
    socketio.emit("options:controls_updated", payload, to=f"user:{user_id}")
    return {"ok": True, **payload}


@socketio.on("attributes:allocate")
def allocate_attribute_points_live(data):
    if not _valid_csrf(data):
        return {"ok": False, "error": "Sua sessão expirou. Atualize a página."}
    if not session.get("in_lobby"):
        return {"ok": False, "error": "Os atributos só podem ser ajustados na Sala de Espera."}
    attribute = data.get("attribute") if isinstance(data, dict) else None
    if attribute not in {"strength", "agility", "vitality", "energy"}:
        return {"ok": False, "error": "Atributo inválido."}
    try:
        amount = int(data.get("amount", 0))
    except (TypeError, ValueError):
        amount = 0
    if amount < 1:
        return {"ok": False, "error": "Informe uma quantidade válida de pontos."}

    db = get_db()
    if not _begin_write(db):
        return {"ok": False, "busy": True, "error": "O banco está ocupado salvando outra ação. Tente novamente."}
    character = _character()
    if character is None:
        db.rollback()
        return {"ok": False, "error": "Personagem inválido."}
    if amount > character["attribute_points"]:
        db.rollback()
        return {"ok": False, "error": "Você não possui pontos livres suficientes."}
    if character[attribute] + amount > MAX_ATTRIBUTE_VALUE:
        db.rollback()
        return {"ok": False, "error": "Esse atributo atingiria o limite técnico atual."}

    active_ids = _active_ids(character["id"])
    old_stats = _combat_stats(character, active_ids)
    old_health = min(max(0, character["current_health"]), old_stats["max_health"])
    old_mana = min(max(0, character["current_mana"]), old_stats["max_mana"])
    db.execute(
        f"UPDATE characters SET {attribute} = {attribute} + ?, "
        "attribute_points = attribute_points - ? WHERE id = ? AND user_id = ?",
        (amount, amount, character["id"], session["user_id"]),
    )
    updated = db.execute("SELECT * FROM characters WHERE id = ?", (character["id"],)).fetchone()
    new_stats = _combat_stats(updated, active_ids)
    health = min(new_stats["max_health"], old_health + max(0, new_stats["max_health"] - old_stats["max_health"]))
    mana = min(new_stats["max_mana"], old_mana + max(0, new_stats["max_mana"] - old_stats["max_mana"]))
    db.execute(
        "UPDATE characters SET current_health = ?, current_mana = ? WHERE id = ?",
        (health, mana, character["id"]),
    )
    updated = db.execute("SELECT * FROM characters WHERE id = ?", (character["id"],)).fetchone()
    payload = _attribute_state(updated)
    unit = "ponto" if amount == 1 else "pontos"
    verb = "adicionado" if amount == 1 else "adicionados"
    payload["message"] = f"{amount} {unit} {verb} em {_ATTRIBUTE_LABELS[attribute]}."
    db.commit()
    socketio.emit("attributes:updated", payload, to=_room(character["id"]))
    return {"ok": True, **payload}


@socketio.on("attributes:auto_toggle")
def toggle_auto_attribute_distribution(data):
    if not _valid_csrf(data):
        return {"ok": False, "error": "Sua sessão expirou. Atualize a página."}
    if not session.get("in_lobby"):
        return {"ok": False, "error": "A distribuição automática só pode ser alterada na Sala de Espera."}
    if not _is_premium():
        return {"ok": False, "error": "A distribuição automática exige o benefício especial."}
    try:
        enabled = int(data.get("enabled", -1))
    except (TypeError, ValueError):
        enabled = -1
    if enabled not in (0, 1):
        return {"ok": False, "error": "Estado da distribuição automática inválido."}

    db = get_db()
    if not _begin_write(db):
        return {"ok": False, "busy": True, "error": "O banco está ocupado salvando outra ação. Tente novamente."}
    character = _character()
    if character is None:
        db.rollback()
        return {"ok": False, "error": "Personagem inválido."}
    active_ids = _active_ids(character["id"])
    old_stats = _combat_stats(character, active_ids)
    old_health = min(max(0, character["current_health"]), old_stats["max_health"])
    old_mana = min(max(0, character["current_mana"]), old_stats["max_mana"])
    allocated = 0
    remaining = character["attribute_points"]
    if enabled:
        values = {key: character[key] for key in ("strength", "agility", "vitality", "energy")}
        values, remaining, allocated = distribute_attribute_points(
            character["class_id"], values, character["attribute_points"]
        )
        db.execute(
            """UPDATE characters SET strength = ?, agility = ?, vitality = ?, energy = ?,
                      attribute_points = ?, auto_allocate_attributes = 1
               WHERE id = ? AND user_id = ?""",
            (*[values[key] for key in ("strength", "agility", "vitality", "energy")],
             remaining, character["id"], session["user_id"]),
        )
    else:
        db.execute(
            "UPDATE characters SET auto_allocate_attributes = 0 WHERE id = ? AND user_id = ?",
            (character["id"], session["user_id"]),
        )
    updated = db.execute("SELECT * FROM characters WHERE id = ?", (character["id"],)).fetchone()
    new_stats = _combat_stats(updated, active_ids)
    health = min(new_stats["max_health"], old_health + max(0, new_stats["max_health"] - old_stats["max_health"]))
    mana = min(new_stats["max_mana"], old_mana + max(0, new_stats["max_mana"] - old_stats["max_mana"]))
    db.execute(
        "UPDATE characters SET current_health = ?, current_mana = ? WHERE id = ?",
        (health, mana, character["id"]),
    )
    updated = db.execute("SELECT * FROM characters WHERE id = ?", (character["id"],)).fetchone()
    payload = _attribute_state(updated)
    class_name = CLASSES[character["class_id"]]["name"]
    if enabled:
        allocated_label = "ponto" if allocated == 1 else "pontos"
        allocated_verb = "foi distribuído" if allocated == 1 else "foram distribuídos"
        remaining_label = "ponto" if remaining == 1 else "pontos"
        remaining_verb = "continua disponível" if remaining == 1 else "continuam disponíveis"
        payload["message"] = (
            f"Distribuição automática ativada para {class_name}: {allocated} {allocated_label} {allocated_verb} "
            f"conforme a classe. {remaining} {remaining_label} {remaining_verb}; os próximos ganhos também serão distribuídos."
        )
    else:
        payload["message"] = "Distribuição automática desativada. Os atributos já distribuídos permanecem como estão."
    payload["class_distribution"] = CLASS_AUTO_DISTRIBUTION.get(character["class_id"], {})
    db.commit()
    socketio.emit("attributes:updated", payload, to=_room(character["id"]))
    return {"ok": True, **payload}


def _attribute_state(character) -> dict:
    active_ids = _active_ids(character["id"])
    purchased_talents = {
        row["talent_id"] for row in get_db().execute(
            "SELECT talent_id FROM character_talents WHERE character_id = ?",
            (character["id"],),
        ).fetchall()
    }
    class_info = CLASSES[character["class_id"]]
    return {
        "attributes": {key: character[key] for key in ("strength", "agility", "vitality", "energy")},
        "base_attributes": class_info["base_attributes"],
        "attribute_points": character["attribute_points"],
        "auto_allocate_attributes": bool(character["auto_allocate_attributes"]),
        "current_health": character["current_health"],
        "current_mana": character["current_mana"],
        "combat_summary": combat_summary(character, active_ids, purchased_talents),
    }


@socketio.on("card_orb:collect")
def collect_card_orb(data):
    if not _valid_csrf(data):
        return {"ok": False, "error": "Sua sessão expirou. Atualize a página."}
    try:
        orb_id = int(data.get("orb_id"))
    except (TypeError, ValueError):
        return {"ok": False, "error": "Dados do orbe inválidos."}

    db = get_db()
    if not _begin_write(db):
        return {"ok": False, "busy": True, "error": "O banco está ocupado salvando outra ação. Tente novamente."}
    character = _character()
    if character is None:
        db.rollback()
        return {"ok": False, "error": "Personagem inválido."}
    mission_run = active_mission_run(
        db, character["user_id"], character["id"]
    )
    if mission_run is None and not current_app.config.get("TESTING"):
        db.rollback()
        return {"ok": False, "error": "Nenhuma missão ativa."}
    if mission_run is not None and (
        mission_run["phase"] != character["current_phase"]
        or mission_run["difficulty"] != character["current_difficulty"]
    ):
        db.rollback()
        return {"ok": False, "error": "A missão ativa não corresponde à fase atual."}
    if (character["phase_preparation_until"] > time.time()
            or character["phase_intermission"] or character["death_intermission"]):
        db.rollback()
        return {"ok": False, "error": "Aguarde a contagem regressiva ou a escolha de fase."}
    orb = db.execute(
        "SELECT id, collected FROM card_xp_orbs WHERE id = ? AND character_id = ?",
        (orb_id, character["id"]),
    ).fetchone()
    if orb is None:
        db.rollback()
        return {"ok": False, "error": "Orbe inválido."}
    if orb["collected"]:
        db.commit()
        return {"ok": True, "already_collected": True, "orb_id": orb_id}
    orb = db.execute(
        """SELECT id, world_x, world_y, xp_value FROM card_xp_orbs
           WHERE id = ? AND character_id = ? AND collected = 0""",
        (orb_id, character["id"]),
    ).fetchone()
    if orb is None:
        db.rollback()
        return {"ok": False, "error": "Esse orbe já foi coletado."}
    xp_gained = CARD_XP_PER_ORB_PREMIUM if _is_premium() else orb["xp_value"]
    new_xp = character["card_experience"] + xp_gained
    threshold = card_xp_needed(len(_active_ids(character["id"])))
    new_choices, remaining_xp = divmod(new_xp, threshold)
    db.execute("UPDATE card_xp_orbs SET collected = 1 WHERE id = ?", (orb_id,))
    db.execute(
        """UPDATE characters SET card_experience = ?,
               pending_card_choices = pending_card_choices + ? WHERE id = ?""",
        (remaining_xp, new_choices, character["id"]),
    )
    updated = db.execute(
        "SELECT * FROM characters WHERE id = ?", (character["id"],)
    ).fetchone()
    offer = _ensure_offer(updated) if new_choices else None
    if offer:
        updated = db.execute(
            "SELECT * FROM characters WHERE id = ?", (character["id"],)
        ).fetchone()
    db.commit()
    payload = _base_state(updated)
    payload.update({"orb_id": orb_id, "xp_gained": xp_gained})
    socketio.emit("card_xp:updated", payload, to=_room(character["id"]))
    if offer:
        card_state = {
            **payload,
            "offer": offer,
            "offer_id": offer["id"],
            "offer_resolved": False,
        }
        socketio.emit("card:state", card_state, to=_room(character["id"]))
    return {"ok": True, **payload}


def _card_choice_resync(character, message: str) -> dict:
    """Return the current persisted offer when a client submits stale choices."""
    db = get_db()
    current = db.execute(
        "SELECT * FROM characters WHERE id = ?", (character["id"],)
    ).fetchone()
    offer = None
    if (current["pending_card_choices"] > 0
            and not current["phase_intermission"]
            and not current["death_intermission"]):
        offer = _ensure_offer(current)
        current = db.execute(
            "SELECT * FROM characters WHERE id = ?", (character["id"],)
        ).fetchone()
    payload = _base_state(current)
    offer_id = offer["id"] if offer else 0
    db.commit()
    payload.update({
        "ok": False,
        "stale": True,
        "error": message,
        "offer": offer,
        "offer_id": offer_id,
        "offer_resolved": offer is None,
    })
    socketio.emit("card:state", payload, to=_room(character["id"]))
    return payload


def _choose_card(data, automatic: bool = False):
    if not _valid_csrf(data):
        return {"ok": False, "error": "Sua sessão expirou. Atualize a página."}
    db = get_db()
    if not _begin_write(db):
        return {"ok": False, "busy": True, "error": "O banco está ocupado salvando outra ação. Tente novamente."}
    character = _character()
    if character is None:
        db.rollback()
        return {"ok": False, "error": "Personagem inválido."}
    offer = db.execute(
        """SELECT id, card_ids, recommended_card_id, auto_pick_at,
                  selected_card_id, resolved FROM card_offers
           WHERE character_id = ? AND phase = ? AND wave = ?""",
        (character["id"], character["current_phase"], character["current_wave"]),
    ).fetchone()
    try:
        submitted_offer_id = int(data.get("offer_id"))
    except (TypeError, ValueError):
        submitted_offer_id = None
    if (offer is None or offer["resolved"]
        or submitted_offer_id != offer["id"]):
        return _card_choice_resync(
            character,
            "As opções de cartas foram atualizadas. Escolha uma das cartas exibidas agora.",
        )
    db.executemany(
        """INSERT OR IGNORE INTO card_offer_history
           (character_id, phase, wave, card_id) VALUES (?, ?, ?, ?)""",
        [
            (character["id"], character["current_phase"], character["current_wave"], card_id)
            for card_id in json.loads(offer["card_ids"])
        ],
    )

    if automatic:
        if not _is_premium():
            db.rollback()
            return {"ok": False, "error": "A escolha automática de cartas exige o benefício especial."}
        if time.time() < float(offer["auto_pick_at"] or 0):
            remaining = max(0, int(float(offer["auto_pick_at"]) - time.time() + .999))
            db.rollback()
            return {"ok": False, "not_due": True, "remaining_seconds": remaining}
        if not offer["selected_card_id"] and not offer["recommended_card_id"]:
            db.rollback()
            return _card_choice_resync(
                character, "A recomendação não está disponível. Atualizei a oferta atual."
            )
        if not offer["selected_card_id"]:
            data = {**data, "card_id": offer["recommended_card_id"]}

    active = _active_ids(character["id"])
    capacity = 8 if _is_premium() else 6
    action = data.get("action")
    if action == "keep" and not automatic and len(active) < capacity:
        db.rollback()
        return {"ok": False, "error": "Ainda há espaço livre. Escolha uma das cartas oferecidas."}
    if automatic and offer["selected_card_id"]:
        db.rollback()
        payload = _base_state(character)
        payload.update({
            "ok": True,
            "replacement_required": True,
            "selected_card": _card_data(offer["selected_card_id"]),
            "offer_id": offer["id"],
            "offer_resolved": False,
        })
        socketio.emit("card:state", payload, to=_room(character["id"]))
        return payload
    if action == "keep" and not automatic:
        db.execute("UPDATE card_offers SET resolved = 1 WHERE id = ?", (offer["id"],))
        db.execute(
            "UPDATE characters SET pending_card_choices = MAX(0, pending_card_choices - 1) WHERE id = ?",
            (character["id"],),
        )
        message = "Cartas ativas mantidas. As três opções desta oferta foram descartadas."
    elif offer["selected_card_id"]:
        replacement_id = data.get("replacement_card_id")
        if replacement_id not in active or len(active) < capacity:
            db.rollback()
            return {"ok": False, "error": "Escolha uma carta ativa para substituir."}
        chosen_id = offer["selected_card_id"]
        db.execute(
            "DELETE FROM temporary_upgrades WHERE character_id = ? AND upgrade_key = ?",
            (character["id"], replacement_id),
        )
        db.execute(
            "INSERT INTO temporary_upgrades (character_id, upgrade_key) VALUES (?, ?)",
            (character["id"], chosen_id),
        )
        db.execute("UPDATE card_offers SET resolved = 1 WHERE id = ?", (offer["id"],))
        db.execute(
            "UPDATE characters SET pending_card_choices = MAX(0, pending_card_choices - 1) WHERE id = ?",
            (character["id"],),
        )
        message = f"{CARDS[chosen_id]['name']} ativada na coleção."
    else:
        chosen_id = data.get("card_id", "")
        offered_ids = set(json.loads(offer["card_ids"]))
        if chosen_id not in offered_ids or chosen_id in active or chosen_id not in CARDS:
            return _card_choice_resync(
                character,
                "Essa oferta mudou. Atualizei as opções; escolha uma das cartas atuais.",
            )
        if len(active) >= capacity:
            if automatic:
                purchased_talents = _purchased_talents(character["id"])
                ordered_active = [
                    row["upgrade_key"]
                    for row in db.execute(
                        "SELECT upgrade_key FROM temporary_upgrades WHERE character_id = ? ORDER BY id",
                        (character["id"],),
                    ).fetchall()
                    if row["upgrade_key"] in CARDS
                ]
                if not ordered_active:
                    db.rollback()
                    return _card_choice_resync(character, "A coleção mudou. Atualizei as opções de cartas.")
                health_ratio = character["current_health"] / max(1, _combat_stats(character)["max_health"])
                replacement_id = min(
                    ordered_active,
                    key=lambda card_id: card_recommendation_score(
                        card_id, character["class_id"], health_ratio,
                        character["current_wave"], character["specialization_id"],
                        purchased_talents,
                    ),
                )
                chosen_score = card_recommendation_score(
                    chosen_id, character["class_id"], health_ratio,
                    character["current_wave"], character["specialization_id"],
                    purchased_talents,
                )
                replaced_score = card_recommendation_score(
                    replacement_id, character["class_id"], health_ratio,
                    character["current_wave"], character["specialization_id"],
                    purchased_talents,
                )
                if chosen_score < replaced_score:
                    message = "Coleção mantida: a carta recomendada não supera nenhuma das cartas ativas."
                else:
                    db.execute(
                        "DELETE FROM temporary_upgrades WHERE character_id = ? AND upgrade_key = ?",
                        (character["id"], replacement_id),
                    )
                    db.execute(
                        "INSERT INTO temporary_upgrades (character_id, upgrade_key) VALUES (?, ?)",
                        (character["id"], chosen_id),
                    )
                    message = f"{CARDS[chosen_id]['name']} ativada automaticamente; {CARDS[replacement_id]['name']} foi substituída."
                db.execute("UPDATE card_offers SET resolved = 1 WHERE id = ?", (offer["id"],))
                db.execute(
                    "UPDATE characters SET pending_card_choices = MAX(0, pending_card_choices - 1) WHERE id = ?",
                    (character["id"],),
                )
            else:
                db.execute(
                    "UPDATE card_offers SET selected_card_id = ? WHERE id = ?",
                    (chosen_id, offer["id"]),
                )
                db.commit()
                payload = _base_state(character)
                payload.update({"ok": True, "replacement_required": True,
                                "selected_card": _card_data(chosen_id),
                                "offer_id": offer["id"], "offer_resolved": False})
                socketio.emit("card:state", payload, to=_room(character["id"]))
                return payload
        else:
            db.execute(
                "INSERT INTO temporary_upgrades (character_id, upgrade_key) VALUES (?, ?)",
                (character["id"], chosen_id),
            )
            db.execute("UPDATE card_offers SET resolved = 1 WHERE id = ?", (offer["id"],))
            if character["pending_card_choices"] > 0:
                db.execute(
                    "UPDATE characters SET pending_card_choices = pending_card_choices - 1 WHERE id = ?",
                    (character["id"],),
                )
            message = f"{CARDS[chosen_id]['name']} ativada na coleção."

    updated = db.execute("SELECT * FROM characters WHERE id = ?", (character["id"],)).fetchone()
    updated_stats = _combat_stats(updated, _active_ids(character["id"]))
    health = min(updated["current_health"], updated_stats["max_health"])
    mana = min(updated["current_mana"], updated_stats["max_mana"])
    if health != updated["current_health"] or mana != updated["current_mana"]:
        db.execute("UPDATE characters SET current_health = ?, current_mana = ? WHERE id = ?",
                   (health, mana, character["id"]))
        updated = db.execute("SELECT * FROM characters WHERE id = ?", (character["id"],)).fetchone()
    next_offer = _ensure_offer(updated) if updated["pending_card_choices"] > 0 else None
    if next_offer:
        updated = db.execute(
            "SELECT * FROM characters WHERE id = ?", (character["id"],)
        ).fetchone()
    db.commit()
    payload = _base_state(updated)
    payload.update({
        "ok": True,
        "message": message,
        "offer": next_offer,
        "offer_id": next_offer["id"] if next_offer else offer["id"],
        "offer_resolved": next_offer is None,
    })
    socketio.emit("card:state", payload, to=_room(character["id"]))
    return payload


@socketio.on("card:choose")
def choose_card(data):
    return _choose_card(data)


@socketio.on("card:auto_choose")
def auto_choose_card(data):
    return _choose_card(data, automatic=True)


@socketio.on("game:complete_wave")
def complete_wave(data):
    if not current_app.config.get("TESTING"):
        return {"ok": False, "error": "Ação de teste indisponível."}
    if not _valid_csrf(data):
        return {"ok": False, "error": "Sua sessão expirou. Atualize a página."}
    db = get_db()
    if not _begin_write(db):
        return {"ok": False, "busy": True, "error": "O banco está ocupado salvando outra ação. Tente novamente."}
    character = _character()
    if character is None:
        db.rollback()
        return {"ok": False, "error": "Personagem inválido."}
    mission_run = active_mission_run(
        db, character["user_id"], character["id"]
    )
    if mission_run is None and not current_app.config.get("TESTING"):
        db.rollback()
        return {"ok": False, "error": "Nenhuma missão ativa."}
    if mission_run is not None and (
        mission_run["phase"] != character["current_phase"]
        or mission_run["difficulty"] != character["current_difficulty"]
    ):
        db.rollback()
        return {"ok": False, "error": "A missão ativa não corresponde à fase atual."}
    if character["campaign_complete"]:
        db.rollback()
        return {"ok": False, "error": "A Temporada 1 já foi concluída."}
    offer = db.execute(
        """SELECT resolved FROM card_offers WHERE character_id = ? AND phase = ? AND wave = ?""",
        (character["id"], character["current_phase"], character["current_wave"]),
    ).fetchone()
    if character["phase_intermission"] or character["death_intermission"]:
        db.rollback()
        return {"ok": False, "error": "Escolha como deseja continuar antes de iniciar a fase."}
    if character["phase_preparation_until"] > time.time():
        db.rollback()
        return {"ok": False, "error": "Aguarde o fim da preparação da fase."}
    if (offer is not None and not offer["resolved"]) or character["pending_card_choices"] > 0:
        db.rollback()
        return {"ok": False, "error": "Escolha ou mantenha sua carta antes de avançar."}

    old_phase, old_wave = character["current_phase"], character["current_wave"]
    reward = wave_experience_reward(
        old_phase, old_wave, character["phase_xp_budget"],
        character["current_difficulty"],
    )
    # Monster EXP is granted on kill, never again on wave transition.
    level, experience, levels_gained = character["level"], character["experience"], 0
    phase_ended = old_wave == WAVES_PER_PHASE
    was_boss_wave = encounter_type(old_phase, old_wave) == "boss"
    was_miniboss_wave = encounter_type(old_phase, old_wave) == "miniboss"
    campaign_complete = phase_ended and old_phase >= SEASON_1_PHASES
    if phase_ended and not campaign_complete:
        phase, wave = old_phase + 1, 1
    elif phase_ended:
        phase, wave = old_phase, old_wave
    else:
        phase, wave = old_phase, old_wave + 1
    preparation_until = character["phase_preparation_until"]
    attribute_points_gained = levels_gained * ATTRIBUTE_POINTS_PER_LEVEL
    _, auto_allocated = award_attribute_points(
        db, character["id"], levels_gained, _is_premium()
    )
    updated = db.execute("SELECT * FROM characters WHERE id = ?", (character["id"],)).fetchone()
    active_card_ids = _active_ids(character["id"])
    combat_stats = _combat_stats(updated, active_card_ids)
    max_health, max_mana = combat_stats["max_health"], combat_stats["max_mana"]
    if phase_ended:
        preparation_until = 0
        db.execute("DELETE FROM temporary_upgrades WHERE character_id = ?", (character["id"],))
        db.execute("DELETE FROM card_offers WHERE character_id = ?", (character["id"],))
        db.execute("DELETE FROM card_offer_history WHERE character_id = ?", (character["id"],))
        db.execute("DELETE FROM card_xp_orbs WHERE character_id = ?", (character["id"],))
        combat_stats = _combat_stats(updated)
        max_health, max_mana = combat_stats["max_health"], combat_stats["max_mana"]
        db.execute(
            """UPDATE characters SET level = ?, experience = ?, current_phase = ?, current_wave = ?,
               current_health = ?, current_mana = ?, phase_preparation_until = ?, phase_xp_budget = ?,
               phase_intermission = ?, campaign_complete = ?,
               card_experience = 0, pending_card_choices = 0 WHERE id = ?""",
            (
                level, experience, phase, wave, max_health, max_mana,
                preparation_until, phase_xp_budget_for_level(level),
                int(not campaign_complete), int(campaign_complete), character["id"],
            ),
        )
    else:
        health = min(max_health, character["current_health"] + round(max_health * combat_stats["wave_heal"]))
        db.execute(
            """UPDATE characters SET level = ?, experience = ?, current_phase = ?, current_wave = ?,
               current_health = ?
               WHERE id = ?""",
            (level, experience, phase, wave, health, character["id"]),
        )
    updated = db.execute("SELECT * FROM characters WHERE id = ?", (character["id"],)).fetchone()
    db.commit()
    card_state = _base_state(updated)
    payload = {
        "ok": True,
        "phase": phase,
        "wave": wave,
        "level": level,
        "experience": experience,
        "next_level_xp": experience_needed(level) if level < MAX_LEVEL else 0,
        "max_level": MAX_LEVEL,
        "health": updated["current_health"],
        "max_health": max_health,
        "mana": updated["current_mana"],
        "max_mana": max_mana,
        "phase_preparation_until": preparation_until,
        "monsters_remaining": (
            0 if campaign_complete else enemies_in_wave(
                wave, phase, character["current_difficulty"]
            )
        ),
        "experience_reward": reward,
        "levels_gained": levels_gained,
        "attribute_points_gained": levels_gained * 5,
        "attribute_points": updated["attribute_points"],
        "auto_allocated_attributes": auto_allocated,
        "is_boss_wave": was_boss_wave,
        "is_miniboss_wave": was_miniboss_wave,
        "phase_changed": phase != old_phase,
        "awaiting_phase_choice": phase_ended and not campaign_complete,
        "campaign_complete": campaign_complete,
        "next_wave_reward": (
            0 if campaign_complete else wave_experience_reward(
                phase, wave,
                phase_xp_budget_for_level(level)
                if phase_ended else character["phase_xp_budget"],
                character["current_difficulty"],
            )
        ),
        "next_is_boss": encounter_type(phase, wave) == "boss",
        "next_is_miniboss": encounter_type(phase, wave) == "miniboss",
        "card_state": card_state,
    }
    socketio.emit("game:wave_updated", payload, to=_room(character["id"]))
    return payload


@socketio.on("combat:attack")
def attack_enemy(data):
    if not _valid_csrf(data):
        return {"ok": False, "error": "Sua sessão expirou. Atualize a página."}
    now_ms = int(time.time() * 1000)
    for old_id, old_attack in list(_pending_player_attacks.items()):
        if old_attack["expires_at"] < now_ms:
            _pending_player_attacks.pop(old_id, None)
    projectile_id = data.get("projectile_id")
    pending_attack = None
    if projectile_id:
        pending_attack = _pending_player_attacks.get(str(projectile_id))
        if pending_attack is None or pending_attack["sid"] != request.sid:
            return {"ok": False, "error": "Esse projétil não está mais ativo."}
        now_ms = int(time.time() * 1000)
        if not pending_attack.get("reflection") and now_ms < pending_attack["impact_at"] - 75:
            return {"ok": False, "early": True}
        if now_ms > pending_attack["expires_at"]:
            _pending_player_attacks.pop(str(projectile_id), None)
            return {"ok": False, "expired": True}
        data = {
            **pending_attack["attack_data"],
            "projectile_id": str(projectile_id),
            "csrf_token": data.get("csrf_token", ""),
        }
    try:
        enemy_id = int(data.get("enemy_id"))
    except (TypeError, ValueError):
        return {"ok": False, "error": "Alvo inválido."}
    try:
        spawn_origin = (float(data.get("player_x", 1200)), float(data.get("player_y", 900)))
        if not all(math.isfinite(value) for value in spawn_origin):
            raise ValueError("Posição inválida")
    except (TypeError, ValueError):
        spawn_origin = (1200, 900)
    db = get_db()
    if not _begin_write(db):
        return {"ok": False, "busy": True, "error": "O banco está ocupado salvando outra ação. Tente novamente."}
    character = _character()
    if character is None:
        db.rollback()
        return {"ok": False, "error": "Personagem inválido."}
    spawn_origin = clamp_map_position(*spawn_origin, character["current_phase"])
    mission_run = active_mission_run(
        db, character["user_id"], character["id"]
    )
    if mission_run is None and not current_app.config.get("TESTING"):
        db.rollback()
        return {"ok": False, "error": "Nenhuma missão ativa."}
    if mission_run is not None and (
        mission_run["phase"] != character["current_phase"]
        or mission_run["difficulty"] != character["current_difficulty"]
    ):
        db.rollback()
        return {"ok": False, "error": "A missão ativa não corresponde à fase atual."}
    if character["phase_intermission"] or character["death_intermission"]:
        db.rollback()
        return {"ok": False, "error": "Escolha como deseja continuar antes de iniciar a fase."}
    if pending_attack and (
        character["id"] != pending_attack["character_id"]
        or (character["current_phase"], character["current_wave"])
        != (pending_attack["phase"], pending_attack["wave"])
    ):
        _pending_player_attacks.pop(str(projectile_id), None)
        db.rollback()
        return {"ok": False, "error": "A onda do projétil já terminou."}
    if not pending_attack and any(
        attack["character_id"] == character["id"]
        for attack in _pending_player_attacks.values()
    ):
        db.rollback()
        return {"ok": False, "pending": True, "error": "Aguarde seu projétil atingir o alvo."}
    requested_skill_id = data.get("skill_id", "basic")
    if not isinstance(requested_skill_id, str):
        db.rollback()
        return {"ok": False, "error": "Habilidade inválida."}
    skill_id = requested_skill_id
    active_card_ids = _active_ids(character["id"])
    purchased_talents = _purchased_talents(character["id"])
    combat_stats = derived_combat_stats(character, active_card_ids, purchased_talents)
    skill = None
    if skill_id != "basic":
        saved_controls = db.execute(
            """SELECT skill_slot_2, skill_slot_3, skill_slot_4
               FROM users WHERE id = ?""",
            (session.get("user_id"),),
        ).fetchone()
        if saved_controls is None:
            db.rollback()
            return {"ok": False, "error": "Não foi possível confirmar os atalhos desta conta."}
        saved_slots = [
            "basic", saved_controls["skill_slot_2"],
            saved_controls["skill_slot_3"], saved_controls["skill_slot_4"],
        ]
        equipped_skill_ids = set(normalized_skill_slots(
            character["class_id"], character["specialization_id"],
            purchased_talents, saved_slots,
        )[1:])
        launched_as_equipped = (
            pending_attack is not None
            and pending_attack.get("skill_id") == skill_id
        )
        if skill_id not in equipped_skill_ids and not launched_as_equipped:
            db.rollback()
            return {"ok": False, "error": "Essa habilidade não está equipada ou ainda não foi desbloqueada."}
        skill = SKILLS[skill_id]
    now = time.monotonic()
    max_health, max_mana = combat_stats["max_health"], combat_stats["max_mana"]
    if character["phase_preparation_until"] > time.time():
        db.rollback()
        return {"ok": False, "error": "Aguarde o fim da preparação da fase."}
    fallback_reason = None
    cooldown_key = (character["id"], skill_id)
    mana_cost = skill["mana"] if skill else 0
    if skill and not pending_attack and _skill_cooldowns.get(cooldown_key, 0) > now:
        skill_id, skill, mana_cost = "basic", None, 0
        fallback_reason = "cooldown"
    elif skill and not pending_attack and character["current_mana"] < mana_cost:
        skill_id, skill, mana_cost = "basic", None, 0
        fallback_reason = "mana"

    attack_damage_type = (
        skill["damage_type"] if skill
        else CLASS_BASE_SKILLS[character["class_id"]]["basic_damage_type"]
    )
    attack_element = (
        skill.get("element") if skill
        else CLASS_BASE_SKILLS[character["class_id"]].get("basic_element")
    )
    cooldown_key = (character["id"], skill_id)
    cooldown = cooldown_for_agility(
        (
            combat_stats["basic_cooldown"]
            if skill_id == "basic"
            else skill["cooldown"]
        )
        * combat_stats["cooldown_multiplier"], character["agility"],
    )
    if (
        skill_id == "basic" and not pending_attack
        and _basic_attack_cooldowns.get(character["id"], 0) > now
    ):
        db.rollback()
        return {
            "ok": False,
            "fallback": bool(fallback_reason),
            "fallback_reason": fallback_reason,
            "error": "Ataque básico em recarga.",
        }
    enemy = db.execute(
        """SELECT * FROM wave_enemies WHERE id = ? AND character_id = ? AND phase = ? AND wave = ? AND alive = 1""",
        (enemy_id, character["id"], character["current_phase"], character["current_wave"]),
    ).fetchone()
    if enemy is None:
        db.rollback()
        return {"ok": False, "error": "Esse inimigo já foi derrotado."}
    try:
        target_x = float(data.get("enemy_x"))
        target_y = float(data.get("enemy_y"))
        if not math.isfinite(target_x) or not math.isfinite(target_y):
            raise ValueError("Posição inválida")
        target_x, target_y = clamp_map_position(
            target_x, target_y, character["current_phase"]
        )
    except (TypeError, ValueError):
        db.rollback()
        return {"ok": False, "error": "Não foi possível confirmar a posição do alvo."}
    class_ranges = CLASSES.get(character["class_id"], {})
    max_attack_range = class_ranges.get(
        "base_attack_range" if skill_id == "basic" else "base_skill_range", 100
    ) * combat_stats["attack_range_multiplier"]
    target_radius = (
        28 if encounter_type(enemy["phase"], enemy["wave"]) == "boss"
        else 24 if encounter_type(enemy["phase"], enemy["wave"]) == "miniboss"
        else 17
    )
    if math.hypot(target_x - spawn_origin[0], target_y - spawn_origin[1]) > max_attack_range + target_radius:
        db.rollback()
        return {"ok": False, "error": "O monstro está fora do alcance deste ataque."}
    nearby_enemies = data.get("nearby_enemies", [])
    if pending_attack:
        damage = pending_attack["damage"]
        critical = pending_attack["critical"]
    else:
        skill_burst = bool(
            skill and random.random() < combat_stats["skill_burst_chance"]
        )
        attack_streak = 0
        if combat_stats["attack_streak_cap"]:
            previous_count, previous_attack = _card_attack_streaks.get(character["id"], (0, 0))
            streak_count = min(combat_stats["attack_streak_cap"], previous_count + 1) if now - previous_attack <= 3 else 1
            _card_attack_streaks[character["id"]] = (streak_count, now)
            attack_streak = streak_count
        else:
            _card_attack_streaks.pop(character["id"], None)
        critical = bool(skill and skill.get("force_critical")) or (
            random.random() < combat_stats["critical_chance"]
        )
        damage = calculate_attack_damage(
            combat_stats,
            skill,
            attack_damage_type,
            attack_element,
            enemy["phase"],
            enemy["wave"],
            critical=critical,
            skill_burst=skill_burst,
            attack_streak=attack_streak,
        )
    if skill and skill.get("projectile") and not pending_attack:
        created_at = int(time.time() * 1000)
        flight_ms = max(
            180,
            min(900, round(math.hypot(target_x - spawn_origin[0], target_y - spawn_origin[1]) / 900 * 1000)),
        )
        impact_at = created_at + flight_ms
        attack_id = secrets.token_urlsafe(18)
        projectile = {
            "origin_x": spawn_origin[0],
            "origin_y": spawn_origin[1],
            "target_x": target_x,
            "target_y": target_y,
            "flight_ms": flight_ms,
            "damage_type": skill["damage_type"],
            "element": skill.get("element"),
        }
        attack_payload = {
            "attack_id": attack_id,
            "enemy_id": enemy_id,
            "skill_id": skill_id,
            "name": skill["name"],
            "projectile": projectile,
            "created_at": created_at,
            "impact_at": impact_at,
        }
        _pending_player_attacks[attack_id] = {
            **attack_payload,
            "character_id": character["id"],
            "phase": enemy["phase"],
            "wave": enemy["wave"],
            "sid": request.sid,
            "damage": damage,
            "critical": critical,
            "mana_cost": mana_cost,
            "mana_spent": True,
            "cooldown_reserved": True,
            "expires_at": impact_at + 1500,
            "attack_data": {
                "enemy_id": enemy_id,
                "enemy_x": target_x,
                "enemy_y": target_y,
                "player_x": spawn_origin[0],
                "player_y": spawn_origin[1],
                "skill_id": requested_skill_id,
                "nearby_enemies": nearby_enemies,
            },
        }
        for old_id, old_attack in list(_pending_player_attacks.items()):
            if old_attack["expires_at"] < created_at:
                _pending_player_attacks.pop(old_id, None)
        mana = character["current_mana"] - mana_cost
        if mana_cost:
            db.execute(
                "UPDATE characters SET current_mana = ? WHERE id = ?",
                (mana, character["id"]),
            )
        db.commit()
        _skill_cooldowns[cooldown_key] = now + cooldown
        socketio.emit(
            "combat:player_projectile", attack_payload,
            to=_room(character["id"]), skip_sid=request.sid,
        )
        socketio.emit(
            "combat:player_mana_updated",
            {"mana": mana, "max_mana": max_mana},
            to=_room(character["id"]), skip_sid=request.sid,
        )
        return {
            "ok": True,
            "projectile_pending": True,
            "cooldown_ms": int(cooldown * 1000),
            "skill_id": skill_id,
            "mana": mana,
            "max_mana": max_mana,
            **attack_payload,
        }
    base_damage = damage
    shadow_support = _consume_shadow_summons(character["id"], base_damage)
    damage += shadow_support["damage"]
    hp = max(0, enemy["hp"] - damage)
    defeated = hp == 0
    shadow_summoned = bool(
        skill and skill.get("effect_kind") == "shadow_raise" and defeated
    )
    shadow_soldier_count = shadow_support["count"]
    if shadow_summoned:
        shadow_soldier_count = _raise_shadow_soldier(
            character["id"],
            skill,
            enemy_name(
                enemy["enemy_index"], enemy["wave"], WAVES_PER_PHASE,
                phase=enemy["phase"],
            ),
        )
    drop_x, drop_y = enemy["world_x"], enemy["world_y"]
    if defeated:
        drop_x, drop_y = target_x, target_y
        db.execute("""UPDATE wave_enemies SET hp = ?, alive = 0, world_x = ?, world_y = ?
                      WHERE id = ?""", (hp, drop_x, drop_y, enemy_id))
    else:
        db.execute("UPDATE wave_enemies SET hp = ? WHERE id = ?", (hp, enemy_id))
    damage_dealt = min(enemy["hp"], damage)
    root_duration_ms = round(
        min(3, max(0, float(skill.get("immobilize_duration", 0)))) * 1000
    ) if skill and skill.get("effect_kind") == "gravity_well" else 0
    affected_enemies = [{
        "id": enemy_id, "hp": hp, "alive": not defeated,
        "damage": damage_dealt, "world_x": drop_x if defeated else enemy["world_x"],
        "world_y": drop_y if defeated else enemy["world_y"],
        "position_changed": defeated,
        "root_duration_ms": root_duration_ms,
    }]
    secondary_targets = _skill_area_targets(
        db, character, skill or {}, nearby_enemies, target_x, target_y,
        spawn_origin[0], spawn_origin[1], enemy_id,
    ) if skill else []
    secondary_xp = 0
    secondary_damage = 0
    defeated_enemy_ids = [enemy_id] if defeated else []
    affected_area = [*secondary_targets]
    if skill and skill.get("effect_kind") in {"repulse", "gravity_well"}:
        primary_target = {
            "enemy": enemy, "x": target_x, "y": target_y,
        }
        affected_area.insert(0, primary_target)
    for candidate in affected_area:
        target_enemy = candidate["enemy"]
        candidate_x, candidate_y = candidate["x"], candidate["y"]
        is_primary_target = target_enemy["id"] == enemy_id
        hit_damage = 0 if is_primary_target else (
            round(base_damage * skill.get("chain_damage_fraction", 1))
            if skill and skill.get("effect_kind") == "chain"
            else base_damage
        )
        target_hp = hp if is_primary_target else max(0, target_enemy["hp"] - hit_damage)
        target_defeated = defeated if is_primary_target else target_hp == 0
        if target_defeated and not is_primary_target:
            defeated_enemy_ids.append(target_enemy["id"])
        if skill and skill.get("effect_kind") == "repulse":
            dx, dy = candidate_x - spawn_origin[0], candidate_y - spawn_origin[1]
            distance = math.hypot(dx, dy) or 1
            knockback = min(220, max(0, float(skill.get("knockback_distance", 0))))
            candidate_x, candidate_y = clamp_map_position(
                candidate_x + dx / distance * knockback,
                candidate_y + dy / distance * knockback,
                character["current_phase"],
            )
        elif skill and skill.get("effect_kind") == "gravity_well":
            dx, dy = candidate_x - target_x, candidate_y - target_y
            distance = math.hypot(dx, dy)
            pull = min(220, max(0, float(skill.get("pull_distance", 0))))
            movement = min(pull, max(0, distance - 20))
            if distance:
                candidate_x -= dx / distance * movement
                candidate_y -= dy / distance * movement
        candidate_x, candidate_y = clamp_map_position(
            candidate_x, candidate_y, character["current_phase"]
        )
        if (
            character["current_phase"] == 1
            and not target_defeated
            and terminal_vilar_collides(candidate_x, candidate_y, 28)
        ):
            candidate_x = target_enemy["world_x"]
            candidate_y = target_enemy["world_y"]
        db.execute(
            """UPDATE wave_enemies SET hp = ?, alive = ?, world_x = ?, world_y = ?
               WHERE id = ?""",
            (
                target_hp, int(not target_defeated), candidate_x, candidate_y,
                target_enemy["id"],
            ),
        )
        dealt = 0 if is_primary_target else min(target_enemy["hp"], hit_damage)
        secondary_damage += dealt
        if target_defeated and not is_primary_target:
            secondary_xp += enemy_experience_reward(
                target_enemy["phase"], target_enemy["wave"],
                target_enemy["enemy_index"], character["phase_xp_budget"],
                character["current_difficulty"],
            )
            db.execute(
                """INSERT OR IGNORE INTO card_xp_orbs
                   (character_id, phase, wave, world_x, world_y, xp_value, source_key)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    character["id"], target_enemy["phase"], target_enemy["wave"],
                    candidate_x, candidate_y, CARD_XP_PER_ORB,
                    f"enemy:{target_enemy['id']}",
                ),
            )
        if is_primary_target:
            affected_enemies[0]["world_x"] = candidate_x
            affected_enemies[0]["world_y"] = candidate_y
            affected_enemies[0]["position_changed"] = True
        else:
            affected_enemies.append({
                "id": target_enemy["id"], "hp": target_hp,
                "alive": not target_defeated, "damage": dealt,
                "world_x": candidate_x, "world_y": candidate_y,
                "position_changed": True,
                "root_duration_ms": root_duration_ms,
            })
    any_defeated = bool(defeated_enemy_ids)
    xp_gained = (
        enemy_experience_reward(
            enemy["phase"], enemy["wave"], enemy["enemy_index"],
            character["phase_xp_budget"], character["current_difficulty"],
        ) if defeated else 0
    ) + secondary_xp
    level, experience, levels_gained = character["level"], character["experience"], 0
    legacy_points_gained = 0
    legacy_milestones_gained = 0
    auto_allocated = 0
    health = character["current_health"]
    mana = (
        character["current_mana"]
        if pending_attack and pending_attack.get("mana_spent")
        else character["current_mana"] - mana_cost
    )
    for defeated_id in defeated_enemy_ids:
        credit_gold_monster_drop(
            db,
            character["user_id"],
            character["id"],
            defeated_id,
            enemy_level(character["current_phase"], character["current_wave"]),
        )
    damage_dealt += secondary_damage
    life_steal_healing = (
        0 if pending_attack and pending_attack.get("no_life_steal")
        else round(damage_dealt * combat_stats["life_steal"])
    )
    healing = life_steal_healing
    if skill:
        skill_healing = (
            round(damage_dealt * skill.get("heal_damage_fraction", 0))
            + round(max_health * skill.get("heal_max_health_fraction", 0))
        )
        healing += round(skill_healing * (1 + combat_stats["skill_healing"]))
    if healing:
        health_before_healing = health
        health = min(max_health, health + healing)
        life_stolen = min(life_steal_healing, max_health - health_before_healing)
    else:
        life_stolen = 0
    if skill:
        if any_defeated:
            mana = min(
                max_mana,
                mana + round(mana_cost * skill.get("mana_refund_on_kill_fraction", 0)),
            )
    if any_defeated:
        level, experience, levels_gained = add_experience(level, experience, xp_gained)
        legacy_points_gained, legacy_milestones_gained = award_legacy_points(
            db, character["id"], character["level"], level
        )
        _, auto_allocated = award_attribute_points(
            db, character["id"], levels_gained, _is_premium()
        )
        db.execute("UPDATE characters SET level = ?, experience = ? WHERE id = ?",
                   (level, experience, character["id"]))
        refreshed = db.execute("SELECT * FROM characters WHERE id = ?", (character["id"],)).fetchone()
        if levels_gained:
            combat_stats = _combat_stats(refreshed, active_card_ids)
            max_health, max_mana = combat_stats["max_health"], combat_stats["max_mana"]
        if defeated:
            db.execute(
                """INSERT OR IGNORE INTO card_xp_orbs
                   (character_id, phase, wave, world_x, world_y, xp_value, source_key)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (character["id"], character["current_phase"], character["current_wave"],
                 drop_x, drop_y, CARD_XP_PER_ORB, f"enemy:{enemy_id}"),
            )
    if critical and combat_stats["critical_heal"]:
        health = min(max_health, health + round(max_health * combat_stats["critical_heal"]))
    if any_defeated and not levels_gained and combat_stats["mana_on_kill"]:
        mana = min(max_mana, mana + round(max_mana * combat_stats["mana_on_kill"]))
    mana_potion_used = False
    if skill_id == "basic" and not (pending_attack and pending_attack.get("reflection")):
        _basic_attack_cooldowns[character["id"]] = now + cooldown
    elif skill:
        cooldown_refund = combat_stats["cooldown_refund_on_kill"] if any_defeated else 0
        if pending_attack and pending_attack.get("cooldown_reserved"):
            if cooldown_refund:
                _skill_cooldowns[cooldown_key] = min(
                    _skill_cooldowns.get(cooldown_key, now + cooldown),
                    now + max(0, cooldown - cooldown_refund),
                )
        else:
            _skill_cooldowns[cooldown_key] = now + max(0, cooldown - cooldown_refund)
    else:
        cooldown_refund = 0
    if mana_cost and not levels_gained:
        mana, mana_potion_used = _try_auto_potion(
            db, character, "mana", mana, max_mana
        )
    if levels_gained:
        health, mana = max_health, max_mana
    if mana_cost or health != character["current_health"] or mana != character["current_mana"]:
        db.execute("UPDATE characters SET current_mana = ?, current_health = ? WHERE id = ?",
                   (mana, health, character["id"]))
    active_count = len(_active_ids(character["id"]))
    remaining = db.execute(
        "SELECT COUNT(*) FROM wave_enemies WHERE character_id = ? AND phase = ? AND wave = ? AND alive = 1",
        (character["id"], character["current_phase"], character["current_wave"]),
    ).fetchone()[0]
    next_enemies = []
    next_phase, next_wave = character["current_phase"], character["current_wave"]
    phase_changed = False
    campaign_complete = False
    mission_complete = False
    mission_summary = None
    wave_heal_amount = 0
    preparation_until = character["phase_preparation_until"]
    if remaining == 0:
        if character["current_wave"] < WAVES_PER_PHASE and combat_stats["wave_heal"]:
            wave_heal_amount = round(max_health * combat_stats["wave_heal"])
            health = min(max_health, health + wave_heal_amount)
            db.execute("UPDATE characters SET current_health = ? WHERE id = ?",
                       (health, character["id"]))
        if next_wave == WAVES_PER_PHASE and mission_run is not None:
            mission_summary = complete_mission(
                db, character["user_id"], character["id"], next_phase,
                now=time.time(),
            )
            mission_complete = True
            campaign_complete = next_phase >= SEASON_1_PHASES
            preparation_until = 0
        else:
            if next_wave == WAVES_PER_PHASE:
                campaign_complete = next_phase >= SEASON_1_PHASES
                if not campaign_complete:
                    next_phase += 1
                    next_wave = 1
            else:
                next_wave += 1
            phase_changed = next_phase != character["current_phase"]
            count = (
                0 if campaign_complete
                else enemies_in_wave(
                    next_wave, next_phase, character["current_difficulty"]
                )
            )
            spawn_positions = enemy_spawn_positions(
                f"enemy:{character['id']}:{next_phase}:{next_wave}",
                count,
                *spawn_origin,
                phase=next_phase,
            )
            db.execute(
                "DELETE FROM wave_enemies WHERE character_id = ? AND phase = ? AND wave = ? AND enemy_index >= ?",
                (character["id"], next_phase, next_wave, count),
            )
            for index in range(count):
                enemy_hp = enemy_max_health(
                    next_phase, next_wave, WAVES_PER_PHASE,
                    character["current_difficulty"],
                )
                db.execute(
                    """INSERT INTO wave_enemies
                       (character_id, phase, wave, enemy_index, world_x, world_y, hp, max_hp, experience_reward)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                       ON CONFLICT(character_id, phase, wave, enemy_index) DO UPDATE SET
                         world_x = excluded.world_x, world_y = excluded.world_y,
                         hp = excluded.max_hp, max_hp = excluded.max_hp, alive = 1,
                         experience_reward = excluded.experience_reward""",
                    (character["id"], next_phase, next_wave, index,
                     *spawn_positions[index],
                     enemy_hp, enemy_hp, enemy_experience_reward(
                         next_phase, next_wave, index,
                         phase_xp_budget_for_level(level) if phase_changed else character["phase_xp_budget"],
                         character["current_difficulty"],
                     )),
                )
            next_enemies = [dict(row) for row in db.execute(
                """SELECT id, enemy_index, world_x, world_y, hp, max_hp, alive FROM wave_enemies
                   WHERE character_id = ? AND phase = ? AND wave = ? ORDER BY enemy_index""",
                (character["id"], next_phase, next_wave),
            ).fetchall()]
            for next_enemy in next_enemies:
                next_enemy["name"] = enemy_name(
                    next_enemy["enemy_index"], next_wave, WAVES_PER_PHASE,
                    phase=next_phase,
                )
                next_enemy["attack_style"] = enemy_attack_style(
                    next_enemy["enemy_index"], next_wave, WAVES_PER_PHASE,
                    phase=next_phase,
                )
                next_enemy["level"] = enemy_level(next_phase, next_wave)
                next_enemy["is_boss"] = encounter_type(next_phase, next_wave) == "boss"
                next_enemy["is_miniboss"] = encounter_type(next_phase, next_wave) == "miniboss"
                if next_enemy["is_boss"]:
                    next_enemy["affinity"] = boss_affinity(next_phase)
        if phase_changed or campaign_complete or mission_complete:
            refreshed = db.execute("SELECT * FROM characters WHERE id = ?", (character["id"],)).fetchone()
            active_card_ids.clear()
            combat_stats = _combat_stats(refreshed)
            max_health, max_mana = combat_stats["max_health"], combat_stats["max_mana"]
            health, mana = max_health, max_mana
            preparation_until = 0
            db.execute(
                """UPDATE characters SET current_phase = ?, current_wave = ?,
                   current_health = ?, current_mana = ?, phase_preparation_until = ?, phase_xp_budget = ?,
                   phase_intermission = ?, campaign_complete = ?,
                   card_experience = 0, pending_card_choices = 0
                   WHERE id = ?""",
                (
                    next_phase, next_wave, health, mana, preparation_until,
                    phase_xp_budget_for_level(level),
                    int(phase_changed or mission_complete),
                    int(campaign_complete), character["id"],
                ),
            )
            db.execute("DELETE FROM temporary_upgrades WHERE character_id = ?", (character["id"],))
            db.execute("DELETE FROM card_offers WHERE character_id = ?", (character["id"],))
            db.execute("DELETE FROM card_offer_history WHERE character_id = ?", (character["id"],))
            db.execute("DELETE FROM card_xp_orbs WHERE character_id = ? AND source_key != ?",
                       (character["id"], f"enemy:{enemy_id}"))
            db.execute("UPDATE characters SET card_experience = 0, pending_card_choices = 0 WHERE id = ?",
                       (character["id"],))
            _card_attack_streaks.pop(character["id"], None)
        else:
            db.execute("UPDATE characters SET current_phase = ?, current_wave = ? WHERE id = ?",
                       (next_phase, next_wave, character["id"]))
    active_effect = _activate_skill_effect(character["id"], skill) if skill else None
    effect_kind = skill.get("effect_kind") if skill else None
    if effect_kind in {"echo_strikes", "combo"}:
        hit_count = max(
            1, int(skill.get("strike_count", skill.get("echo_count", 1)))
        )
    elif effect_kind == "chain":
        hit_count = 1 + len(secondary_targets)
    else:
        hit_count = 1 + len(secondary_targets)
    db.commit()
    orb_ids = defeated_enemy_ids if any_defeated else []
    orbs = []
    for defeated_id in orb_ids:
        orb = db.execute(
            """SELECT id, world_x, world_y FROM card_xp_orbs
               WHERE character_id = ? AND source_key = ?""",
            (character["id"], f"enemy:{defeated_id}"),
        ).fetchone()
        if orb:
            orbs.append(dict(orb))
    orb_row = db.execute(
        "SELECT id, world_x, world_y FROM card_xp_orbs WHERE character_id = ? AND source_key = ?",
        (character["id"], f"enemy:{enemy_id}"),
    ).fetchone() if defeated else None
    if phase_changed or campaign_complete or mission_complete:
        card_state = _base_state(db.execute("SELECT * FROM characters WHERE id = ?", (character["id"],)).fetchone())
    else:
        card_state = None
    fresh_points = db.execute("SELECT attribute_points FROM characters WHERE id = ?", (character["id"],)).fetchone()[0]
    payload = {"enemy_id": enemy_id, "hp": hp, "defeated": defeated,
               "damage": damage, "mana": mana, "max_mana": max_mana,
               "damage_type": attack_damage_type, "element": attack_element,
               "levels_gained": levels_gained, "attribute_points_gained": levels_gained * ATTRIBUTE_POINTS_PER_LEVEL,
               "attribute_points": fresh_points,
               "auto_allocated_attributes": auto_allocated,
               "health": health, "max_health": max_health,
               "mana_potion_used": mana_potion_used,
               "skill_id": skill_id,
               "requested_skill_id": requested_skill_id,
               "skill_name": skill["name"] if skill else "",
               "effect_kind": effect_kind,
               "effect_radius": skill.get("area_radius", 0) if skill else 0,
               "effect_center": (
                   {"x": spawn_origin[0], "y": spawn_origin[1]}
                   if effect_kind in {"repulse", "guard", "sanctuary", "evasion"}
                   else {"x": target_x, "y": target_y}
               ) if effect_kind else None,
               "hit_count": hit_count,
               "active_effect": active_effect,
               "shadow_summoned": shadow_summoned,
               "shadow_soldier_count": shadow_soldier_count,
               "shadow_support_damage": shadow_support["damage"],
               "affected_enemies": affected_enemies,
               "fallback": bool(fallback_reason),
               "fallback_reason": fallback_reason,
               "experience_gained": xp_gained, "level": level, "experience": experience,
               "life_stolen": life_stolen,
               "next_level_xp": experience_needed(level) if level < MAX_LEVEL else 0,
               "max_level": MAX_LEVEL,
               "legacy_points_gained": legacy_points_gained,
               "legacy_milestones_gained": legacy_milestones_gained,
               "levels_gained": levels_gained, "enemies_remaining": remaining,
               "boss_defeated": (
                   remaining == 0
                   and encounter_type(character["current_phase"], character["current_wave"]) == "boss"
               ),
               "is_boss_wave": encounter_type(next_phase, next_wave) == "boss",
               "is_miniboss_wave": encounter_type(next_phase, next_wave) == "miniboss",
               "phase_changed": phase_changed,
               "awaiting_phase_choice": bool(phase_changed and not mission_complete),
               "campaign_complete": campaign_complete,
               "mission_complete": mission_complete,
               "mission_summary": mission_summary,
               "phase_preparation_until": preparation_until,
               "monsters_remaining": (
                   0 if campaign_complete else len(next_enemies)
               ) if remaining == 0 else remaining,
               "card_experience_needed": card_xp_needed(active_count),
               "phase": next_phase if remaining == 0 else character["current_phase"],
               "wave": next_wave if remaining == 0 else character["current_wave"],
               "next_enemies": next_enemies,
               "drop_position": {"world_x": drop_x, "world_y": drop_y} if defeated else None,
               "wave_heal": wave_heal_amount,
               "critical": critical,
               "cooldown_ms": int(max(0, cooldown - cooldown_refund) * 1000) if skill else int(cooldown * 1000),
               "card_state": card_state,
               "orbs": orbs,
               "orb": {"id": orb_row["id"], "world_x": orb_row["world_x"], "world_y": orb_row["world_y"]}
                      if orb_row else None}
    socketio.emit("combat:enemy_updated", payload, to=_room(character["id"]))
    if mana_potion_used:
        socketio.emit("combat:potion_used", {"resource": "mana", "value": mana,
                       "maximum": max_mana}, to=_room(character["id"]))
    if pending_attack:
        _pending_player_attacks.pop(str(projectile_id), None)
    return {"ok": True, **payload}


@socketio.on("combat:resolve_player_projectile")
def resolve_player_projectile(data):
    if not _valid_csrf(data):
        return {"ok": False, "error": "Sua sessão expirou. Atualize a página."}
    attack_id = str(data.get("attack_id", ""))
    attack = _pending_player_attacks.get(attack_id)
    if attack is None or attack["sid"] != request.sid:
        return {"ok": False, "error": "Esse projétil não está mais ativo."}
    if int(time.time() * 1000) < attack["impact_at"] - 75:
        return {"ok": False, "early": True}
    result = attack_enemy({
        "projectile_id": attack_id,
        "csrf_token": data.get("csrf_token", ""),
    })
    if result.get("ok") or not result.get("busy") and not result.get("early"):
        _pending_player_attacks.pop(attack_id, None)
    return result


def _apply_enemy_damage(db, character, enemy_id, damage, is_projectile=False):
    active_card_ids = _active_ids(character["id"])
    stats = _combat_stats(character, active_card_ids)
    max_health, max_mana = stats["max_health"], stats["max_mana"]
    enemy = db.execute(
        """SELECT id, enemy_index, wave, phase, world_x, world_y, hp
           FROM wave_enemies WHERE id = ? AND character_id = ? AND alive = 1""",
        (enemy_id, character["id"]),
    ).fetchone()
    ranged_attack = bool(is_projectile or enemy and enemy_attack_style(
        enemy["enemy_index"], enemy["wave"], WAVES_PER_PHASE,
        phase=enemy["phase"],
    ) == "ranged")
    temporary_effect = _temporary_player_effects.get(character["id"], {})
    if temporary_effect.get("expires_at", 0) <= time.monotonic():
        _temporary_player_effects.pop(character["id"], None)
        temporary_effect = {}
    damage_reduction = stats["damage_reduction"]
    damage_reduction += temporary_effect.get("damage_reduction", 0)
    if ranged_attack:
        damage_reduction += stats["ranged_reduction"]
    current = db.execute(
        "SELECT current_health, current_mana FROM characters WHERE id = ?", (character["id"],)
    ).fetchone()
    if current["current_health"] <= max_health * .30:
        damage_reduction += stats["low_health_reduction"]
    damage_reduction = min(.65, damage_reduction)
    dodge_chance = min(
        .85, stats["dodge_chance"] + temporary_effect.get("dodge_chance", 0)
    )
    dodged = random.random() < dodge_chance
    damage_taken = 0 if dodged else max(1, round(damage * (1 - damage_reduction)))
    health = max(0, current["current_health"] - damage_taken)
    health, health_potion_used = _try_auto_potion(db, character, "health", health, max_health)
    death = health == 0
    if death:
        _temporary_player_effects.pop(character["id"], None)
        _shadow_summons.pop(character["id"], None)
    reflected_damage = 0
    reflected_attack_id = None
    reflected_hp = None
    if not death and not dodged and enemy and stats["damage_reflection"]:
        reflected_damage = round(damage_taken * stats["damage_reflection"])
        if reflected_damage:
            if reflected_damage >= enemy["hp"]:
                reflected_attack_id = secrets.token_urlsafe(18)
                now_ms = int(time.time() * 1000)
                _pending_player_attacks[reflected_attack_id] = {
                    "character_id": character["id"],
                    "phase": enemy["phase"],
                    "wave": enemy["wave"],
                    "sid": request.sid,
                    "damage": reflected_damage,
                    "critical": False,
                    "reflection": True,
                    "no_life_steal": True,
                    "impact_at": now_ms,
                    "expires_at": now_ms + 1500,
                    "attack_data": {
                        "enemy_id": enemy_id,
                        "enemy_x": enemy["world_x"],
                        "enemy_y": enemy["world_y"],
                        "player_x": enemy["world_x"],
                        "player_y": enemy["world_y"],
                        "skill_id": "basic",
                    },
                }
            else:
                reflected_hp = enemy["hp"] - reflected_damage
                db.execute(
                    "UPDATE wave_enemies SET hp = ? WHERE id = ?",
                    (reflected_hp, enemy_id),
                )
    mana = max_mana if death else current["current_mana"]
    phase, wave = character["current_phase"], character["current_wave"]
    if death:
        db.execute(
            """UPDATE mission_runs SET status = 'failed'
               WHERE character_id = ? AND status = 'active'""",
            (character["id"],),
        )
        db.execute("DELETE FROM temporary_upgrades WHERE character_id = ?", (character["id"],))
        db.execute("DELETE FROM card_offers WHERE character_id = ?", (character["id"],))
        db.execute("DELETE FROM card_offer_history WHERE character_id = ?", (character["id"],))
        db.execute("DELETE FROM card_xp_orbs WHERE character_id = ?", (character["id"],))
        db.execute("UPDATE characters SET card_experience = 0, pending_card_choices = 0 WHERE id = ?",
                   (character["id"],))
        _card_attack_streaks.pop(character["id"], None)
        for key in [key for key in _skill_cooldowns if key[0] == character["id"]]:
            _skill_cooldowns.pop(key, None)
        _basic_attack_cooldowns.pop(character["id"], None)
        _dash_cooldowns.pop(character["id"], None)
        stats = _combat_stats(character)
        max_health, max_mana = stats["max_health"], stats["max_mana"]
        mana = max_mana
        wave = 1
        health = max_health
        db.execute(
            """UPDATE characters SET current_health = ?, current_mana = ?, current_wave = 1,
               death_intermission = 1 WHERE id = ?""",
            (health, mana, character["id"]),
        )
        db.execute(
            "UPDATE wave_enemies SET hp = max_hp, alive = 1 WHERE character_id = ? AND phase = ?",
            (character["id"], phase),
        )
        next_enemies = [dict(row) for row in db.execute(
            """SELECT id, enemy_index, world_x, world_y, hp, max_hp, alive FROM wave_enemies
               WHERE character_id = ? AND phase = ? AND wave = 1 ORDER BY enemy_index""",
            (character["id"], phase),
        ).fetchall()]
        for next_enemy in next_enemies:
            next_enemy["name"] = enemy_name(
                next_enemy["enemy_index"], 1, WAVES_PER_PHASE, phase=phase
            )
            next_enemy["attack_style"] = enemy_attack_style(
                next_enemy["enemy_index"], 1, WAVES_PER_PHASE, phase=phase
            )
            next_enemy["level"] = enemy_level(phase, 1)
            next_enemy["is_boss"] = False
            next_enemy["is_miniboss"] = False
        for key in [key for key in _enemy_attack_cooldowns if key[0] == character["id"]]:
            _enemy_attack_cooldowns.pop(key, None)
            _enemy_attack_cycles.pop(key, None)
        for attack_id in [attack_id for attack_id, attack in _pending_enemy_attacks.items()
                          if attack["character_id"] == character["id"]]:
            _pending_enemy_attacks.pop(attack_id, None)
        for attack_id in [attack_id for attack_id, attack in _pending_player_attacks.items()
                          if attack["character_id"] == character["id"]]:
            _pending_player_attacks.pop(attack_id, None)
    else:
        db.execute("UPDATE characters SET current_health = ? WHERE id = ?", (health, character["id"]))
        next_enemies = []
    db.commit()
    card_state = None
    if death:
        updated = db.execute("SELECT * FROM characters WHERE id = ?", (character["id"],)).fetchone()
        card_state = _base_state(updated)
    payload = {
        "health": health, "max_health": max_health, "mana": mana, "max_mana": max_mana,
        "damage": damage_taken, "incoming_damage": damage, "dodged": dodged,
        "reflected_damage": reflected_damage,
        "health_potion_used": health_potion_used,
        "death": death, "enemy_id": enemy_id, "phase": phase, "wave": wave,
        "next_enemies": next_enemies, "card_state": card_state,
    }
    socketio.emit("combat:player_damaged", payload, to=_room(character["id"]))
    if reflected_hp is not None:
        socketio.emit(
            "combat:enemy_reflected",
            {
                "enemy_id": enemy_id,
                "hp": reflected_hp,
                "damage": reflected_damage,
            },
            to=_room(character["id"]),
        )
    if health_potion_used:
        socketio.emit("combat:potion_used", {"resource": "health", "value": health,
                       "maximum": max_health}, to=_room(character["id"]))
    if reflected_attack_id:
        reflection_result = attack_enemy({
            "projectile_id": reflected_attack_id,
            "csrf_token": session.get("csrf_token", ""),
        })
        if not reflection_result.get("ok"):
            _pending_player_attacks.pop(reflected_attack_id, None)
            return {
                "ok": False,
                "error": reflection_result.get("error", "Não foi possível aplicar o dano refletido."),
            }
    return {"ok": True, **payload}


@socketio.on("combat:request_enemy_attack")
def request_enemy_attack(data):
    if not _valid_csrf(data):
        return {"ok": False, "error": "Sua sessão expirou. Atualize a página."}
    character = _character()
    if character is None:
        return {"ok": False, "error": "Personagem inválido."}
    if (active_mission_run(
            get_db(), character["user_id"], character["id"]
        ) is None and not current_app.config.get("TESTING")):
        return {"ok": False, "error": "Nenhuma missão ativa."}
    if character["phase_preparation_until"] > time.time() or character["phase_intermission"] or character["death_intermission"]:
        return {"ok": False, "intermission": True}
    try:
        enemy_id = int(data.get("enemy_id"))
        enemy_x, enemy_y = float(data.get("enemy_x")), float(data.get("enemy_y"))
        target_x, target_y = float(data.get("target_x")), float(data.get("target_y"))
        if not all(math.isfinite(value) for value in (enemy_x, enemy_y, target_x, target_y)):
            raise ValueError("Posição inválida")
    except (TypeError, ValueError):
        return {"ok": False, "error": "Ataque inválido."}
    enemy_x, enemy_y = clamp_map_position(
        enemy_x, enemy_y, character["current_phase"]
    )
    target_x, target_y = clamp_map_position(
        target_x, target_y, character["current_phase"]
    )
    db = get_db()
    enemy = db.execute(
        """SELECT id, enemy_index, world_x, world_y, phase, wave FROM wave_enemies
           WHERE id = ? AND character_id = ? AND phase = ? AND wave = ? AND alive = 1""",
        (enemy_id, character["id"], character["current_phase"], character["current_wave"]),
    ).fetchone()
    if enemy is None:
        return {"ok": False, "error": "Esse inimigo não está ativo."}
    active_ids = {row[0] for row in db.execute(
        """SELECT id FROM wave_enemies WHERE character_id = ? AND phase = ? AND wave = ? AND alive = 1""",
        (character["id"], character["current_phase"], character["current_wave"]),
    ).fetchall()}
    for key in [key for key in _enemy_attack_cooldowns if key[0] == character["id"] and key[1] not in active_ids]:
        _enemy_attack_cooldowns.pop(key, None)
        _enemy_attack_cycles.pop(key, None)
    style = enemy_attack_style(
        enemy["enemy_index"], enemy["wave"], WAVES_PER_PHASE,
        phase=enemy["phase"],
    )
    max_range = {"melee": 175, "ranged": 420, "miniboss": 500, "boss": 520}[style]
    if math.hypot(target_x - enemy_x, target_y - enemy_y) > max_range:
        return {"ok": False, "out_of_range": True}
    created_at = int(time.time() * 1000)
    for old_id, old_attack in list(_pending_enemy_attacks.items()):
        if old_attack["expires_at"] <= created_at:
            _pending_enemy_attacks.pop(old_id, None)
    cycle_key = (character["id"], enemy_id)
    cycle = _enemy_attack_cycles.get(cycle_key, 0)
    attack_cycle = {
        "melee": ("melee_slam",),
        "ranged": ("ranged_shadow_bolt",),
        "miniboss": ("miniboss_groundbreak", "miniboss_shards"),
        "boss": ("boss_shadowfall", "boss_rift_line"),
    }[style]
    attack_type = attack_cycle[cycle % len(attack_cycle)]
    definition = ENEMY_ATTACKS[attack_type]
    now = time.monotonic()
    cooldown_key = (character["id"], enemy_id)
    remaining_cooldown = _enemy_attack_cooldowns.get(cooldown_key, 0) - now
    if remaining_cooldown > 0:
        return {"ok": False, "cooldown": True, "retry_after_ms": int(remaining_cooldown * 1000) + 50}
    if any(attack["character_id"] == character["id"] and attack["enemy_id"] == enemy_id
           for attack in _pending_enemy_attacks.values()):
        return {"ok": False, "pending": True}

    areas = []
    if style == "boss" and attack_type == "boss_shadowfall":
        direction = math.atan2(target_y - enemy_y, target_x - enemy_x)
        side_x, side_y = -math.sin(direction) * 82, math.cos(direction) * 82
        for offset in (-1, 0, 1):
            area_x, area_y = clamp_map_position(
                target_x + side_x * offset,
                target_y + side_y * offset,
                character["current_phase"],
            )
            areas.append({"x": area_x, "y": area_y, "radius": definition["radius"]})
    elif style == "boss":
        for step in (0.28, 0.50, 0.72, 0.94):
            area_x, area_y = clamp_map_position(
                enemy_x + (target_x - enemy_x) * step,
                enemy_y + (target_y - enemy_y) * step,
                character["current_phase"],
            )
            areas.append({"x": area_x, "y": area_y, "radius": definition["radius"]})
    elif style == "miniboss" and attack_type == "miniboss_shards":
        direction = math.atan2(target_y - enemy_y, target_x - enemy_x)
        side_x, side_y = -math.sin(direction) * 64, math.cos(direction) * 64
        for offset in (-1, 0, 1):
            area_x, area_y = clamp_map_position(
                target_x + side_x * offset,
                target_y + side_y * offset,
                character["current_phase"],
            )
            areas.append({"x": area_x, "y": area_y, "radius": definition["radius"]})
    else:
        areas.append({"x": target_x, "y": target_y, "radius": definition["radius"]})
    impact_at = created_at + definition["windup_ms"]
    projectiles = []
    if definition["projectile"]:
        for area in areas:
            if style == "boss" or attack_type == "miniboss_shards":
                origin_x, origin_y = area["x"], area["y"] - 340
            else:
                origin_x, origin_y = enemy_x, enemy_y
            projectiles.append({
                "origin_x": origin_x, "origin_y": origin_y,
                "target_x": area["x"], "target_y": area["y"],
                "flight_ms": definition["windup_ms"] - 180,
            })
    attack_id = secrets.token_urlsafe(18)
    payload = {
        "ok": True, "attack_id": attack_id, "enemy_id": enemy_id,
        "attack_type": attack_type, "name": definition["name"], "style": style,
        "areas": areas, "projectiles": projectiles,
        "created_at": created_at, "impact_at": impact_at,
        "damage": scale_enemy_attack_damage(
            definition["damage"], enemy["phase"], enemy["wave"],
            character["current_difficulty"],
        ),
        "cooldown_ms": int(definition["cooldown"] * 1000),
    }
    _enemy_attack_cooldowns[cooldown_key] = now + definition["cooldown"]
    _enemy_attack_cycles[cycle_key] = cycle + 1
    _pending_enemy_attacks[attack_id] = {
        **payload, "character_id": character["id"], "phase": enemy["phase"],
        "wave": enemy["wave"], "expires_at": impact_at + 1500,
    }
    socketio.emit("combat:enemy_telegraph", payload, to=_room(character["id"]), skip_sid=request.sid)
    return payload


@socketio.on("combat:resolve_enemy_attack")
def resolve_enemy_attack(data):
    if not _valid_csrf(data):
        return {"ok": False, "error": "Sua sessão expirou. Atualize a página."}
    character = _character()
    if character is None:
        return {"ok": False, "error": "Personagem inválido."}
    attack_id = str(data.get("attack_id", ""))
    attack = _pending_enemy_attacks.get(attack_id)
    if attack is None or attack["character_id"] != character["id"]:
        return {"ok": False, "error": "Esse ataque não está mais ativo."}
    if (character["phase_preparation_until"] > time.time()
            or character["phase_intermission"] or character["death_intermission"]
            or (active_mission_run(
                get_db(), character["user_id"], character["id"]
            ) is None and not current_app.config.get("TESTING"))):
        _pending_enemy_attacks.pop(attack_id, None)
        return {"ok": False, "intermission": True}
    if attack.get("resolving"):
        return {"ok": False, "pending": True}
    if (character["current_phase"], character["current_wave"]) != (attack["phase"], attack["wave"]):
        _pending_enemy_attacks.pop(attack_id, None)
        return {"ok": False, "error": "A onda do ataque já terminou."}
    now_ms = int(time.time() * 1000)
    if now_ms < attack["impact_at"] - 75:
        return {"ok": False, "early": True}
    if now_ms > attack["expires_at"]:
        _pending_enemy_attacks.pop(attack_id, None)
        return {"ok": False, "expired": True}
    try:
        player_x, player_y = float(data.get("player_x")), float(data.get("player_y"))
        if not math.isfinite(player_x) or not math.isfinite(player_y):
            raise ValueError("Posição inválida")
    except (TypeError, ValueError):
        _pending_enemy_attacks.pop(attack_id, None)
        return {"ok": False, "error": "Posição inválida."}
    player_x, player_y = clamp_map_position(
        player_x, player_y, character["current_phase"]
    )
    hit = any(
        math.hypot(player_x - area["x"], player_y - area["y"]) <= area["radius"] + 13
        for area in attack["areas"]
    )
    if not hit:
        _pending_enemy_attacks.pop(attack_id, None)
        return {"ok": True, "hit": False, "attack_id": attack_id}
    if character["phase_preparation_until"] > time.time() or character["phase_intermission"] or character["death_intermission"]:
        _pending_enemy_attacks.pop(attack_id, None)
        return {"ok": False, "intermission": True}
    db = get_db()
    attack["resolving"] = True
    if not _begin_write(db):
        attack["resolving"] = False
        return {"ok": False, "busy": True}
    active_enemy = db.execute(
        """SELECT 1 FROM wave_enemies WHERE id = ? AND character_id = ?
           AND phase = ? AND wave = ? AND alive = 1""",
        (attack["enemy_id"], character["id"], attack["phase"], attack["wave"]),
    ).fetchone()
    if active_enemy is None:
        db.rollback()
        _pending_enemy_attacks.pop(attack_id, None)
        return {"ok": False, "error": "O inimigo não está mais ativo."}
    _pending_enemy_attacks.pop(attack_id, None)
    attack_definition = ENEMY_ATTACKS.get(attack["attack_type"], {})
    payload = _apply_enemy_damage(
        db, character, attack["enemy_id"], attack["damage"],
        is_projectile=bool(attack_definition.get("projectile")),
    )
    payload.update({"hit": True, "attack_id": attack_id, "attack_name": attack["name"]})
    return payload


@socketio.on("combat:auto_potion:toggle")
def toggle_auto_potion(data):
    if not _valid_csrf(data):
        return {"ok": False, "error": "Sua sessão expirou. Atualize a página."}
    character = _character()
    if character is None:
        return {"ok": False, "error": "Personagem inválido."}
    if not _is_premium():
        return {"ok": False, "error": "As poções automáticas exigem o benefício especial."}
    resource = data.get("resource")
    if resource not in ("health", "mana"):
        return {"ok": False, "error": "Tipo de auto-poção inválido."}
    enabled = data.get("enabled") is True
    column = "auto_health_potion" if resource == "health" else "auto_mana_potion"
    db = get_db()
    if not _begin_write(db):
        return {"ok": False, "busy": True, "error": "O banco está ocupado. Tente novamente."}
    db.execute(f"UPDATE characters SET {column} = ? WHERE id = ?",
               (int(enabled), character["id"]))
    db.commit()
    payload = {"ok": True, "resource": resource, "enabled": enabled}
    socketio.emit("combat:auto_potion_state", payload, to=_room(character["id"]))
    return payload


@socketio.on("account:toggle_test_premium")
def toggle_test_premium(data):
    if not current_app.config.get("ENABLE_PREMIUM_TEST_TOGGLE", False):
        return {"ok": False, "error": "O controle temporário de benefícios está desativado."}
    if not _valid_csrf(data):
        return {"ok": False, "error": "Sua sessão expirou. Atualize a página."}
    user_id = session.get("user_id")
    if user_id is None:
        return {"ok": False, "error": "Entre na conta para alterar o modo de teste."}
    db = get_db()
    if not _begin_write(db):
        return {"ok": False, "busy": True, "error": "O banco está ocupado. Tente novamente."}
    user = db.execute("SELECT is_premium FROM users WHERE id = ?", (user_id,)).fetchone()
    if user is None:
        db.rollback()
        return {"ok": False, "error": "Conta inválida."}
    enabled = not bool(user["is_premium"])
    db.execute("UPDATE users SET is_premium = ? WHERE id = ?", (int(enabled), user_id))
    db.commit()
    return {"ok": True, "is_premium": enabled}


@socketio.on("combat:dash")
def request_dash(data):
    if not _valid_csrf(data):
        return {"ok": False, "error": "Sua sessão expirou. Atualize a página."}
    character = _character()
    if character is None:
        return {"ok": False, "error": "Personagem inválido."}
    if character["phase_intermission"] or character["death_intermission"]:
        return {"ok": False, "error": "Escolha como deseja continuar antes de iniciar a fase."}
    if character["phase_preparation_until"] > time.time():
        return {"ok": False, "error": "Avanço indisponível durante a preparação."}
    now = time.monotonic()
    if _dash_cooldowns.get(character["id"], 0) > now:
        return {"ok": False, "error": "Avanço em recarga."}
    stats = _combat_stats(character)
    cooldown = cooldown_for_agility(
        DASH_COOLDOWN * stats["cooldown_multiplier"], character["agility"]
    )
    _dash_cooldowns[character["id"]] = now + cooldown
    return {"ok": True, "cooldown": cooldown}
