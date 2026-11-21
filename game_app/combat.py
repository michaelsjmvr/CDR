"""Temporary combat values for the first playable HUD prototype."""

import math
import random

from .abilities import SKILLS, SPECIALIZATION_ABILITIES, active_class_skill
from .cards import card_modifiers
from .campaign import encounter_type
from .classes import CLASSES
from .map_geometry import terminal_vilar_collides, terminal_vilar_map_config
from .progression import MAX_LEVEL, WAVES_PER_PHASE
from .talents import NODE_INDEX

BASIC_ATTACK_DAMAGE = 35
BASIC_ATTACK_COOLDOWN = 1.0
DASH_COOLDOWN = 3.0
CRITICAL_DAMAGE_MULTIPLIER = 1.5
CRITICAL_CHANCE_PER_AGILITY = 0.0001
DODGE_CHANCE_PER_AGILITY = 0.0001
PHASE_PREPARATION_SECONDS = 30

WARRIOR_SKILLS = SKILLS


def derived_combat_stats(character, active_card_ids=(), purchased_talents=()):
    """Return the candidate, class-aware combat values used by the live server."""
    level = max(1, int(character["level"]))
    strength = max(0, int(character["strength"]))
    agility = max(0, int(character["agility"]))
    vitality = max(0, int(character["vitality"]))
    energy = max(0, int(character["energy"]))
    class_id = character["class_id"]
    cards = card_modifiers(active_card_ids)
    if class_id == "guardian":
        damage = 10 + .5 * strength + .2 * agility
        health = 120 + 1.5 * (level - 1) + 2 * vitality
        mana = 60 + level - 1 + 1.5 * energy
    elif class_id == "ash_weaver":
        damage = 20 + .35 * energy + .2 * agility + .1 * strength
        health = 120 + 1.5 * (level - 1) + 2 * vitality
        mana = 60 + level - 1 + 1.5 * energy
    elif class_id == "wild_scout":
        damage = 15 + .35 * agility + .2 * strength
        health = 120 + 1.5 * (level - 1) + 2 * vitality
        mana = 60 + level - 1 + 1.5 * energy
    else:
        damage = 10 + .4 * strength + .4 * energy + .1 * agility
        health = 120 + 1.5 * (level - 1) + 2 * vitality
        mana = 60 + level - 1 + 1.5 * energy
    character_keys = character.keys()
    specialization_id = (
        character["specialization_id"]
        if "specialization_id" in character_keys else None
    )
    specialization = SPECIALIZATION_ABILITIES.get(specialization_id)
    if specialization and specialization["class_id"] == class_id:
        for key, value in specialization["passive"]["modifiers"].items():
            cards[key] = cards.get(key, 0) + value
    skill_damage_by_id = {}
    for talent_id in purchased_talents:
        node = NODE_INDEX.get(talent_id)
        if (
            node
            and node.get("class_id") == class_id
            and node.get("specialization_id") == specialization_id
        ):
            for key, value in node.get("combat_modifiers", {}).items():
                cards[key] = cards.get(key, 0) + value
            if node.get("skill_id") and node.get("skill_damage_bonus"):
                skill_id = node["skill_id"]
                skill_damage_by_id[skill_id] = (
                    skill_damage_by_id.get(skill_id, 0)
                    + node["skill_damage_bonus"]
                )
    cards["damage_reduction"] = min(.50, cards.get("damage_reduction", 0))
    cards["dodge_chance"] = min(
        .35, cards.get("dodge_chance", 0) + agility * DODGE_CHANCE_PER_AGILITY
    )
    cards["critical_chance"] = min(
        .50, cards.get("critical_chance", 0) + agility * CRITICAL_CHANCE_PER_AGILITY
    )
    cards["skill_burst_chance"] = min(.50, cards.get("skill_burst_chance", 0))
    basic_damage_exact = damage * (1 + cards.get("damage", 0))
    skill_damage_exact = damage * 1.5 * (
        1 + cards.get("damage", 0) + cards.get("skill_damage", 0)
    )
    return {
        "max_health": max(1, round(health * (1 + cards.get("max_health", 0)))),
        "max_mana": max(1, round(mana * (1 + cards.get("max_mana", 0)))),
        "basic_damage": max(1, round(basic_damage_exact)),
        "skill_damage": max(1, round(skill_damage_exact)),
        "basic_damage_exact": basic_damage_exact,
        "skill_damage_exact": skill_damage_exact,
        "skill_damage_by_id": skill_damage_by_id,
        "skill_mana": 25,
        "basic_cooldown": 1.15,
        "skill_cooldown": 6.0,
        "dash_cooldown": DASH_COOLDOWN,
        "cooldown_multiplier": max(.50, 1 - cards.get("cooldown_reduction", 0)),
        "damage_reduction": cards.get("damage_reduction", 0),
        "ranged_reduction": min(.50, cards.get("ranged_reduction", 0)),
        "move_speed_multiplier": min(
            1.50,
            (1 + min(.25, agility * .001)) * (1 + cards.get("move_speed", 0)),
        ),
        "attack_range_multiplier": 1 + cards.get("attack_range", 0),
        "critical_chance": cards.get("critical_chance", 0),
        "dodge_chance": cards.get("dodge_chance", 0),
        "projectile_damage": cards.get("projectile_damage", 0),
        "elemental_damage": cards.get("elemental_damage", 0),
        "common_damage_multiplier": 1 + cards.get("common_damage", 0),
        "boss_damage_multiplier": 1 + cards.get("boss_damage", 0),
        "critical_heal": cards.get("critical_heal", 0),
        "skill_healing": cards.get("skill_healing", 0),
        "cooldown_refund_on_kill": cards.get("cooldown_refund_on_kill", 0),
        "skill_burst_chance": cards.get("skill_burst_chance", 0),
        "skill_burst_damage": cards.get("skill_burst_damage", 0),
        "wave_heal": cards.get("wave_heal", 0),
        "low_health_reduction": cards.get("low_health_reduction", 0),
        "attack_streak_damage": cards.get("attack_streak_damage", 0),
        "attack_streak_cap": min(5, int(cards.get("attack_streak_cap", 0))),
        "mana_on_kill": cards.get("mana_on_kill", 0),
        "life_steal": cards.get("life_steal", 0),
        "damage_reflection": cards.get("damage_reflection", 0),
    }


