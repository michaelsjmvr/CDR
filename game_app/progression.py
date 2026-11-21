"""Prototype progression values kept separate for easy balancing changes."""

import sqlite3

from .campaign import encounter_type
from .classes import CLASSES
from .mission_system import DIFFICULTIES

WAVES_PER_PHASE = 10
MAX_LEVEL = 400
ATTRIBUTE_POINTS_PER_LEVEL = 5
MAX_ATTRIBUTE_VALUE = 10000
LEGACY_POINTS_LEVEL_STEP = 10
LEGACY_POINTS_MILESTONE_STEP = 50
LEGACY_POINTS_BONUS_STEP = 25
CARD_XP_PER_ORB = 25
CARD_XP_PER_ORB_PREMIUM = 40
CARD_AUTO_PICK_SECONDS = 10
CARD_XP_FOR_CHOICE = 100
CARD_XP_PER_ACTIVE_CARD = 25


def card_xp_needed(active_cards: int) -> int:
    """Provisional card-choice threshold grows with the active collection."""
    return CARD_XP_FOR_CHOICE + max(0, active_cards) * CARD_XP_PER_ACTIVE_CARD
XP_BASE = 100
XP_PER_LEVEL = 25
ENEMY_XP_BASE = 20
ENEMY_XP_PER_LEVEL = 6
MINIBOSS_XP_MULTIPLIER = 3
BOSS_XP_MULTIPLIER = 5


def experience_needed(level: int) -> int:
    """Provisional XP curve; this is a tuning value, not a final rule."""
    return XP_BASE + level * XP_PER_LEVEL


def legacy_points_for_level(level: int) -> int:
    """Return Legacy points earned within a level-1-to-400 progression."""
    level = min(MAX_LEVEL, max(1, int(level)))
    return (
        level // LEGACY_POINTS_LEVEL_STEP
        + level // LEGACY_POINTS_MILESTONE_STEP
        + level // LEGACY_POINTS_BONUS_STEP
    )


