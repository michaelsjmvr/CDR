"""Authenticated radial talent graph and class specialization routes."""

from datetime import datetime, timezone

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from .classes import CLASSES
from .combat import derived_combat_stats
from .database import get_db
from .progression import MAX_ATTRIBUTE_VALUE, MAX_LEVEL, legacy_points_for_level
from .security import validate_csrf
from .talents import (
    CLASS_SPECIALIZATIONS,
    NODE_INDEX,
    LEGACY_NODE_INDEX,
    LEGACY_V104_NODE_INDEX,
    RADIAL_GRAPHS,
    SPECIALIZATION_UNLOCK_LEVEL,
    activated_from_root,
    talent_node,
)


talents_blueprint = Blueprint("talents", __name__)


def _current_character():
    character_id = session.get("selected_character_id")
    if character_id is None:
        return None
    return get_db().execute(
        """SELECT id, name, class_id, level, legacy_points,
                  specialization_id
           FROM characters WHERE id = ? AND user_id = ?""",
        (character_id, g.user["id"]),
    ).fetchone()


def _refund_v104_talents(character_id: int, user_id: int) -> bool:
    """Refund the replaced tree once, preserving its purchased attributes."""
    db = get_db()
    owned_rows = db.execute(
        "SELECT talent_id FROM character_talents WHERE character_id = ?",
        (character_id,),
    ).fetchall()
    owned = {row["talent_id"] for row in owned_rows}
    old_ids = owned & set(LEGACY_V104_NODE_INDEX)
    if not old_ids:
        return False

    db.execute("BEGIN IMMEDIATE")
    current = db.execute(
        "SELECT * FROM characters WHERE id = ? AND user_id = ?",
        (character_id, user_id),
    ).fetchone()
    if current is None:
        db.rollback()
        return False
    old_ids = {
        talent_id for talent_id in old_ids
        if LEGACY_V104_NODE_INDEX[talent_id].get("class_id") == current["class_id"]
    }
    if not old_ids:
        db.rollback()
        return False

    refund_stats = {}
    for talent_id in old_ids:
        node = LEGACY_V104_NODE_INDEX[talent_id]
        for stat, value in node.get("stat_bonuses", {}).items():
            refund_stats[stat] = refund_stats.get(stat, 0) + int(value)
        if node.get("agility_bonus"):
            refund_stats["agility"] = refund_stats.get("agility", 0) + int(
                node["agility_bonus"]
            )

    placeholders = ",".join("?" for _ in old_ids)
    db.execute(
        f"DELETE FROM character_talents WHERE character_id = ? AND talent_id IN ({placeholders})",
        (character_id, *old_ids),
    )
    if refund_stats:
        assignments = ", ".join(f"{stat} = max(0, {stat} - ?)" for stat in refund_stats)
        db.execute(
            f"UPDATE characters SET {assignments} WHERE id = ?",
            (*refund_stats.values(), character_id),
        )
    db.execute(
        "UPDATE characters SET talent_root_id = ? WHERE id = ?",
        (RADIAL_GRAPHS[current["class_id"]]["root_id"], character_id),
    )
    updated = db.execute(
        "SELECT * FROM characters WHERE id = ?", (character_id,)
    ).fetchone()
    active_cards = {
        row["upgrade_key"] for row in db.execute(
            "SELECT upgrade_key FROM temporary_upgrades WHERE character_id = ?",
            (character_id,),
        ).fetchall()
    }
    remaining_talents = {
        row["talent_id"] for row in db.execute(
            "SELECT talent_id FROM character_talents WHERE character_id = ?",
            (character_id,),
        ).fetchall()
    }
    stats = derived_combat_stats(updated, active_cards, remaining_talents)
    db.execute(
        "UPDATE characters SET current_health = ?, current_mana = ? WHERE id = ?",
        (
            min(updated["current_health"], stats["max_health"]),
            min(updated["current_mana"], stats["max_mana"]),
            character_id,
        ),
    )
    db.commit()
    return True


