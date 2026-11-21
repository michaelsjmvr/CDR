"""Routes for the authenticated game prototype."""

import json
import time
from datetime import datetime, timezone

from flask import (
    current_app,
    Blueprint,
    abort,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from .classes import CLASSES
from .campaign import (
    SEASON_1_ACTS,
    SEASON_1_PHASES,
    campaign_map_for_phase,
    encounter_type,
    season_act_for_phase,
)
from .abilities import available_class_skills, normalized_skill_slots
from .cards import CARDS, draw_card_offer, recommend_card
from .combat import PHASE_PREPARATION_SECONDS, boss_affinity, enemy_attack_style, enemy_level, enemy_name, enemy_max_health, enemy_spawn_positions, derived_combat_stats
from .database import get_db
from .map_geometry import (
    save_terminal_vilar_map_config,
    terminal_vilar_collision_data,
    terminal_vilar_collides,
    terminal_vilar_map_config,
)
from .progression import (
    CARD_XP_PER_ORB,
    CARD_XP_PER_ORB_PREMIUM,
    CARD_AUTO_PICK_SECONDS,
    card_xp_needed,
    MAX_LEVEL,
    WAVES_PER_PHASE,
    enemies_in_wave,
    phase_xp_budget_for_level,
    add_experience,
    award_attribute_points,
    experience_needed,
    enemy_experience_reward,
    wave_experience_reward,
)
from .security import validate_csrf
from .talents import NODE_INDEX
from .mission_system import (
    DIFFICULTIES,
    InventoryCapacityError,
    INVENTORY_CAPACITY,
    active_account_mission_run,
    active_mission_run,
    can_access_mission,
    difficulty_state,
    discard_inventory_item,
    format_gold,
    pending_mission_run,
    resolve_staging_inventory,
    sell_inventory_item,
)


game_blueprint = Blueprint("game", __name__)
MISSION_COUNTDOWN_SECONDS = 5


@game_blueprint.get("/jogo")
def room():
    if not g.user:
        flash("Entre na sua conta para acessar o jogo.", "info")
        return redirect(url_for("auth.home"))
    session["in_lobby"] = False
    character_id = session.get("selected_character_id")
    db = get_db()
    character = db.execute(
        """SELECT id, name, class_id, level, experience, specialization_id,
                  current_phase, current_wave, current_difficulty, gold, legacy_points,
                  strength, vitality, energy, attribute_points,
                  card_experience, pending_card_choices, card_offer_revision, current_health, current_mana,
                  phase_preparation_until, phase_intermission, death_intermission, agility,
                  phase_xp_budget,
                  auto_health_potion, auto_mana_potion, campaign_complete
           FROM characters WHERE id = ? AND user_id = ?""",
        (character_id, g.user["id"]),
    ).fetchone() if character_id is not None else None
    if character is None:
        session.pop("selected_character_id", None)
        flash("Selecione um personagem antes de entrar na sala.", "info")
        return redirect(url_for("characters.index"))
    character = dict(character)
    run = active_mission_run(db, g.user["id"], character["id"])
    if run is None:
        pending = pending_mission_run(db, g.user["id"])
        if pending is not None:
            return redirect(url_for("game.post_mission", run_id=pending["id"]))
        if not current_app.config.get("TESTING"):
            flash("Escolha uma fase liberada na Sala de Espera antes de entrar.", "info")
            return redirect(url_for("game.lobby"))
        difficulty = character["current_difficulty"]
    else:
        if (run["phase"] != character["current_phase"]
                or run["difficulty"] != character["current_difficulty"]
                or not can_access_mission(
                    db, g.user["id"], run["difficulty"], run["phase"]
                )):
            flash("A missão ativa não corresponde ao progresso liberado.", "error")
            return redirect(url_for("game.lobby"))
        difficulty = run["difficulty"]
    if character["campaign_complete"]:
        enemy_rows = []
        enemy_count = 0
    else:
        enemy_rows = db.execute(
            "SELECT id, enemy_index, world_x, world_y FROM wave_enemies WHERE character_id = ? AND phase = ? AND wave = ? AND alive = 1",
            (character["id"], character["current_phase"], character["current_wave"]),
        ).fetchall()
        enemy_count = enemies_in_wave(
            character["current_wave"], character["current_phase"], difficulty
        )
    purchased_talents = {
        row["talent_id"] for row in db.execute(
            "SELECT talent_id FROM character_talents WHERE character_id = ?",
            (character["id"],),
        ).fetchall()
    }
    skill_options = available_class_skills(
        character["class_id"], character["specialization_id"], purchased_talents
    )
    saved_skill_slots = [
        "basic",
        g.user["skill_slot_2"], g.user["skill_slot_3"], g.user["skill_slot_4"],
    ]
    class_skill_slots = normalized_skill_slots(
        character["class_id"], character["specialization_id"],
        purchased_talents, saved_skill_slots,
    )
    skills_by_id = {skill["id"]: skill for skill in skill_options}
    equipped_skills = [
        skills_by_id.get(skill_id) for skill_id in class_skill_slots[1:]
    ]

    current_encounter = encounter_type(
        character["current_phase"], character["current_wave"]
    )
    is_boss_wave = current_encounter == "boss"
    is_miniboss_wave = current_encounter == "miniboss"
    if not character["phase_xp_budget"]:
        db.execute("UPDATE characters SET phase_xp_budget = ? WHERE id = ?", (phase_xp_budget_for_level(character["level"]), character["id"]))
        character = dict(db.execute("SELECT * FROM characters WHERE id = ?", (character["id"],)).fetchone())
    if not character["campaign_complete"]:
        db.execute(
            "DELETE FROM wave_enemies WHERE character_id = ? AND phase = ? AND wave = ? AND enemy_index >= ?",
            (character["id"], character["current_phase"], character["current_wave"], enemy_count),
        )
        db.commit()
    old_cluster = bool(enemy_rows) and (
        any(((row["world_x"] - 1200) ** 2 + (row["world_y"] - 900) ** 2) ** 0.5 < 380 for row in enemy_rows)
        or any(
            ((left["world_x"] - right["world_x"]) ** 2 + (left["world_y"] - right["world_y"]) ** 2) ** 0.5 < 92
            for index, left in enumerate(enemy_rows)
            for right in enemy_rows[index + 1:]
        )
        or (
            character["current_phase"] == 1
            and any(
                terminal_vilar_collides(row["world_x"], row["world_y"], 28)
                for row in enemy_rows
            )
        )
    )
    if character["campaign_complete"]:
        enemies = []
    elif old_cluster:
        spawn_positions = enemy_spawn_positions(
            f"enemy:{character['id']}:{character['current_phase']}:{character['current_wave']}",
            enemy_count,
            phase=character["current_phase"],
        )
        for enemy in enemy_rows:
            db.execute(
                "UPDATE wave_enemies SET world_x = ?, world_y = ? WHERE id = ? AND alive = 1",
                (*spawn_positions[enemy["enemy_index"]], enemy["id"]),
            )
        db.commit()
    elif not enemy_rows:
        spawn_positions = enemy_spawn_positions(
            f"enemy:{character['id']}:{character['current_phase']}:{character['current_wave']}",
            enemy_count,
            phase=character["current_phase"],
        )
        enemy_hp = enemy_max_health(
            character["current_phase"], character["current_wave"],
            WAVES_PER_PHASE, difficulty,
        )
        for enemy_index in range(enemy_count):
            db.execute(
                """INSERT INTO wave_enemies
                   (character_id, phase, wave, enemy_index, world_x, world_y, hp, max_hp, experience_reward)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                   ON CONFLICT(character_id, phase, wave, enemy_index) DO UPDATE SET
                     world_x = excluded.world_x, world_y = excluded.world_y,
                     hp = excluded.max_hp, max_hp = excluded.max_hp, alive = 1,
                     experience_reward = excluded.experience_reward""",
                (character["id"], character["current_phase"], character["current_wave"], enemy_index,
                 *spawn_positions[enemy_index],
                 enemy_hp, enemy_hp, enemy_experience_reward(
                     character["current_phase"], character["current_wave"],
                     enemy_index, character["phase_xp_budget"], difficulty,
                 )),
            )
        db.commit()
    stored_indices = {
        row["enemy_index"] for row in db.execute(
            """SELECT enemy_index FROM wave_enemies
               WHERE character_id = ? AND phase = ? AND wave = ?""",
            (character["id"], character["current_phase"], character["current_wave"]),
        ).fetchall()
    }
    missing_indices = [index for index in range(enemy_count) if index not in stored_indices]
    if missing_indices:
        spawn_positions = enemy_spawn_positions(
            f"enemy:{character['id']}:{character['current_phase']}:{character['current_wave']}",
            enemy_count,
            phase=character["current_phase"],
        )
        enemy_hp = enemy_max_health(
            character["current_phase"], character["current_wave"],
            WAVES_PER_PHASE, difficulty,
        )
        for enemy_index in missing_indices:
            db.execute(
                """INSERT INTO wave_enemies
                   (character_id, phase, wave, enemy_index, world_x, world_y, hp, max_hp, experience_reward)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (character["id"], character["current_phase"], character["current_wave"], enemy_index,
                 *spawn_positions[enemy_index], enemy_hp, enemy_hp,
                 enemy_experience_reward(
                     character["current_phase"], character["current_wave"],
                     enemy_index, character["phase_xp_budget"], difficulty,
                 )),
            )
        db.commit()
    enemies = [] if character["campaign_complete"] else [
        dict(row) for row in db.execute(
            """SELECT id, enemy_index, world_x, world_y, hp, max_hp, alive FROM wave_enemies
               WHERE character_id = ? AND phase = ? AND wave = ? ORDER BY enemy_index""",
            (character["id"], character["current_phase"], character["current_wave"]),
        ).fetchall()
    ]
    for enemy in enemies:
        expected_hp = enemy_max_health(
            character["current_phase"], character["current_wave"],
            WAVES_PER_PHASE, difficulty,
        )
        if enemy["max_hp"] != expected_hp:
            ratio = enemy["hp"] / enemy["max_hp"] if enemy["max_hp"] else 1
            enemy["max_hp"] = expected_hp
            enemy["hp"] = min(expected_hp, max(0, round(expected_hp * ratio)))
            db.execute("UPDATE wave_enemies SET hp = ?, max_hp = ? WHERE id = ?", (enemy["hp"], expected_hp, enemy["id"]))
    db.commit()
    for enemy in enemies:
        enemy["name"] = enemy_name(
            enemy["enemy_index"], character["current_wave"], WAVES_PER_PHASE,
            phase=character["current_phase"],
        )
        enemy["attack_style"] = enemy_attack_style(
            enemy["enemy_index"], character["current_wave"], WAVES_PER_PHASE,
            phase=character["current_phase"],
        )
        enemy["level"] = enemy_level(character["current_phase"], character["current_wave"])
        enemy["is_boss"] = is_boss_wave
        enemy["is_miniboss"] = is_miniboss_wave
        if enemy["is_boss"]:
            enemy["affinity"] = boss_affinity(character["current_phase"])

    active_rows = db.execute(
        "SELECT upgrade_key FROM temporary_upgrades WHERE character_id = ? ORDER BY id",
        (character["id"],),
    ).fetchall()
    active_card_list = [row["upgrade_key"] for row in active_rows]
    active_card_ids = set(active_card_list)
    purchased_talents = {
        row["talent_id"] for row in db.execute(
            "SELECT talent_id FROM character_talents WHERE character_id = ?",
            (character["id"],),
        ).fetchall()
    }
    combat_stats = derived_combat_stats(character, active_card_ids, purchased_talents)
    clamped_health = min(max(0, character["current_health"]), combat_stats["max_health"])
    clamped_mana = min(max(0, character["current_mana"]), combat_stats["max_mana"])
    if clamped_health != character["current_health"] or clamped_mana != character["current_mana"]:
        db.execute(
            "UPDATE characters SET current_health = ?, current_mana = ? WHERE id = ?",
            (clamped_health, clamped_mana, character["id"]),
        )
        db.commit()
        character["current_health"] = clamped_health
        character["current_mana"] = clamped_mana
    if (not active_card_ids and character["pending_card_choices"] <= 0
            and not character["phase_intermission"] and not character["death_intermission"]):
        # A fresh temporary collection always exposes its first offer to the player.
        db.execute(
            "UPDATE characters SET pending_card_choices = 1 WHERE id = ?",
            (character["id"],),
        )
        character["pending_card_choices"] = 1
        db.commit()
    card_offer_available = not character["phase_intermission"] and not character["death_intermission"] and (
        character["pending_card_choices"] > 0 or not active_card_ids
    )
    offer = db.execute(
        """SELECT id, card_ids, recommended_card_id, auto_pick_at, auto_pick_version,
                  selected_card_id, resolved FROM card_offers
           WHERE character_id = ? AND phase = ? AND wave = ?""",
        (character["id"], character["current_phase"], character["current_wave"]),
    ).fetchone()
    if card_offer_available and offer is not None and offer["resolved"]:
        db.execute("DELETE FROM card_offers WHERE character_id = ? AND phase = ? AND wave = ?", (
            character["id"], character["current_phase"], character["current_wave"]
        ))
        db.commit()
        offer = None
    elif not card_offer_available and offer is not None and not offer["resolved"]:
        db.execute("UPDATE card_offers SET resolved = 1 WHERE id = ?", (offer["id"],))
        db.commit()
        offer = None
    if card_offer_available and offer is None:
        is_premium = bool(g.user["is_premium"])
        previously_shown = {
            row["card_id"] for row in db.execute(
                """SELECT card_id FROM card_offer_history
                   WHERE character_id = ? AND phase = ? AND wave = ?""",
                (character["id"], character["current_phase"], character["current_wave"]),
            ).fetchall()
        }
        offer_ids = draw_card_offer(active_card_ids, excluded_card_ids=previously_shown)
        db.execute("BEGIN IMMEDIATE")
        db.execute(
            """DELETE FROM card_offer_history WHERE character_id = ?
               AND (phase != ? OR wave != ?)""",
            (character["id"], character["current_phase"], character["current_wave"]),
        )
        inserted_offer = db.execute(
            """INSERT OR IGNORE INTO card_offers
               (character_id, phase, wave, card_ids, recommended_card_id,
                auto_pick_at, auto_pick_version, created_at)
               VALUES (?, ?, ?, ?, ?, ?, 1, ?)""",
            (
                character["id"],
                character["current_phase"],
                character["current_wave"],
                json.dumps(offer_ids),
                recommend_card(
                    offer_ids, character["class_id"],
                    character["current_health"] / max(1, combat_stats["max_health"]),
                    character["current_wave"],
                    character["specialization_id"], purchased_talents,
                ),
                time.time() + CARD_AUTO_PICK_SECONDS if is_premium else None,
                datetime.now(timezone.utc).isoformat(),
            ),
        )
        if inserted_offer.rowcount:
            db.execute(
                "UPDATE characters SET card_offer_revision = card_offer_revision + 1 WHERE id = ?",
                (character["id"],),
            )
            db.executemany(
                """INSERT OR IGNORE INTO card_offer_history
                   (character_id, phase, wave, card_id) VALUES (?, ?, ?, ?)""",
                [
                    (character["id"], character["current_phase"], character["current_wave"], card_id)
                    for card_id in offer_ids
                ],
            )
        db.commit()
        offer = db.execute(
            """SELECT id, card_ids, recommended_card_id, auto_pick_at, auto_pick_version,
                      selected_card_id, resolved FROM card_offers
               WHERE character_id = ? AND phase = ? AND wave = ?""",
            (character["id"], character["current_phase"], character["current_wave"]),
        ).fetchone()

    if offer is not None and not offer["resolved"]:
        offer_ids = json.loads(offer["card_ids"])
        recommendation = recommend_card(
            offer_ids, character["class_id"],
            character["current_health"] / max(1, combat_stats["max_health"]),
            character["current_wave"],
            character["specialization_id"], purchased_talents,
        )
        deadline = offer["auto_pick_at"]
        timer_version = offer["auto_pick_version"] or 0
        if g.user["is_premium"] and timer_version < 1:
            deadline = max(time.time(), float(deadline) - CARD_AUTO_PICK_SECONDS) if deadline else time.time() + CARD_AUTO_PICK_SECONDS
            timer_version = 1
        elif g.user["is_premium"] and not deadline:
            deadline = time.time() + CARD_AUTO_PICK_SECONDS
        elif not g.user["is_premium"]:
            deadline = None
            timer_version = 1
        if (recommendation != offer["recommended_card_id"]
                or deadline != offer["auto_pick_at"]
                or timer_version != offer["auto_pick_version"]):
            db.execute(
                """UPDATE card_offers SET recommended_card_id = ?, auto_pick_at = ?, auto_pick_version = ?
                   WHERE id = ?""",
                (recommendation, deadline, timer_version, offer["id"]),
            )
            db.commit()
            offer = db.execute(
                """SELECT id, card_ids, recommended_card_id, auto_pick_at, auto_pick_version,
                          selected_card_id, resolved FROM card_offers WHERE id = ?""",
                (offer["id"],),
            ).fetchone()

    selected_offer_card = CARDS.get(offer["selected_card_id"] or "") if offer else None
    pending_offer = bool(offer and not offer["resolved"] and card_offer_available)
    card_offer_revision = db.execute(
        "SELECT card_offer_revision FROM characters WHERE id = ?", (character["id"],)
    ).fetchone()[0]
    card_choices = (
        [CARDS[card_id] for card_id in json.loads(offer["card_ids"]) if card_id in CARDS]
        if pending_offer and selected_offer_card is None
        else []
    )
    card_limit = 8 if g.user["is_premium"] else 6
    active_cards = [
        CARDS[row["upgrade_key"]]
        for row in active_rows
        if row["upgrade_key"] in CARDS
    ]
    replacement_cards = active_cards if pending_offer and selected_offer_card else []
    wave_reward = wave_experience_reward(
        character["current_phase"], character["current_wave"],
        character["phase_xp_budget"], difficulty,
    )
    xp_orbs = db.execute(
        """SELECT id, world_x, world_y FROM card_xp_orbs
           WHERE character_id = ? AND collected = 0 ORDER BY id""",
        (character["id"],),
    ).fetchall()
    return render_template(
        "game.html",
        username=g.user["username"],
        character=character,
        max_health=combat_stats["max_health"],
        max_mana=combat_stats["max_mana"],
        class_info=CLASSES[character["class_id"]],
        skill_options=skill_options,
        skills_by_id=skills_by_id,
        equipped_skills=equipped_skills,
        base_attack_range=CLASSES[character["class_id"]]["base_attack_range"],
        base_skill_range=CLASSES[character["class_id"]]["base_skill_range"],
        active_cards=active_cards,
        card_choices=card_choices,
        card_offer_id=offer["id"] if pending_offer else 0,
        recommended_card_id=offer["recommended_card_id"] if card_choices else "",
        card_auto_pick_at=(offer["auto_pick_at"] or 0) if card_choices else 0,
        card_offer_resolved=not pending_offer,
        selected_offer_card=selected_offer_card if pending_offer else None,
        replacement_cards=replacement_cards,
        pending_card_choices=character["pending_card_choices"],
        card_experience=character["card_experience"],
        card_experience_needed=card_xp_needed(len(active_cards)),
        card_experience_orb_value=CARD_XP_PER_ORB,
        card_experience_orb_value_premium=CARD_XP_PER_ORB_PREMIUM,
        xp_orbs=[dict(orb) for orb in xp_orbs],
        enemies=enemies,
        card_limit=card_limit,
        is_premium=bool(g.user["is_premium"]),
        premium_test_toggle_enabled=current_app.config["ENABLE_PREMIUM_TEST_TOGGLE"],
        waves_per_phase=WAVES_PER_PHASE,
        wave_reward=wave_reward,
        next_level_xp=(
            experience_needed(character["level"])
            if character["level"] < MAX_LEVEL
            else 0
        ),
        max_level=MAX_LEVEL,
        is_boss_wave=is_boss_wave,
        is_miniboss_wave=is_miniboss_wave,
        mission_difficulty=difficulty,
        mission_difficulty_label=DIFFICULTIES[difficulty]["label"],
        mission_countdown_seconds=MISSION_COUNTDOWN_SECONDS,
        dialogue_hooks={
            "status": "pending",
            "mission_start": None,
            "boss_encounter": None,
        },
        terminal_vilar_colliders=(
            terminal_vilar_collision_data()
            if character["current_phase"] == 1
            else []
        ),
        terminal_vilar_map_config=(
            terminal_vilar_map_config()
            if character["current_phase"] == 1
            else None
        ),
        season_act=season_act_for_phase(character["current_phase"]),
        campaign_map=campaign_map_for_phase(character["current_phase"]),
        season_phase_limit=SEASON_1_PHASES,
        agility=character["agility"],
        move_speed_multiplier=combat_stats["move_speed_multiplier"],
        attack_range_multiplier=combat_stats["attack_range_multiplier"],
        cooldown_multiplier=combat_stats["cooldown_multiplier"],
        control_options={
            "scheme": g.user["control_scheme"],
            "mouse_left_slot": g.user["mouse_left_slot"],
            "mouse_right_slot": g.user["mouse_right_slot"],
            "skill_slots": class_skill_slots,
        },
    )


@game_blueprint.get("/mapas/terminal-vilar-fase1")
def terminal_vilar_fase1_preview():
    return render_template(
        "mapas/terminal_vilar_fase1.html",
        terminal_vilar_colliders=terminal_vilar_collision_data(),
        terminal_vilar_map_config=terminal_vilar_map_config(),
        map_editor_enabled=request.remote_addr in {"127.0.0.1", "::1"},
    )


@game_blueprint.post("/mapas/terminal-vilar-fase1/salvar")
def save_terminal_vilar_fase1_config():
    if request.remote_addr not in {"127.0.0.1", "::1"}:
        abort(403, description="O editor do mapa só aceita salvamento local.")
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        abort(400, description="Envie a configuração do mapa em JSON.")
    csrf_token_value = payload.get("csrf_token")
    if not isinstance(csrf_token_value, str):
        abort(400, description="Token de segurança inválido.")
    validate_csrf(csrf_token_value)
    config = {key: value for key, value in payload.items() if key != "csrf_token"}
    try:
        saved_config = save_terminal_vilar_map_config(config)
    except ValueError as error:
        return jsonify({"ok": False, "error": str(error)}), 400
    return jsonify({"ok": True, "map_config": saved_config})


def _selected_character_for_lobby():
    if not g.user:
        return None
    character_id = session.get("selected_character_id")
    if character_id is None:
        return None
    return get_db().execute(
        """SELECT id, name, class_id, level, strength, agility, vitality, energy,
                  current_phase, current_wave, current_difficulty,
                  phase_intermission, death_intermission, attribute_points,
                  legacy_points, campaign_complete
           FROM characters WHERE id = ? AND user_id = ?""",
        (character_id, g.user["id"]),
    ).fetchone()


@game_blueprint.get("/sala-de-espera")
def lobby():
    if not g.user:
        flash("Entre na sua conta para acessar a Sala de Espera.", "info")
        return redirect(url_for("auth.home"))
    character = _selected_character_for_lobby()
    if character is None:
        flash("Selecione um personagem antes de entrar na Sala de Espera.", "info")
        return redirect(url_for("characters.index"))
    db = get_db()
    pending = pending_mission_run(db, g.user["id"])
    if pending is not None:
        return redirect(url_for("game.post_mission", run_id=pending["id"]))
    session["in_lobby"] = True
    purchased_talents = db.execute(
        "SELECT talent_id FROM character_talents WHERE character_id = ?",
        (character["id"],),
    ).fetchall()
    spent_legacy_points = sum(
        NODE_INDEX[row["talent_id"]]["cost"]
        for row in purchased_talents
        if row["talent_id"] in NODE_INDEX
        and NODE_INDEX[row["talent_id"]]["class_id"] == character["class_id"]
    )
    available_talent_points = max(0, character["legacy_points"] - spent_legacy_points)
    mission_difficulties = [
        {
            **state,
            "profile": DIFFICULTIES[state["key"]],
            "completed_phases": sorted(state["completed_phases"]),
            "available_phases": sorted(state["available_phases"]),
        }
        for state in difficulty_state(db, g.user["id"])
    ]
    selected_state = next(
        (
            state for state in mission_difficulties
            if state["key"] == character["current_difficulty"]
            and state["unlocked"]
            and state["available_phases"]
        ),
        next((state for state in mission_difficulties if state["available_phases"]), None),
    )
    selected_phase = character["current_phase"]
    if selected_state and selected_phase not in selected_state["available_phases"]:
        selected_phase = selected_state["available_phases"][0]
    return render_template(
        "lobby.html",
        character=character,
        class_info=CLASSES[character["class_id"]],
        campaign_map=campaign_map_for_phase(selected_phase),
        season_acts=SEASON_1_ACTS,
        season_phase_limit=SEASON_1_PHASES,
        available_talent_points=available_talent_points,
        mission_difficulties=mission_difficulties,
        selected_difficulty=selected_state["key"] if selected_state else "",
        selected_phase=selected_phase,
        friends=[],
    )


def _launch_mission(db, character, user_id: int, difficulty: str, phase: int):
    if difficulty not in DIFFICULTIES or not can_access_mission(db, user_id, difficulty, phase):
        return False
    if (pending_mission_run(db, user_id) is not None
            or active_account_mission_run(db, user_id) is not None):
        return False
    character_id = character["id"]
    character_row = db.execute(
        "SELECT * FROM characters WHERE id = ? AND user_id = ?",
        (character_id, user_id),
    ).fetchone()
    if character_row is None:
        return False
    db.execute("DELETE FROM temporary_upgrades WHERE character_id = ?", (character_id,))
    db.execute("DELETE FROM card_offers WHERE character_id = ?", (character_id,))
    db.execute("DELETE FROM card_offer_history WHERE character_id = ?", (character_id,))
    db.execute("DELETE FROM card_xp_orbs WHERE character_id = ?", (character_id,))
    purchased_talents = {
        row["talent_id"] for row in db.execute(
            "SELECT talent_id FROM character_talents WHERE character_id = ?",
            (character_id,),
        ).fetchall()
    }
    stats = derived_combat_stats(character_row, purchased_talents=purchased_talents)
    start_time = time.time() + MISSION_COUNTDOWN_SECONDS
    now = datetime.now(timezone.utc).isoformat()
    db.execute(
        """UPDATE characters
           SET current_phase = ?, current_wave = 1, current_difficulty = ?,
               current_health = ?, current_mana = ?, phase_preparation_until = ?,
               phase_xp_budget = ?, phase_intermission = 0, death_intermission = 0,
               campaign_complete = 0, card_experience = 0, pending_card_choices = 0
           WHERE id = ? AND user_id = ?""",
        (
            phase, difficulty, stats["max_health"], stats["max_mana"],
            start_time, phase_xp_budget_for_level(character_row["level"]),
            character_id, user_id,
        ),
    )
    db.execute(
        """INSERT INTO mission_runs
           (user_id, character_id, difficulty, phase, start_time, created_at)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (user_id, character_id, difficulty, phase, start_time, now),
    )
    return True


@game_blueprint.post("/sala-de-espera/iniciar")
def lobby_start():
    if not g.user:
        return redirect(url_for("auth.home"))
    validate_csrf(request.form.get("csrf_token", ""))
    character = _selected_character_for_lobby()
    if character is None:
        return redirect(url_for("characters.index"))
    db = get_db()
    pending = pending_mission_run(db, g.user["id"])
    if pending is not None:
        return redirect(url_for("game.post_mission", run_id=pending["id"]))
    if current_app.config.get("TESTING") and not request.form.get("difficulty"):
        session["in_lobby"] = False
        if character["phase_intermission"]:
            db.execute(
                """UPDATE characters SET phase_intermission = 0, death_intermission = 0,
                   phase_preparation_until = ? WHERE id = ?""",
                (time.time() + PHASE_PREPARATION_SECONDS, character["id"]),
            )
        elif character["death_intermission"]:
            db.execute(
                """UPDATE characters SET death_intermission = 0,
                   phase_preparation_until = 0 WHERE id = ?""",
                (character["id"],),
            )
        db.commit()
        return redirect(url_for("game.room"))
    try:
        phase = int(request.form.get("phase", ""))
    except (TypeError, ValueError):
        flash("Selecione uma fase válida.", "error")
        return redirect(url_for("game.lobby"))
    difficulty = request.form.get("difficulty", "")
    if not can_access_mission(db, g.user["id"], difficulty, phase):
        flash("Essa dificuldade ou fase ainda não foi liberada.", "error")
        return redirect(url_for("game.lobby"))
    db.execute("BEGIN IMMEDIATE")
    pending = pending_mission_run(db, g.user["id"])
    if pending is not None:
        db.rollback()
        return redirect(url_for("game.post_mission", run_id=pending["id"]))
    active = active_account_mission_run(db, g.user["id"])
    if active is not None:
        db.rollback()
        if active["character_id"] == character["id"]:
            return redirect(url_for("game.room"))
        flash("Já existe uma missão ativa nesta conta. Retome-a antes de iniciar outra.", "info")
        return redirect(url_for("game.lobby"))
    if not _launch_mission(db, character, g.user["id"], difficulty, phase):
        db.rollback()
        flash("Não foi possível iniciar essa missão.", "error")
        return redirect(url_for("game.lobby"))
    db.commit()
    from .socket_events import reset_character_combat_state

    reset_character_combat_state(character["id"])
    session["in_lobby"] = False
    return redirect(url_for("game.room"))


@game_blueprint.post("/jogo/proxima-fase")
def continue_phase():
    if not g.user:
        return redirect(url_for("auth.home"))
    validate_csrf(request.form.get("csrf_token", ""))
    character = _selected_character_for_lobby()
    if character is None:
        return redirect(url_for("characters.index"))
    return redirect(url_for("game.lobby"))


@game_blueprint.post("/jogo/reiniciar-fase")
def restart_phase():
    if not g.user:
        return redirect(url_for("auth.home"))
    validate_csrf(request.form.get("csrf_token", ""))
    character = _selected_character_for_lobby()
    if character is None:
        return redirect(url_for("characters.index"))
    db = get_db()
    phase = character["current_phase"]
    difficulty = character["current_difficulty"]
    pending = pending_mission_run(db, g.user["id"])
    if pending is not None:
        return redirect(url_for("game.post_mission", run_id=pending["id"]))
    db.execute("BEGIN IMMEDIATE")
    db.execute(
        """UPDATE mission_runs SET status = 'failed'
           WHERE character_id = ? AND status = 'active'""",
        (character["id"],),
    )
    if not _launch_mission(db, character, g.user["id"], difficulty, phase):
        db.rollback()
        flash("Não foi possível reiniciar esta fase.", "error")
        return redirect(url_for("game.lobby"))
    db.commit()
    from .socket_events import reset_character_combat_state

    reset_character_combat_state(character["id"])
    return redirect(url_for("game.room"))


@game_blueprint.get("/jogo/pos-fase")
def post_mission():
    if not g.user:
        return redirect(url_for("auth.home"))
    db = get_db()
    pending = pending_mission_run(db, g.user["id"])
    run = pending
    requested_run_id = request.args.get("run_id", type=int)
    if run is None:
        if requested_run_id is not None:
            run = db.execute(
                """SELECT * FROM mission_runs
                   WHERE id = ? AND user_id = ? AND status = 'completed'""",
                (requested_run_id, g.user["id"]),
            ).fetchone()
        if run is None:
            run = db.execute(
                """SELECT * FROM mission_runs
                   WHERE user_id = ? AND status = 'completed'
                   ORDER BY id DESC LIMIT 1""",
                (g.user["id"],),
            ).fetchone()
    if run is None:
        flash("Não há espólios de missão para resolver.", "info")
        return redirect(url_for("game.lobby"))
    loot = db.execute(
        """SELECT * FROM staging_inventory
           WHERE mission_run_id = ? AND user_id = ? ORDER BY chest_index""",
        (run["id"], g.user["id"]),
    ).fetchall()
    inventory = db.execute(
        """SELECT * FROM inventory_items WHERE user_id = ?
           ORDER BY created_at DESC, id DESC""",
        (g.user["id"],),
    ).fetchall()
    gold_balance = db.execute(
        "SELECT wallet_gold FROM users WHERE id = ?", (g.user["id"],)
    ).fetchone()["wallet_gold"]
    total_gold = db.execute(
        """SELECT COALESCE(SUM(amount_gold), 0) FROM gold_ledger
           WHERE mission_run_id = ?""",
        (run["id"],),
    ).fetchone()[0]
    return render_template(
        "post_mission.html",
        run=run,
        difficulty_label=DIFFICULTIES[run["difficulty"]]["label"],
        loot=loot,
        inventory=inventory,
        inventory_count=len(inventory),
        inventory_capacity=INVENTORY_CAPACITY,
        has_pending_loot=any(item["status"] == "pending" for item in loot),
        gold_balance=gold_balance,
        gold_display=format_gold(gold_balance),
        mission_reward_gold_display=format_gold(total_gold),
        rarity_labels={
            "common": "Comum", "rare": "Raro",
            "epic": "Épico", "legendary": "Lendário",
        },
        format_gold=format_gold,
    )


@game_blueprint.post("/jogo/pos-fase/resolver")
def resolve_mission_loot():
    if not g.user:
        return redirect(url_for("auth.home"))
    validate_csrf(request.form.get("csrf_token", ""))
    try:
        run_id = int(request.form.get("run_id", ""))
        kept_item_ids = {int(value) for value in request.form.getlist("keep_item_ids")}
    except (TypeError, ValueError):
        flash("Seleção de espólios inválida.", "error")
        return redirect(url_for("game.post_mission"))
    db = get_db()
    db.execute("BEGIN IMMEDIATE")
    try:
        result = resolve_staging_inventory(
            db, g.user["id"], run_id, kept_item_ids
        )
    except InventoryCapacityError as error:
        db.rollback()
        flash(str(error), "error")
        return redirect(url_for("game.post_mission", run_id=run_id))
    except ValueError as error:
        db.rollback()
        flash(str(error), "error")
        return redirect(url_for("game.post_mission"))
    db.commit()
    next_pending = pending_mission_run(db, g.user["id"])
    if next_pending is not None:
        flash(
            f"{result['kept_count']} item(ns) mantido(s); resolva também os espólios pendentes.",
            "success",
        )
        return redirect(url_for("game.post_mission", run_id=next_pending["id"]))
    flash(
        f"{result['kept_count']} item(ns) resgatado(s); "
        f"{result['discarded_count']} descartado(s).",
        "success",
    )
    return redirect(url_for("game.lobby"))


@game_blueprint.get("/inventario")
def inventory():
    if not g.user:
        return redirect(url_for("auth.home"))
    db = get_db()
    pending = pending_mission_run(db, g.user["id"])
    if pending is not None:
        return redirect(url_for("game.post_mission", run_id=pending["id"]))
    items = db.execute(
        "SELECT * FROM inventory_items WHERE user_id = ? ORDER BY created_at DESC, id DESC",
        (g.user["id"],),
    ).fetchall()
    gold_balance = db.execute(
        "SELECT wallet_gold FROM users WHERE id = ?", (g.user["id"],)
    ).fetchone()["wallet_gold"]
    return render_template(
        "inventory.html",
        items=items,
        inventory_count=len(items),
        inventory_capacity=INVENTORY_CAPACITY,
        gold_balance=gold_balance,
        gold_display=format_gold(gold_balance),
        rarity_labels={
            "common": "Comum", "rare": "Raro",
            "epic": "Épico", "legendary": "Lendário",
        },
        format_gold=format_gold,
    )


@game_blueprint.post("/inventario/item")
def inventory_item_action():
    if not g.user:
        return redirect(url_for("auth.home"))
    validate_csrf(request.form.get("csrf_token", ""))
    try:
        item_id = int(request.form.get("item_id", ""))
    except (TypeError, ValueError):
        flash("Item inválido.", "error")
        return redirect(url_for("game.inventory"))
    action = request.form.get("action")
    return_to = request.form.get("return_to")
    destination = (
        url_for("game.post_mission")
        if return_to == "post_mission"
        else url_for("game.inventory")
    )
    db = get_db()
    db.execute("BEGIN IMMEDIATE")
    try:
        if action == "sell":
            sold_gold = sell_inventory_item(db, g.user["id"], item_id)
        elif action == "discard":
            discard_inventory_item(db, g.user["id"], item_id)
            sold_gold = 0
        else:
            db.rollback()
            flash("Ação de inventário inválida.", "error")
            return redirect(destination)
    except ValueError as error:
        db.rollback()
        flash(str(error), "error")
        return redirect(destination)
    db.commit()
    if sold_gold:
        flash(f"Item vendido por {format_gold(sold_gold)} Ouro.", "success")
    else:
        flash("Item descartado.", "info")
    if return_to == "post_mission":
        pending = pending_mission_run(db, g.user["id"])
        if pending is not None:
            return redirect(url_for("game.post_mission", run_id=pending["id"]))
    return redirect(destination)


@game_blueprint.post("/jogo/cartas/escolher")
def choose_card():
    if not g.user:
        return redirect(url_for("auth.home"))
    validate_csrf(request.form.get("csrf_token", ""))
    character_id = session.get("selected_character_id")
    db = get_db()
    db.execute("BEGIN IMMEDIATE")
    character = db.execute(
        """SELECT * FROM characters
           WHERE id = ? AND user_id = ?""",
        (character_id, g.user["id"]),
    ).fetchone() if character_id is not None else None
    if character is None:
        db.rollback()
        flash("Selecione um personagem antes de escolher cartas.", "error")
        return redirect(url_for("characters.index"))

    offer = db.execute(
        """SELECT id, card_ids, selected_card_id, resolved FROM card_offers
           WHERE character_id = ? AND phase = ? AND wave = ?""",
        (character_id, character["current_phase"], character["current_wave"]),
    ).fetchone()
    if offer is None or offer["resolved"]:
        db.rollback()
        flash("Não há uma oferta de cartas pendente nesta onda.", "info")
        return redirect(url_for("game.room"))

    db.executemany(
        """INSERT OR IGNORE INTO card_offer_history
           (character_id, phase, wave, card_id) VALUES (?, ?, ?, ?)""",
        [
            (character_id, character["current_phase"], character["current_wave"], card_id)
            for card_id in json.loads(offer["card_ids"])
        ],
    )

    active_rows = db.execute(
        "SELECT id, upgrade_key FROM temporary_upgrades WHERE character_id = ? ORDER BY id",
        (character_id,),
    ).fetchall()
    active = {row["upgrade_key"] for row in active_rows}
    capacity = 8 if g.user["is_premium"] else 6

    if request.form.get("skip_replacement") == "1":
        if len(active) < capacity:
            db.rollback()
            flash("Ainda há espaço livre. Escolha uma das cartas oferecidas.", "error")
            return redirect(url_for("game.room"))
        db.execute("UPDATE card_offers SET resolved = 1 WHERE id = ?", (offer["id"],))
        db.execute(
            "UPDATE characters SET pending_card_choices = MAX(0, pending_card_choices - 1) WHERE id = ?",
            (character_id,),
        )
        db.commit()
        flash("Cartas ativas mantidas. As três opções desta oferta foram descartadas.", "info")
        return redirect(url_for("game.room"))

    if offer["selected_card_id"]:
        chosen_id = offer["selected_card_id"]
        offered_ids = set(json.loads(offer["card_ids"]))
        replacement_id = request.form.get("replacement_card_id", "")
        if (chosen_id not in CARDS or chosen_id not in offered_ids
                or replacement_id not in active or len(active) < capacity):
            db.rollback()
            flash("Escolha uma carta ativa válida para substituir.", "error")
            return redirect(url_for("game.room"))
        db.execute(
            "DELETE FROM temporary_upgrades WHERE character_id = ? AND upgrade_key = ?",
            (character_id, replacement_id),
        )
        db.execute(
            "INSERT INTO temporary_upgrades (character_id, upgrade_key) VALUES (?, ?)",
            (character_id, chosen_id),
        )
        db.execute(
            """UPDATE card_offers SET resolved = 1 WHERE id = ?""", (offer["id"],)
        )
        if character["pending_card_choices"] > 0:
            db.execute(
                "UPDATE characters SET pending_card_choices = pending_card_choices - 1 WHERE id = ?",
                (character_id,),
            )
        db.commit()
        flash(f"{CARDS[chosen_id]['name']} ativada na coleção.", "success")
        return redirect(url_for("game.room"))

    chosen_id = request.form.get("card_id", "")
    offered_ids = set(json.loads(offer["card_ids"]))
    if chosen_id not in offered_ids or chosen_id in active or chosen_id not in CARDS:
        db.rollback()
        flash("Essa carta não está disponível nesta oferta.", "error")
        return redirect(url_for("game.room"))
    if len(active) >= capacity:
        db.execute(
            "UPDATE card_offers SET selected_card_id = ? WHERE id = ?",
            (chosen_id, offer["id"]),
        )
        db.commit()
        flash("Clique em uma carta ativa para substituí-la ou mantenha as cartas atuais.", "info")
        return redirect(url_for("game.room"))

    db.execute(
        "INSERT INTO temporary_upgrades (character_id, upgrade_key) VALUES (?, ?)",
        (character_id, chosen_id),
    )
    db.execute("UPDATE card_offers SET resolved = 1 WHERE id = ?", (offer["id"],))
    if character["pending_card_choices"] > 0:
        db.execute(
            "UPDATE characters SET pending_card_choices = pending_card_choices - 1 WHERE id = ?",
            (character_id,),
        )
    db.commit()
    flash(f"{CARDS[chosen_id]['name']} ativada na coleção.", "success")
    return redirect(url_for("game.room"))


@game_blueprint.post("/jogo/onda/concluir")
def complete_wave():
    if not g.user:
        return redirect(url_for("auth.home"))
    validate_csrf(request.form.get("csrf_token", ""))
    character_id = session.get("selected_character_id")
    db = get_db()
    db.execute("BEGIN IMMEDIATE")
    character = db.execute(
        """SELECT id, level, experience, current_phase, current_wave,
                  card_experience, pending_card_choices, phase_intermission,
                  campaign_complete
           FROM characters WHERE id = ? AND user_id = ?""",
        (character_id, g.user["id"]),
    ).fetchone() if character_id is not None else None
    if character is None:
        db.rollback()
        flash("Selecione um personagem antes de avançar.", "error")
        return redirect(url_for("characters.index"))

    offer = db.execute(
        """SELECT resolved FROM card_offers
           WHERE character_id = ? AND phase = ? AND wave = ?""",
        (character_id, character["current_phase"], character["current_wave"]),
    ).fetchone()
    if offer is not None and not offer["resolved"]:
        db.rollback()
        flash("Escolha uma carta ou mantenha a coleção antes de concluir a onda.", "info")
        return redirect(url_for("game.room"))
    if character["pending_card_choices"] > 0:
        db.rollback()
        flash("Escolha uma carta antes de concluir a onda.", "info")
        return redirect(url_for("game.room"))
    if character["phase_intermission"]:
        db.rollback()
        flash("Escolha entre a Sala de Espera e a próxima fase antes de avançar.", "info")
        return redirect(url_for("game.room"))
    if character["campaign_complete"]:
        db.rollback()
        return redirect(url_for("game.room"))

    phase = character["current_phase"]
    wave = character["current_wave"]
    # EXP is already awarded for each monster defeated; this endpoint only advances.
    level, experience, levels_gained = character["level"], character["experience"], 0
    phase_ended = wave == WAVES_PER_PHASE
    campaign_complete = (
        phase_ended and phase >= SEASON_1_PHASES
    )
    was_boss_wave = encounter_type(phase, wave) == "boss"
    if phase_ended and not campaign_complete:
        phase += 1
        wave = 1
    elif not phase_ended:
        wave += 1
    _, auto_allocated = award_attribute_points(
        db, character_id, levels_gained, bool(g.user["is_premium"])
    )
    db.execute(
        """UPDATE characters
           SET level = ?, experience = ?, current_phase = ?, current_wave = ?,
               phase_xp_budget = CASE WHEN ? THEN ? ELSE phase_xp_budget END,
               phase_intermission = ?, campaign_complete = ?, phase_preparation_until = 0,
               card_experience = CASE WHEN ? THEN 0 ELSE card_experience END,
               pending_card_choices = CASE WHEN ? THEN 0 ELSE pending_card_choices END
           WHERE id = ? AND user_id = ?""",
        (
            level,
            experience,
            phase,
            wave,
            int(phase_ended and not campaign_complete),
            phase_xp_budget_for_level(level),
            int(phase_ended and not campaign_complete),
            int(campaign_complete),
            int(phase_ended),
            int(phase_ended),
            character_id,
            g.user["id"],
        ),
    )
    if phase_ended:
        db.execute("DELETE FROM temporary_upgrades WHERE character_id = ?", (character_id,))
        db.execute("DELETE FROM card_offers WHERE character_id = ?", (character_id,))
        db.execute("DELETE FROM card_offer_history WHERE character_id = ?", (character_id,))
        db.execute("DELETE FROM card_xp_orbs WHERE character_id = ?", (character_id,))
    db.commit()
    if campaign_complete:
        message = "Temporada 1 concluída. Sua jornada continua nas próximas temporadas."
    elif was_boss_wave:
        message = f"Chefe da fase derrotado no protótipo. Fase {phase} iniciada."
    else:
        message = f"Onda concluída no protótipo. Próxima: fase {phase}, onda {wave}."
    if levels_gained:
        message += f" Você subiu {levels_gained} nível(is)!"
    if auto_allocated:
        message += f" {auto_allocated} ponto(s) distribuído(s) automaticamente."
    flash(message, "success")
    return redirect(url_for("game.room"))