def legacy_milestones_crossed(old_level: int, new_level: int) -> int:
    """Count 50-level milestones crossed while advancing."""
    old_level = min(MAX_LEVEL, max(1, int(old_level)))
    new_level = min(MAX_LEVEL, max(1, int(new_level)))
    return max(0, new_level // LEGACY_POINTS_MILESTONE_STEP
               - old_level // LEGACY_POINTS_MILESTONE_STEP)


def award_legacy_points(
    db: sqlite3.Connection,
    character_id: int,
    old_level: int,
    new_level: int,
) -> tuple[int, int]:
    """Grant earned Legacy points and return points and bonus milestones."""
    points_gained = max(
        0,
        legacy_points_for_level(new_level) - legacy_points_for_level(old_level),
    )
    milestones_gained = legacy_milestones_crossed(old_level, new_level)
    if points_gained:
        db.execute(
            "UPDATE characters SET legacy_points = legacy_points + ? WHERE id = ?",
            (points_gained, character_id),
        )
    return points_gained, milestones_gained


def phase_xp_budget_for_level(level: int) -> int:
    """Candidate phase budget: roughly six level thresholds, fixed on phase entry."""
    return experience_needed(min(MAX_LEVEL, max(1, level))) * 6


def enemies_in_wave(
    wave: int,
    phase: int = 1,
    difficulty: str = "risk_low",
) -> int:
    """Ramp density by wave, phase, and the Moderate risk enemy-count bonus."""
    if wave >= WAVES_PER_PHASE:
        count = 1
    else:
        phase_bonus = min(4, max(0, phase - 1) // 4)
        count = 3 + max(0, wave - 1) + phase_bonus
    config = DIFFICULTIES.get(difficulty)
    if config is None:
        raise ValueError("Dificuldade inválida.")
    if encounter_type(phase, wave) == "common":
        count += config["extra_enemies"]
    return count


def wave_xp_weight(phase: int, wave: int) -> int:
    encounter = encounter_type(phase, wave)
    if encounter == "boss":
        return BOSS_XP_MULTIPLIER
    if encounter == "miniboss":
        return MINIBOSS_XP_MULTIPLIER
    return 1


def phase_xp_weight_total(phase: int, difficulty: str = "risk_low") -> int:
    return sum(
        enemies_in_wave(wave, phase, difficulty) * wave_xp_weight(phase, wave)
        for wave in range(1, WAVES_PER_PHASE + 1)
    )


def wave_experience_reward(
    phase: int,
    wave: int,
    budget: int | None = None,
    difficulty: str = "risk_low",
) -> int:
    """The phase's fixed XP budget share attributed to this wave."""
    budget = budget if budget is not None else phase_xp_budget_for_level(1)
    total = phase_xp_weight_total(phase, difficulty)
    prior = sum(
        enemies_in_wave(item, phase, difficulty) * wave_xp_weight(phase, item)
        for item in range(1, wave)
    )
    weight = enemies_in_wave(wave, phase, difficulty) * wave_xp_weight(phase, wave)
    return (budget * (prior + weight)) // total - (budget * prior) // total


def enemy_experience_reward(
    phase: int,
    wave: int,
    enemy_index: int = 0,
    budget: int | None = None,
    difficulty: str = "risk_low",
) -> int:
    """Distribute fixed phase XP by enemy weight; boss/miniboss get larger shares."""
    budget = budget if budget is not None else phase_xp_budget_for_level(1)
    total = phase_xp_weight_total(phase, difficulty)
    prior = sum(
        enemies_in_wave(item, phase, difficulty) * wave_xp_weight(phase, item)
        for item in range(1, wave)
    )
    weight = wave_xp_weight(phase, wave)
    offset = prior + enemy_index * weight
    return (budget * (offset + weight)) // total - (budget * offset) // total


CLASS_AUTO_DISTRIBUTION = {
    "guardian": {"strength": 40, "vitality": 30, "agility": 20, "energy": 10},
    "ash_weaver": {"energy": 40, "vitality": 25, "agility": 25, "strength": 10},
    "wild_scout": {"agility": 40, "strength": 30, "vitality": 20, "energy": 10},
    "rune_blade": {"strength": 30, "energy": 30, "agility": 25, "vitality": 15},
}


def distribute_attribute_points(class_id: str, stats: dict, points: int) -> tuple[dict, int, int]:
    """Apply points with the class profile, returning stats, leftover and spent."""
    base = CLASSES[class_id]["base_attributes"]
    weights = CLASS_AUTO_DISTRIBUTION.get(
        class_id,
        {"strength": 40, "vitality": 30, "agility": 20, "energy": 10},
    )
    distributed = dict(stats)
    remaining = max(0, int(points))
    initial = remaining
    while remaining:
        candidates = [key for key in weights if distributed[key] < MAX_ATTRIBUTE_VALUE]
        target = min(
            candidates,
            key=lambda key: (distributed[key] - base[key]) / weights[key],
        ) if candidates else None
        if target is None:
            break
        distributed[target] += 1
        remaining -= 1
    return distributed, remaining, initial - remaining


def award_attribute_points(db, character_id: int, levels_gained: int, is_premium: bool) -> tuple[int, int]:
    """Grant 5 points per level, optionally allocating them for opted-in VIPs."""
    earned = max(0, levels_gained) * ATTRIBUTE_POINTS_PER_LEVEL
    if not earned:
        row = db.execute("SELECT attribute_points FROM characters WHERE id = ?", (character_id,)).fetchone()
        return (row[0] if row else 0, 0)
    character = db.execute(
        "SELECT class_id, auto_allocate_attributes, strength, agility, vitality, energy, attribute_points "
        "FROM characters WHERE id = ?", (character_id,),
    ).fetchone()
    if not character:
        return 0, 0
    if not (is_premium and character["auto_allocate_attributes"]):
        db.execute("UPDATE characters SET attribute_points = attribute_points + ? WHERE id = ?", (earned, character_id))
        return character["attribute_points"] + earned, 0

    stats = {key: character[key] for key in ("strength", "agility", "vitality", "energy")}
    stats, remaining, allocated = distribute_attribute_points(character["class_id"], stats, earned)
    db.execute(
        "UPDATE characters SET strength = ?, agility = ?, vitality = ?, energy = ?, "
        "attribute_points = attribute_points + ? WHERE id = ?",
        (*[stats[key] for key in ("strength", "agility", "vitality", "energy")], remaining, character_id),
    )
    return character["attribute_points"] + remaining, allocated


def add_experience(level: int, experience: int, reward: int) -> tuple[int, int, int]:
    """Apply XP, carry overflow between levels, and stop at level cap."""
    experience += reward
    levels_gained = 0
    while level < MAX_LEVEL:
        threshold = experience_needed(level)
        if experience < threshold:
            break
        experience -= threshold
        level += 1
        levels_gained += 1
    if level == MAX_LEVEL:
        experience = 0
    return level, experience, levels_gained