@talents_blueprint.get("/talentos")
def tree():
    if not g.user:
        flash("Entre na sua conta para acessar a Árvore de Talentos.", "info")
        return redirect(url_for("auth.home"))
    if not session.get("in_lobby"):
        flash("Os talentos só podem ser ajustados na Sala de Espera.", "info")
        return redirect(url_for("game.lobby"))
    character = _current_character()
    if character is None:
        flash("Selecione um personagem antes de abrir a Árvore de Talentos.", "info")
        return redirect(url_for("characters.index"))
    if _refund_v104_talents(character["id"], g.user["id"]):
        flash(
            "A árvore foi atualizada. Seus antigos talentos e atributos foram devolvidos para você investir no novo caminho.",
            "success",
        )
        character = _current_character()

    db = get_db()
    purchased = {
        row["talent_id"]
        for row in db.execute(
            "SELECT talent_id FROM character_talents WHERE character_id = ?",
            (character["id"],),
        ).fetchall()
    }
    class_id = character["class_id"]
    graph = RADIAL_GRAPHS[class_id]
    selected_root = graph["root_id"]
    spent_points = sum(
        NODE_INDEX[talent_id]["cost"]
        for talent_id in purchased
        if talent_id in NODE_INDEX and NODE_INDEX[talent_id].get("class_id") == class_id
    )
    available_points = max(0, character["legacy_points"] - spent_points)
    active = activated_from_root(class_id, selected_root, purchased)
    nodes = []
    for source in graph["nodes"]:
        node = dict(source)
        is_root = node["id"] == selected_root
        is_purchased = node["id"] in purchased
        branch_matches = (
            node.get("specialization_id") is None
            or node.get("specialization_id") == character["specialization_id"]
        )
        can_unlock = (
            branch_matches
            and node["id"] not in active
            and bool(set(node["neighbors"]) & active)
        )
        node.update(
            purchased=is_purchased,
            is_current_root=is_root,
            is_active=is_root or is_purchased,
            can_unlock=can_unlock,
            affordable=available_points >= node["cost"],
            allocatable=node.get("allocatable", True),
            selectable=True,
        )
        node["can_purchase"] = (
            bool(character["specialization_id"])
            and branch_matches
            and can_unlock
            and not is_purchased
            and not is_root
            and not node.get("is_root_option")
            and node.get("allocatable", True)
            and available_points >= node["cost"]
        )
        nodes.append(node)
    node_by_id = {node["id"]: node for node in nodes}
    edges = [
        {
            **edge,
            "connected": edge["from"] in active and edge["to"] in active,
            "available": (
                edge["from"] in active and node_by_id[edge["to"]]["can_unlock"]
            ) or (
                edge["to"] in active and node_by_id[edge["from"]]["can_unlock"]
            ),
        }
        for edge in graph["edges"]
    ]
    legacy_owned = [
        LEGACY_NODE_INDEX[talent_id]
        for talent_id in sorted(purchased)
        if talent_id in LEGACY_NODE_INDEX
        and LEGACY_NODE_INDEX[talent_id]["class_id"] == class_id
    ]
    tree_data = {
        "title": f"Árvore de {CLASSES[class_id]['name']}",
        "subtitle": "Três evoluções possíveis; escolha uma no nível 100 e desenvolva somente o caminho escolhido.",
    }
    specialization = next(
        (item for item in CLASS_SPECIALIZATIONS[character["class_id"]]
         if item["id"] == character["specialization_id"]),
        None,
    )
    specialization_skill_unlocked = bool(
        specialization and specialization["keystone_id"] in purchased
    )
    specialization_costs = sorted({
        item["branch_cost"]
        for item in CLASS_SPECIALIZATIONS[character["class_id"]]
    })
    specialization_cost_summary = " ou ".join(
        str(cost) for cost in specialization_costs
    )
    return render_template(
        "talents.html",
        character=character,
        class_info=CLASSES[character["class_id"]],
        tree_data=tree_data,
        nodes=nodes,
        graph_nodes=nodes,
        graph_edges=edges,
        graph_sectors=graph["sectors"],
        core_name=graph["roots"][0]["name"],
        selected_root=selected_root,
        legacy_owned=legacy_owned,
        legacy_count=len(legacy_owned),
        specializations=CLASS_SPECIALIZATIONS[character["class_id"]],
        specialization_cost_summary=specialization_cost_summary,
        specialization_paths_total_cost=sum(
            item["branch_cost"]
            for item in CLASS_SPECIALIZATIONS[character["class_id"]]
        ),
        specialization=specialization,
        specialization_skill_unlocked=specialization_skill_unlocked,
        specialization_unlock_level=SPECIALIZATION_UNLOCK_LEVEL,
        is_premium=bool(g.user["is_premium"]),
        available_points=available_points,
        spent_points=spent_points,
        legacy_points_cap=legacy_points_for_level(MAX_LEVEL),
        purchased_count=len(purchased),
    )