def calculate_attack_damage(
    combat_stats,
    skill,
    damage_type,
    element,
    phase,
    wave,
    critical=False,
    skill_burst=False,
    attack_streak=0,
):
    """Apply the live damage modifiers in the same order used by combat events."""
    damage = (
        round(
            combat_stats["skill_damage"] * skill["damage_multiplier"]
            * (1 + combat_stats.get("skill_damage_by_id", {}).get(skill["id"], 0))
        )
        if skill else combat_stats["basic_damage"]
    )
    if skill and skill.get("projectile"):
        damage = round(damage * (1 + combat_stats["projectile_damage"]))
    if damage_type == "magical" and element:
        damage = round(damage * (1 + combat_stats["elemental_damage"]))
    if encounter_type(phase, wave) in {"boss", "miniboss"}:
        damage = round(damage * combat_stats["boss_damage_multiplier"])
    else:
        damage = round(damage * combat_stats["common_damage_multiplier"])
    if skill and skill_burst:
        damage = round(damage * (1 + combat_stats["skill_burst_damage"]))
    if combat_stats["attack_streak_cap"]:
        streak_count = min(combat_stats["attack_streak_cap"], attack_streak)
        damage = round(
            damage * (1 + streak_count * combat_stats["attack_streak_damage"])
        )
    if critical:
        damage = round(damage * CRITICAL_DAMAGE_MULTIPLIER)
    damage = max(1, damage)
    if encounter_type(phase, wave) == "boss" and damage_type == "magical":
        affinity = boss_affinity(phase)
        if element and affinity["key"] == element:
            damage = max(1, round(damage * (1 - affinity["resistance"])))
    return damage


