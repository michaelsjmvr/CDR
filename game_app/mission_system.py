"""Difficulty progression, virtual rewards, and mission-loot rules."""

import random
from datetime import datetime, timezone

from .campaign import SEASON_1_PHASES, encounter_type

INVENTORY_CAPACITY = 30

DIFFICULTY_ORDER = ("risk_low", "risk_moderate", "risk_high", "risk_extreme")
DIFFICULTIES = {
    "risk_low": {
        "label": "Risco Baixo",
        "enemy_health_multiplier": 1.0,
        "enemy_damage_multiplier": 1.0,
        "extra_enemies": 0,
        "gold_base_per_monster": 5,
        "phase_bonus_gold": 100,
        "boss_bonus_gold": 150,
        "third_chest_chance": 0.15,
        "boss_rarity_weights": (75, 20, 4, 1),
    },
    "risk_moderate": {
        "label": "Risco Moderado",
        "enemy_health_multiplier": 1.2,
        "enemy_damage_multiplier": 1.25,
        "extra_enemies": 1,
        "gold_base_per_monster": 10,
        "phase_bonus_gold": 200,
        "boss_bonus_gold": 300,
        "third_chest_chance": 0.35,
        "boss_rarity_weights": (58, 28, 12, 2),
    },
    "risk_high": {
        "label": "Risco Alto",
        "enemy_health_multiplier": 1.75,
        "enemy_damage_multiplier": 1.8,
        "extra_enemies": 0,
        "gold_base_per_monster": 20,
        "phase_bonus_gold": 350,
        "boss_bonus_gold": 500,
        "third_chest_chance": 0.6,
        "boss_rarity_weights": (34, 36, 25, 5),
    },
    "risk_extreme": {
        "label": "Risco Extremo",
        "enemy_health_multiplier": 2.4,
        "enemy_damage_multiplier": 2.5,
        "extra_enemies": 0,
        "gold_base_per_monster": 30,
        "phase_bonus_gold": 500,
        "boss_bonus_gold": 800,
        "third_chest_chance": 0.85,
        "boss_rarity_weights": (12, 23, 40, 25),
    },
}

RARITY_LABELS = {
    "common": "Comum",
    "rare": "Raro",
    "epic": "Épico",
    "legendary": "Lendário",
}
RARITY_SALVAGE_GOLD = {
    "common": 25,
    "rare": 75,
    "epic": 200,
    "legendary": 500,
}


def difficulty_state(db, user_id: int) -> list[dict]:
    completed = {key: set() for key in DIFFICULTY_ORDER}
    for row in db.execute(
        """SELECT difficulty, phase FROM mission_progress
           WHERE user_id = ?""",
        (user_id,),
    ).fetchall():
        if row["difficulty"] in completed:
            completed[row["difficulty"]].add(row["phase"])

    states = []
    previous_complete = True
    for difficulty in DIFFICULTY_ORDER:
        phases = completed[difficulty]
        unlocked = previous_complete
        available = []
        if unlocked:
            for phase in range(1, SEASON_1_PHASES + 1):
                if phase in phases or phase == 1 or phase - 1 in phases:
                    available.append(phase)
        states.append({
            "key": difficulty,
            "label": DIFFICULTIES[difficulty]["label"],
            "unlocked": unlocked,
            "completed_phases": phases,
            "available_phases": available,
            "completion_count": len(phases),
        })
        previous_complete = unlocked and len(phases) == SEASON_1_PHASES
    return states


def can_access_mission(db, user_id: int, difficulty: str, phase: int) -> bool:
    if difficulty not in DIFFICULTIES or not 1 <= phase <= SEASON_1_PHASES:
        return False
    state = next(
        item for item in difficulty_state(db, user_id)
        if item["key"] == difficulty
    )
    return state["unlocked"] and phase in state["available_phases"]