@talents_blueprint.post("/talentos/comprar")
def purchase():
    if not g.user:
        return redirect(url_for("auth.home"))
    if not session.get("in_lobby"):
        flash("Os talentos só podem ser ajustados na Sala de Espera.", "info")
        return redirect(url_for("game.lobby"))
    validate_csrf(request.form.get("csrf_token", ""))
    character = _current_character()
    if character is None:
        flash("Selecione um personagem antes de investir Pontos de Legado.", "error")
        return redirect(url_for("characters.index"))

    talent_id = request.form.get("talent_id", "")
    node = talent_node(character["class_id"], talent_id)
    if node is None or talent_id not in {item["id"] for item in RADIAL_GRAPHS[character["class_id"]]["nodes"]}:
        flash("Esse talento não pertence à classe selecionada.", "error")
        return redirect(url_for("talents.tree"))

    db = get_db()
    db.execute("BEGIN IMMEDIATE")
    character = db.execute(
        """SELECT * FROM characters
           WHERE id = ? AND user_id = ?""",
        (character["id"], g.user["id"]),
    ).fetchone()
    if character is None:
        db.rollback()
        session.pop("selected_character_id", None)
        flash("Selecione um personagem válido para investir talentos.", "error")
        return redirect(url_for("characters.index"))
    graph = RADIAL_GRAPHS[character["class_id"]]
    root_id = graph["root_id"]
    if not character["specialization_id"]:
        db.rollback()
        flash(f"Escolha uma das três evoluções ao alcançar o nível {SPECIALIZATION_UNLOCK_LEVEL} antes de investir.", "info")
        return redirect(url_for("talents.tree"))
    if node is not None and node.get("specialization_id") != character["specialization_id"]:
        db.rollback()
        flash("Esse ramo pertence a outra evolução e não pode ser desenvolvido junto com o caminho escolhido.", "error")
        return redirect(url_for("talents.tree"))
    node = talent_node(character["class_id"], talent_id)
    if node is not None and node.get("is_root_option"):
        db.rollback()
        flash("Pontos de partida são escolhidos como trilha inicial; não são comprados com Pontos de Legado.", "info")
        return redirect(url_for("talents.tree"))
    if node is None or not node.get("allocatable", True):
        db.rollback()
        flash("Este espaço ainda não está disponível.", "info")
        return redirect(url_for("talents.tree"))
    purchased = {
        row["talent_id"]
        for row in db.execute(
            "SELECT talent_id FROM character_talents WHERE character_id = ?",
            (character["id"],),
        ).fetchall()
    }
    spent = sum(
        NODE_INDEX[item]["cost"]
        for item in purchased
        if item in NODE_INDEX and NODE_INDEX[item].get("class_id") == character["class_id"]
    )

    if talent_id in purchased:
        db.rollback()
        flash("Esse talento já foi adquirido.", "info")
        return redirect(url_for("talents.tree"))
    active = activated_from_root(character["class_id"], root_id, purchased)
    if talent_id not in active and not (set(node["neighbors"]) & active):
        db.rollback()
        flash("Este nó ainda não está ligado por um caminho ativo da sua evolução.", "error")
        return redirect(url_for("talents.tree"))
    if character["legacy_points"] - spent < node["cost"]:
        db.rollback()
        flash("Você ainda não tem Pontos de Legado suficientes.", "info")
        return redirect(url_for("talents.tree"))

    stat_bonuses = {
        key: int(value) for key, value in node.get("stat_bonuses", {}).items()
        if key in {"strength", "agility", "vitality", "energy"} and int(value) > 0
    }
    if any(character[key] + bonus > MAX_ATTRIBUTE_VALUE for key, bonus in stat_bonuses.items()):
        db.rollback()
        flash("O talento ultrapassaria o limite atual de um atributo.", "error")
        return redirect(url_for("talents.tree"))

    db.execute(
        """INSERT INTO character_talents (character_id, talent_id, purchased_at)
           VALUES (?, ?, ?)""",
        (character["id"], talent_id, datetime.now(timezone.utc).isoformat()),
    )
    db.execute(
        "UPDATE characters SET talent_root_id = ? WHERE id = ?",
        (root_id, character["id"]),
    )
    active_ids = {
        row["upgrade_key"] for row in db.execute(
            "SELECT upgrade_key FROM temporary_upgrades WHERE character_id = ?",
            (character["id"],),
        ).fetchall()
    }
    old_stats = derived_combat_stats(character, active_ids, purchased)
    current_health = min(max(0, character["current_health"]), old_stats["max_health"])
    current_mana = min(max(0, character["current_mana"]), old_stats["max_mana"])
    if stat_bonuses:
        assignments = ", ".join(f"{key} = {key} + ?" for key in stat_bonuses)
        db.execute(
            f"UPDATE characters SET {assignments} WHERE id = ?",
            (*stat_bonuses.values(), character["id"]),
        )
    if node.get("agility_bonus"):
        db.execute("UPDATE characters SET agility = agility + ? WHERE id = ?",
                   (node["agility_bonus"], character["id"]))
    updated = db.execute("SELECT * FROM characters WHERE id = ?", (character["id"],)).fetchone()
    new_stats = derived_combat_stats(updated, active_ids, purchased | {talent_id})
    db.execute(
        "UPDATE characters SET current_health = ?, current_mana = ? WHERE id = ?",
        (min(new_stats["max_health"], current_health + max(0, new_stats["max_health"] - old_stats["max_health"])),
         min(new_stats["max_mana"], current_mana + max(0, new_stats["max_mana"] - old_stats["max_mana"])),
         character["id"]),
    )
    db.commit()
    flash(f"Talento adquirido: {node['name']}.", "success")
    return redirect(url_for("talents.tree"))