def combat_summary(character, active_card_ids=(), purchased_talents=()):
    """Return player-facing estimates for the character's current combat effects."""
    stats = derived_combat_stats(character, active_card_ids, purchased_talents)
    skill = active_class_skill(
        character["class_id"],
        character["specialization_id"] if "specialization_id" in character.keys() else None,
        purchased_talents,
    )
    element_names = {
        "fire": "Fogo",
        "ice": "Gelo",
        "lightning": "Raio",
        "umbral": "Umbral",
    }
    skill_damage = round(
        stats["skill_damage"] * skill["damage_multiplier"]
        * (1 + stats["skill_damage_by_id"].get(skill["id"], 0))
    )
    if skill.get("projectile"):
        skill_damage = round(skill_damage * (1 + stats["projectile_damage"]))
    damage_type = skill.get("damage_type")
    if damage_type == "magical" and skill.get("element"):
        skill_damage = round(skill_damage * (1 + stats["elemental_damage"]))
    skill_damage = round(skill_damage, 1)
    elemental_damage = 0
    if skill.get("damage_type") == "magical" and skill.get("element"):
        elemental_damage = skill_damage
    return {
        "basic_damage_exact": stats["basic_damage_exact"],
        "skill_damage_exact": stats["skill_damage_exact"],
        "physical_damage_exact": skill_damage if damage_type == "physical" else 0,
        "magical_damage_exact": skill_damage if damage_type == "magical" else 0,
        "projectile_damage_exact": (
            skill_damage
            if skill.get("projectile") else 0
        ),
        "elemental_damage_exact": elemental_damage,
        "elemental_name": element_names.get(skill.get("element"), ""),
        "life_steal": stats["life_steal"],
        "damage_reflection": stats["damage_reflection"],
        "max_health": stats["max_health"],
        "max_mana": stats["max_mana"],
        "basic_cooldown": cooldown_for_agility(
            stats["basic_cooldown"] * stats["cooldown_multiplier"],
            character["agility"],
        ),
        "skill_cooldown": cooldown_for_agility(
            stats["skill_cooldown"] * stats["cooldown_multiplier"],
            character["agility"],
        ),
        "dash_cooldown": cooldown_for_agility(
            stats["dash_cooldown"] * stats["cooldown_multiplier"],
            character["agility"],
        ),
        "move_speed_bonus": round((stats["move_speed_multiplier"] - 1) * 100, 1),
        "critical_chance": stats["critical_chance"],
        "critical_damage_bonus": 50,
        "critical_heal": stats["critical_heal"],
        "dodge_chance": stats["dodge_chance"],
        "attack_range": (
            CLASSES[character["class_id"]]["base_attack_range"]
            * stats["attack_range_multiplier"]
        ),
        "skill_range": (
            CLASSES[character["class_id"]]["base_skill_range"]
            * stats["attack_range_multiplier"]
        ),
        "damage_reduction": stats["damage_reduction"],
        "ranged_reduction": stats["ranged_reduction"],
    }


def enemy_max_health(
    phase: int,
    wave: int,
    waves_per_phase: int = 10,
    difficulty: str = "risk_low",
) -> int:
    """Scale enemy HP to the approved TTK targets through the level-400 cap."""
    from .mission_system import DIFFICULTIES

    config = DIFFICULTIES.get(difficulty)
    if config is None:
        raise ValueError("Dificuldade inválida.")
    level = enemy_level(phase, wave)
    base_common = round(143 * 1.05 * (1 + .06 * max(0, level - 6)))
    cycle_progress = (level - 1) / (MAX_LEVEL - 1)
    balance_progress = min(1.0, max(0.0, (level - 6) / (MAX_LEVEL - 6)))
    encounter = encounter_type(phase, wave)
    if encounter == "boss":
        boss_scale = min(1.7, .8 + 3.6 * balance_progress)
        health = round(
            base_common * 18.0 * (.75 + .25 * cycle_progress) * boss_scale
        )
    elif encounter == "miniboss":
        miniboss_scale = min(1.65, 1 + .9 * math.sqrt(balance_progress))
        health = round(
            base_common * 6.5 * (.75 + .25 * cycle_progress) * miniboss_scale
        )
    else:
        common_scale = 1.45 + .65 * balance_progress
        health = round(base_common * common_scale)
    return max(1, round(health * config["enemy_health_multiplier"]))


def scale_enemy_attack_damage(
    base_damage: int,
    phase: int,
    wave: int,
    difficulty: str = "risk_low",
) -> int:
    """Increase incoming damage by enemy level, stopping at the level-400 cap."""
    from .mission_system import DIFFICULTIES

    config = DIFFICULTIES.get(difficulty)
    if config is None:
        raise ValueError("Dificuldade inválida.")
    level = enemy_level(phase, wave)
    scaled = base_damage + .65 * max(0, level - 6)
    return max(1, round(scaled * config["enemy_damage_multiplier"]))


def enemy_spawn_positions(
    seed: str,
    count: int,
    player_x: float = 1200,
    player_y: float = 900,
    phase: int | None = None,
):
    """Choose reproducible random map positions with clearance around the player and enemies."""
    rng = random.Random(seed)
    positions = []
    min_player_distance = 380
    min_enemy_distance = 92
    spawn_bounds = (
        terminal_vilar_map_config()["spawn_bounds"]
        if phase == 1
        else {"min_x": 180, "max_x": 2220, "min_y": 180, "max_y": 1620}
    )
    min_x = math.ceil(spawn_bounds["min_x"])
    max_x = math.floor(spawn_bounds["max_x"])
    min_y = math.ceil(spawn_bounds["min_y"])
    max_y = math.floor(spawn_bounds["max_y"])

    def is_valid(candidate):
        x, y = candidate
        if math.hypot(x - player_x, y - player_y) < min_player_distance:
            return False
        if phase == 1 and terminal_vilar_collides(x, y, 28):
            return False
        return not any(
            math.hypot(x - px, y - py) < min_enemy_distance
            for px, py in positions
        )

    for _ in range(max(1, count) * 500):
        candidate = (rng.randint(min_x, max_x), rng.randint(min_y, max_y))
        if not is_valid(candidate):
            continue
        positions.append(candidate)
        if len(positions) >= count:
            return positions

    for y in range(min_y, max_y + 1, 120):
        for x in range(min_x, max_x + 1, 120):
            if not is_valid((x, y)):
                continue
            positions.append((x, y))
            if len(positions) >= count:
                return positions
    return positions