def gold_for_monster(difficulty: str, enemy_level: int) -> int:
    """Return the candidate integer Ouro drop, scaled by risk and level."""
    config = DIFFICULTIES.get(difficulty)
    if config is None:
        raise ValueError("Dificuldade inválida.")
    return config["gold_base_per_monster"] + max(0, min(100, enemy_level // 10))


def phase_gold_bonus(difficulty: str, *, boss_phase: bool) -> int:
    config = DIFFICULTIES.get(difficulty)
    if config is None:
        raise ValueError("Dificuldade inválida.")
    return config["phase_bonus_gold"] + (
        config["boss_bonus_gold"] if boss_phase else 0
    )


def roll_chest_rarities(
    difficulty: str,
    phase: int,
    *,
    rng=None,
) -> list[str]:
    """Return chest-loot rarities; non-boss phases never drop Epic/Legendary."""
    config = DIFFICULTIES.get(difficulty)
    if config is None:
        raise ValueError("Dificuldade inválida.")
    rng = rng or random.SystemRandom()
    encounter = encounter_type(phase, 10)
    if encounter == "boss":
        chest_count = 2 + int(rng.random() < config["third_chest_chance"])
        rarities = ("common", "rare", "epic", "legendary")
        weights = config["boss_rarity_weights"]
        return [rng.choices(rarities, weights=weights, k=1)[0] for _ in range(chest_count)]

    rare_chance = 0.30 if encounter == "miniboss" else 0.15
    return ["rare" if rng.random() < rare_chance else "common"]


def format_gold(amount: int) -> str:
    value = max(0, int(amount))
    return f"{value:,}".replace(",", ".")


class InventoryCapacityError(ValueError):
    """Raised when the selected staging loot exceeds remaining inventory slots."""


def active_mission_run(db, user_id: int, character_id: int):
    return db.execute(
        """SELECT r.* FROM mission_runs r
           WHERE r.user_id = ? AND r.character_id = ? AND r.status = 'active'
             AND r.id = (
                 SELECT active.id FROM mission_runs active
                 WHERE active.user_id = ? AND active.status = 'active'
                 ORDER BY active.id DESC LIMIT 1
             )
             AND NOT EXISTS (
                 SELECT 1 FROM staging_inventory s
                 WHERE s.user_id = r.user_id AND s.status = 'pending'
             )
           LIMIT 1""",
        (user_id, character_id, user_id),
    ).fetchone()


def active_account_mission_run(db, user_id: int):
    return db.execute(
        """SELECT * FROM mission_runs
           WHERE user_id = ? AND status = 'active'
           ORDER BY id DESC LIMIT 1""",
        (user_id,),
    ).fetchone()


def pending_mission_run(db, user_id: int, character_id: int | None = None):
    params = [user_id]
    character_filter = ""
    if character_id is not None:
        character_filter = "AND r.character_id = ?"
        params.append(character_id)
    return db.execute(
        f"""SELECT r.* FROM mission_runs r
            WHERE r.user_id = ? {character_filter}
              AND EXISTS (
                  SELECT 1 FROM staging_inventory s
                  WHERE s.mission_run_id = r.id AND s.status = 'pending'
              )
            ORDER BY r.id DESC LIMIT 1""",
        params,
    ).fetchone()


def _insert_gold_credit(
    db,
    user_id: int,
    run_id: int,
    source_key: str,
    transaction_type: str,
    amount_gold: int,
) -> int:
    if amount_gold <= 0:
        return 0
    result = db.execute(
        """INSERT OR IGNORE INTO gold_ledger
           (user_id, mission_run_id, source_key, transaction_type, amount_gold, created_at)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (
            user_id,
            run_id,
            source_key,
            transaction_type,
            amount_gold,
            datetime.now(timezone.utc).isoformat(),
        ),
    )
    if result.rowcount:
        db.execute(
            "UPDATE users SET wallet_gold = wallet_gold + ? WHERE id = ?",
            (amount_gold, user_id),
        )
        return amount_gold
    return 0


def credit_gold_monster_drop(
    db,
    user_id: int,
    character_id: int,
    enemy_id: int,
    enemy_level: int,
) -> int:
    run = active_mission_run(db, user_id, character_id)
    if run is None:
        return 0
    amount = gold_for_monster(run["difficulty"], enemy_level)
    credited = _insert_gold_credit(
        db,
        user_id,
        run["id"],
        f"monster:{run['id']}:{enemy_id}",
        "monster_drop",
        amount,
    )
    if credited:
        db.execute(
            """UPDATE mission_runs SET monster_gold = monster_gold + ?
               WHERE id = ?""",
            (credited, run["id"]),
        )
    return credited


def complete_mission(
    db,
    user_id: int,
    character_id: int,
    phase: int,
    *,
    now: float,
    rng=None,
) -> dict:
    run = active_mission_run(db, user_id, character_id)
    if run is None or run["phase"] != phase:
        raise ValueError("Não há missão ativa correspondente a esta fase.")
    if not db.execute(
        "UPDATE mission_runs SET status = 'completed' WHERE id = ? AND status = 'active'",
        (run["id"],),
    ).rowcount:
        raise ValueError("Esta missão já foi encerrada.")

    boss_phase = encounter_type(phase, 10) == "boss"
    bonus = phase_gold_bonus(run["difficulty"], boss_phase=boss_phase)
    _insert_gold_credit(
        db,
        user_id,
        run["id"],
        f"phase:{run['id']}",
        "phase_bonus",
        bonus,
    )
    completed_at = datetime.now(timezone.utc).isoformat()
    elapsed_seconds = max(0.0, now - run["start_time"])
    db.execute(
        """INSERT INTO mission_progress
           (user_id, difficulty, phase, completed_at, best_time_seconds)
           VALUES (?, ?, ?, ?, ?)
           ON CONFLICT(user_id, difficulty, phase) DO UPDATE SET
               completed_at = excluded.completed_at,
               best_time_seconds = CASE
                   WHEN mission_progress.best_time_seconds IS NULL
                     OR excluded.best_time_seconds < mission_progress.best_time_seconds
                   THEN excluded.best_time_seconds
                   ELSE mission_progress.best_time_seconds
               END,
               completion_count = mission_progress.completion_count + 1""",
        (user_id, run["difficulty"], phase, completed_at, elapsed_seconds),
    )
    rarities = roll_chest_rarities(run["difficulty"], phase, rng=rng)
    for index, rarity in enumerate(rarities, start=1):
        db.execute(
            """INSERT INTO staging_inventory
               (mission_run_id, user_id, chest_index, item_name, rarity,
                salvage_value_gold, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                run["id"],
                user_id,
                index,
                f"Baú de Missão · {DIFFICULTIES[run['difficulty']]['label']} · Fase {phase}",
                rarity,
                RARITY_SALVAGE_GOLD[rarity],
                completed_at,
            ),
        )
    db.execute(
        """UPDATE mission_runs
           SET phase_bonus_gold = ?, completion_time_seconds = ?, chest_count = ?,
               completed_at = ?
           WHERE id = ?""",
        (bonus, elapsed_seconds, len(rarities), completed_at, run["id"]),
    )
    totals = db.execute(
        """SELECT COALESCE(SUM(amount_gold), 0) FROM gold_ledger
           WHERE mission_run_id = ?""",
        (run["id"],),
    ).fetchone()[0]
    return {
        "run_id": run["id"],
        "difficulty": run["difficulty"],
        "phase": phase,
        "elapsed_seconds": elapsed_seconds,
        "monster_gold": run["monster_gold"],
        "phase_bonus_gold": bonus,
        "total_gold": totals,
        "chest_rarities": rarities,
    }


def resolve_staging_inventory(
    db,
    user_id: int,
    run_id: int,
    kept_item_ids: set[int],
) -> dict:
    run = db.execute(
        "SELECT id FROM mission_runs WHERE id = ? AND user_id = ? AND status = 'completed'",
        (run_id, user_id),
    ).fetchone()
    if run is None:
        raise ValueError("Espólios de missão não encontrados.")
    staged = db.execute(
        """SELECT * FROM staging_inventory
           WHERE mission_run_id = ? AND user_id = ? AND status = 'pending'
           ORDER BY chest_index""",
        (run_id, user_id),
    ).fetchall()
    available_ids = {row["id"] for row in staged}
    if not kept_item_ids.issubset(available_ids):
        raise ValueError("Um ou mais itens selecionados não pertencem a esta missão.")
    current_count = db.execute(
        "SELECT COUNT(*) FROM inventory_items WHERE user_id = ?",
        (user_id,),
    ).fetchone()[0]
    if current_count + len(kept_item_ids) > INVENTORY_CAPACITY:
        raise InventoryCapacityError(
            f"Selecione no máximo {INVENTORY_CAPACITY - current_count} item(ns) para manter."
        )

    for item in staged:
        if item["id"] in kept_item_ids:
            result = db.execute(
                """INSERT INTO inventory_items
                   (user_id, item_name, rarity, salvage_value_gold,
                    obtained_from_run_id, created_at)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    user_id,
                    item["item_name"],
                    item["rarity"],
                    item["salvage_value_gold"],
                    run_id,
                    item["created_at"],
                ),
            )
            db.execute(
                """UPDATE staging_inventory
                   SET status = 'claimed', inventory_item_id = ? WHERE id = ?""",
                (result.lastrowid, item["id"]),
            )
        else:
            db.execute(
                "UPDATE staging_inventory SET status = 'discarded' WHERE id = ?",
                (item["id"],),
            )
    return {
        "kept_count": len(kept_item_ids),
        "discarded_count": len(available_ids - kept_item_ids),
        "inventory_count": current_count + len(kept_item_ids),
    }


def sell_inventory_item(db, user_id: int, item_id: int) -> int:
    item = db.execute(
        "SELECT * FROM inventory_items WHERE id = ? AND user_id = ?",
        (item_id, user_id),
    ).fetchone()
    if item is None:
        raise ValueError("Este item não pertence ao seu inventário.")
    db.execute("DELETE FROM inventory_items WHERE id = ?", (item_id,))
    return _insert_gold_credit(
        db,
        user_id,
        item["obtained_from_run_id"],
        f"sale:{item_id}",
        "item_sale",
        item["salvage_value_gold"],
    )


def discard_inventory_item(db, user_id: int, item_id: int) -> None:
    result = db.execute(
        "DELETE FROM inventory_items WHERE id = ? AND user_id = ?",
        (item_id, user_id),
    )
    if not result.rowcount:
        raise ValueError("Este item não pertence ao seu inventário.")