@talents_blueprint.post("/talentos/evolucao")
def choose_specialization():
    if not g.user:
        return redirect(url_for("auth.home"))
    if not session.get("in_lobby"):
        flash("A evolução de classe só pode ser escolhida na Sala de Espera.", "info")
        return redirect(url_for("game.lobby"))
    validate_csrf(request.form.get("csrf_token", ""))
    character = _current_character()
    if character is None:
        flash("Selecione um personagem antes de escolher uma evolução.", "error")
        return redirect(url_for("characters.index"))

    choice = request.form.get("specialization_id", "")
    allowed = {item["id"] for item in CLASS_SPECIALIZATIONS[character["class_id"]]}
    if choice not in allowed:
        flash("Essa evolução não pertence à classe selecionada.", "error")
        return redirect(url_for("talents.tree"))

    db = get_db()
    db.execute("BEGIN IMMEDIATE")
    current = db.execute(
        "SELECT * FROM characters WHERE id = ? AND user_id = ?",
        (character["id"], g.user["id"]),
    ).fetchone()
    if current is None:
        db.rollback()
        session.pop("selected_character_id", None)
        flash("Selecione um personagem válido.", "error")
        return redirect(url_for("characters.index"))
    premium_row = db.execute(
        "SELECT is_premium FROM users WHERE id = ?", (g.user["id"],)
    ).fetchone()
    is_premium = bool(premium_row and premium_row["is_premium"])
    if current["specialization_id"] == choice:
        db.rollback()
        flash("Esse já é o caminho ativo do personagem.", "info")
        return redirect(url_for("talents.tree"))
    if current["level"] < SPECIALIZATION_UNLOCK_LEVEL and not current["specialization_id"]:
        db.rollback()
        flash(f"A evolução de classe será liberada no nível {SPECIALIZATION_UNLOCK_LEVEL}.", "info")
        return redirect(url_for("talents.tree"))
    if current["specialization_id"] and not is_premium:
        db.rollback()
        flash("É preciso ter o benefício especial ativo para trocar o caminho de evolução.", "error")
        return redirect(url_for("talents.tree"))

    active_ids = {
        row["upgrade_key"] for row in db.execute(
            "SELECT upgrade_key FROM temporary_upgrades WHERE character_id = ?",
            (current["id"],),
        ).fetchall()
    }

    # Ao trocar com VIP, devolve os Pontos de Legado investidos no ramo atual
    # e remove exatamente os atributos permanentes concedidos por esses nós.
    if current["specialization_id"]:
        old_specialization = current["specialization_id"]
        graph_nodes = {
            item["id"]: item for item in RADIAL_GRAPHS[current["class_id"]]["nodes"]
        }
        owned = [row["talent_id"] for row in db.execute(
            "SELECT talent_id FROM character_talents WHERE character_id = ?",
            (current["id"],),
        ).fetchall()]
        reset_ids = [
            talent_id for talent_id in owned
            if talent_id in graph_nodes
            and graph_nodes[talent_id].get("specialization_id") == old_specialization
        ]
        refund_stats = {}
        for talent_id in reset_ids:
            for stat, value in graph_nodes[talent_id].get("stat_bonuses", {}).items():
                refund_stats[stat] = refund_stats.get(stat, 0) + int(value)

        if reset_ids:
            placeholders = ",".join("?" for _ in reset_ids)
            db.execute(
                f"DELETE FROM character_talents WHERE character_id = ? AND talent_id IN ({placeholders})",
                (current["id"], *reset_ids),
            )
        if refund_stats:
            assignments = ", ".join(f"{stat} = {stat} - ?" for stat in refund_stats)
            db.execute(
                f"UPDATE characters SET {assignments} WHERE id = ?",
                (*refund_stats.values(), current["id"]),
            )
        if refund_stats:
            updated = db.execute("SELECT * FROM characters WHERE id = ?", (current["id"],)).fetchone()
            remaining_talents = set(owned) - set(reset_ids)
            new_stats = derived_combat_stats(updated, active_ids, remaining_talents)
            db.execute(
                "UPDATE characters SET current_health = ?, current_mana = ? WHERE id = ?",
                (min(current["current_health"], new_stats["max_health"]),
                 min(current["current_mana"], new_stats["max_mana"]), current["id"]),
            )
    db.execute(
        "UPDATE characters SET specialization_id = ?, talent_root_id = ? WHERE id = ? AND user_id = ?",
        (choice, RADIAL_GRAPHS[current["class_id"]]["root_id"], current["id"], g.user["id"]),
    )
    updated = db.execute(
        "SELECT * FROM characters WHERE id = ? AND user_id = ?",
        (current["id"], g.user["id"]),
    ).fetchone()
    remaining_talents = {
        row["talent_id"] for row in db.execute(
            "SELECT talent_id FROM character_talents WHERE character_id = ?",
            (current["id"],),
        ).fetchall()
    }
    new_stats = derived_combat_stats(updated, active_ids, remaining_talents)
    db.execute(
        "UPDATE characters SET current_health = ?, current_mana = ? WHERE id = ?",
        (min(updated["current_health"], new_stats["max_health"]),
         min(updated["current_mana"], new_stats["max_mana"]), current["id"]),
    )
    db.commit()
    selected = next(item for item in CLASS_SPECIALIZATIONS[current["class_id"]] if item["id"] == choice)
    if current["specialization_id"]:
        flash(f"Caminho alterado para {selected['name']}. Os pontos e atributos do caminho anterior foram devolvidos.", "success")
    else:
        flash(f"Caminho escolhido: {selected['name']}. Os outros dois ramos ficam bloqueados.", "success")
    return redirect(url_for("talents.tree"))