# Protótipo temporário de auto-poções VIP. Valores serão recalibrados com
# inventário, obtenção e economia de consumíveis.
AUTO_POTION_HEALTH_THRESHOLD = 0.50
AUTO_POTION_HEALTH_RESTORE = 0.30
AUTO_POTION_HEALTH_COOLDOWN = 8.0
AUTO_POTION_MANA_THRESHOLD = 0.30
AUTO_POTION_MANA_RESTORE = 0.40
AUTO_POTION_MANA_COOLDOWN = 12.0

ENEMY_NAMES = ("Lacaio das Cinzas", "Sentinela Rachado")
MINI_BOSS_NAME = "Arauto das Cinzas"
BOSS_NAME = "Colosso do Umbral"
ENEMY_ATTACKS = {
    "melee_slam": {
        "name": "Golpe de Cinzas", "damage": 25, "cooldown": 3.8,
        "windup_ms": 1050, "radius": 58, "projectile": False,
    },
    "ranged_shadow_bolt": {
        "name": "Projétil Sombrio", "damage": 20, "cooldown": 4.2,
        "windup_ms": 1350, "radius": 42, "projectile": True,
    },
    "miniboss_groundbreak": {
        "name": "Ruptura do Arauto", "damage": 42, "cooldown": 7.0,
        "windup_ms": 1650, "radius": 100, "projectile": False,
    },
    "miniboss_shards": {
        "name": "Estilhaços da Cripta", "damage": 30, "cooldown": 7.0,
        "windup_ms": 1450, "radius": 48, "projectile": True,
    },
    "boss_shadowfall": {
        "name": "Chuva do Umbral", "damage": 48, "cooldown": 8.5,
        "windup_ms": 2050, "radius": 62, "projectile": True,
    },
    "boss_rift_line": {
        "name": "Fenda do Umbral", "damage": 42, "cooldown": 8.5,
        "windup_ms": 1850, "radius": 46, "projectile": True,
    },
}
ELEMENTAL_AFFINITIES = (
    {"key": "fire", "name": "Fogo", "color": "#e27b50"},
    {"key": "ice", "name": "Gelo", "color": "#78c9d8"},
    {"key": "lightning", "name": "Raio", "color": "#d7bd65"},
    {"key": "umbral", "name": "Umbral", "color": "#a98bd5"},
)
PROTOTYPE_BOSS_RESISTANCE = 0.30


def boss_affinity(phase: int) -> dict:
    """Assign one rotating elemental counter to each ten-phase act boss."""
    act_number = (max(1, phase) + 9) // 10
    affinity = ELEMENTAL_AFFINITIES[(act_number - 1) % len(ELEMENTAL_AFFINITIES)]
    return {**affinity, "resistance": PROTOTYPE_BOSS_RESISTANCE}


def enemy_name(
    enemy_index: int, wave: int, waves_per_phase: int = 10, phase: int = 1
) -> str:
    """Return the display name for the encounter scheduled in this phase."""
    encounter = encounter_type(phase, wave)
    if encounter == "boss":
        return BOSS_NAME
    if encounter == "miniboss":
        return MINI_BOSS_NAME
    return ENEMY_NAMES[enemy_index % len(ENEMY_NAMES)]


def enemy_attack_style(
    enemy_index: int, wave: int, waves_per_phase: int = 10, phase: int = 1
) -> str:
    """Assign a clear attack role to the encounter scheduled in this phase."""
    encounter = encounter_type(phase, wave)
    if encounter == "boss":
        return "boss"
    if encounter == "miniboss":
        return "miniboss"
    return "ranged" if enemy_index % 2 else "melee"


def cooldown_for_agility(base_cooldown: float, agility: int) -> float:
    """Agility shortens combat cooldowns by 0.5% per point, capped at 50%."""
    reduction = min(0.5, max(0, agility) * 0.005)
    return base_cooldown * (1 - reduction)


def enemy_level(phase: int, wave: int) -> int:
    return min(MAX_LEVEL, max(1, phase * 5 + wave))
