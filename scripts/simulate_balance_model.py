"""Diagnostic simulator for the submitted class formulas; does not change gameplay."""

from __future__ import annotations

import sys
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from game_app.classes import CLASSES
from game_app.combat import (
    ENEMY_ATTACKS,
    PROTOTYPE_BOSS_RESISTANCE,
    boss_affinity,
    derived_combat_stats,
    enemy_spawn_positions,
    enemy_max_health,
)
from game_app.progression import (
    CLASS_AUTO_DISTRIBUTION,
    MAX_LEVEL,
    enemy_experience_reward,
    experience_needed,
    enemies_in_wave,
    phase_xp_budget_for_level,
)

CHECKPOINTS = (1, 100, 220, 400)
STAT_KEYS = ("strength", "agility", "vitality", "energy")

# Representative manual specializations for comparison; percentages describe
# newly earned points, not class base stats or an approved optimal build.
MANUAL_BUILD_WEIGHTS = {
    "guardian": {"strength": 0.60, "agility": 0.15, "vitality": 0.25, "energy": 0.00},
    "ash_weaver": {"strength": 0.00, "agility": 0.15, "vitality": 0.25, "energy": 0.60},
    "wild_scout": {"strength": 0.20, "agility": 0.55, "vitality": 0.25, "energy": 0.00},
    "rune_blade": {"strength": 0.35, "agility": 0.10, "vitality": 0.20, "energy": 0.35},
}

# Candidate Premium/VIP auto-allocation presets mirror representative manual
# specializations. They remain separate from live weights until approved.
CANDIDATE_AUTO_DISTRIBUTION = {
    "guardian": {"strength": 60, "vitality": 25, "agility": 15, "energy": 0},
    "ash_weaver": {"energy": 60, "vitality": 25, "agility": 15, "strength": 0},
    "wild_scout": {"agility": 55, "vitality": 25, "strength": 20, "energy": 0},
    "rune_blade": {"strength": 35, "energy": 35, "vitality": 20, "agility": 10},
}

# First skill profiles for balance simulation only; none are live gameplay.
CANDIDATE_SKILLS = {
    "guardian": {
        "name": "Impacto do Umbral", "multiplier": 1.25, "mana": 18, "cooldown": 8.0,
        "target": "Alvo único corpo a corpo", "element": "Físico",
        "area": "Sem área", "status": "Quebra de escudo", "chance": 0.30,
        "duration": 4.0, "status_value": "reduz resistência em 15%",
        "target_limit": 1, "dot_rate": 0.0,
    },
    "ash_weaver": {
        "name": "Chama Crescente", "multiplier": 1.50, "mana": 24, "cooldown": 9.0,
        "target": "Até 3 alvos", "element": "Fogo", "area": "Círculo, raio 80",
        "status": "Queimadura", "chance": 1.00, "duration": 4.0,
        "status_value": "1,5% do dano da habilidade por segundo",
        "target_limit": 3, "dot_rate": 0.015,
    },
    "wild_scout": {
        "name": "Disparo Perfurante", "multiplier": 1.25, "mana": 18, "cooldown": 7.0,
        "target": "Até 3 alvos alinhados", "element": "Físico",
        "area": "Linha, largura 30", "status": "Sangramento", "chance": 0.35,
        "duration": 4.0, "status_value": "1,5% do dano da habilidade por segundo",
        "target_limit": 3, "dot_rate": 0.015,
    },
    "rune_blade": {
        "name": "Ruptura Rúnica", "multiplier": 1.25, "mana": 22, "cooldown": 8.0,
        "target": "Alvo único", "element": "Raio", "area": "Sem área",
        "status": "Paralisia", "chance": 0.20, "duration": 1.0,
        "status_value": "interrompe um telegráfico; chefe ganha 6 s de imunidade",
        "target_limit": 1, "dot_rate": 0.0,
    },
}

COMMON_HP_MULTIPLIER = 1.05
MINIBOSS_HP_MULTIPLIER = 6.7
BOSS_HP_MULTIPLIER = 18.0
# Cooperative boss-health multipliers are balance candidates only. Damage per
# hit is unchanged for now; group scaling needs playtest before approval.
COOP_BOSS_HEALTH_MULTIPLIER = {1: 1.0, 2: 1.6, 3: 2.2}
COOP_COMMON_HEALTH_MULTIPLIER = {1: 1.0, 2: 1.25, 3: 1.5}
COOP_COMMON_COUNT = {1: 3, 2: 4, 3: 5}
COOP_ENEMY_ATTACK_INTERVAL = 2.0
# Candidate correction for common waves only; simulation-only, not live combat.
CANDIDATE_COMMON_HP_SCALE = 0.45
CANDIDATE_COMMON_ATTACK_SCALE = 0.25


def auto_build_at_level(
    class_id: str, level: int, weights_by_class: dict[str, dict[str, int]] | None = None
) -> dict[str, int]:
    """Replicate weighted allocation with live or candidate class weights."""
    base = CLASSES[class_id]["base_attributes"]
    stats = dict(base)
    weights = (weights_by_class or CLASS_AUTO_DISTRIBUTION)[class_id]
    for _ in range(max(0, level - 1) * 5):
        eligible = [key for key in weights if weights[key] > 0 and stats[key] < 10_000]
        if not eligible:
            break
        target = min(eligible, key=lambda key: (stats[key] - base[key]) / weights[key])
        stats[target] += 1
    return stats


def candidate_auto_allocation_at_level(class_id: str, level: int) -> dict[str, int]:
    """Evaluate role-focused Premium/VIP auto-allocation without live changes."""
    return auto_build_at_level(class_id, level, CANDIDATE_AUTO_DISTRIBUTION)


def representative_manual_build(class_id: str, level: int) -> dict[str, int]:
    """Allocate points by class fantasy for a non-optimized manual baseline."""
    base = CLASSES[class_id]["base_attributes"]
    stats = dict(base)
    weights = MANUAL_BUILD_WEIGHTS[class_id]
    points = max(0, level - 1) * 5
    # Largest-remainder style allocation avoids losing points to rounding.
    exact = {key: points * weights[key] for key in STAT_KEYS}
    added = {key: math.floor(exact[key]) for key in STAT_KEYS}
    remainder = points - sum(added.values())
    order = sorted(STAT_KEYS, key=lambda key: (exact[key] - added[key], weights[key]), reverse=True)
    for key in order[:remainder]:
        added[key] += 1
    return {key: stats[key] + added[key] for key in STAT_KEYS}


def reference_outputs(class_id: str, level: int, stats: dict[str, int]) -> dict[str, float | str]:
    """Evaluate the received formulas without claiming they are adopted."""
    strength, agility = stats["strength"], stats["agility"]
    vitality, energy = stats["vitality"], stats["energy"]
    if class_id == "guardian":
        damage = (strength / 6, strength / 4)
        health = 35 + (level - 1) * 2 + vitality * 3
        mana = 10 + (level - 1) * .5 + energy
        defense, speed = agility / 3, agility / 15
    elif class_id == "ash_weaver":
        damage = (energy / 9, energy / 4)
        health = 30 + level - 1 + vitality * 2
        mana = (energy + level - 1) * 2
        defense, speed = agility / 4, agility / 10
    elif class_id == "wild_scout":
        damage = (agility / 8 + strength / 14, agility / 4 + strength / 8)
        health = 40 + level - 1 + vitality * 2
        mana = 6 + (level - 1) * 1.5 + energy * 1.5
        defense, speed = agility / 10, agility / 50
    else:
        physical = (strength / 6 + energy / 12, strength / 4 + energy / 8)
        magical = (energy / 9, energy / 4)
        health = 58 + level - 1 + vitality * 2
        mana = 8 + level - 1 + energy * 2
        defense, speed = agility / 5, agility / 15
        return {
            "damage": f"F {physical[0]:.1f}-{physical[1]:.1f}; M {magical[0]:.1f}-{magical[1]:.1f}",
            "health": health,
            "mana": mana,
            "defense": defense,
            "speed_index": speed,
        }
    return {
        "damage": f"{damage[0]:.1f}-{damage[1]:.1f}",
        "health": health,
        "mana": mana,
        "defense": defense,
        "speed_index": speed,
    }


def current_xp_projection() -> tuple[int, int]:
    """Count phases and monster kills under today's provisional XP formulas."""
    level, xp, phase, kills = 1, 0, 1, 0
    while level < MAX_LEVEL:
        phase_budget = phase_xp_budget_for_level(level)
        for wave in range(1, 11):
            enemy_count = enemies_in_wave(wave, phase)
            for enemy_index in range(enemy_count):
                xp += enemy_experience_reward(phase, wave, enemy_index, phase_budget)
                kills += 1
                while level < MAX_LEVEL and xp >= experience_needed(level):
                    xp -= experience_needed(level)
                    level += 1
                if level >= MAX_LEVEL:
                    return phase, kills
        phase += 1
    return phase, kills


def checkpoint_arenas() -> dict[int, tuple[int, int]]:
    """Find the phase/wave where today's XP curve first reaches each checkpoint."""
    level, xp = 1, 0
    arenas = {1: (1, 1)}
    for phase in range(1, 1000):
        phase_budget = phase_xp_budget_for_level(level)
        for wave in range(1, 11):
            enemy_count = enemies_in_wave(wave, phase)
            for enemy_index in range(enemy_count):
                xp += enemy_experience_reward(phase, wave, enemy_index, phase_budget)
                while level < MAX_LEVEL and xp >= experience_needed(level):
                    xp -= experience_needed(level)
                    level += 1
                    if level in CHECKPOINTS and level not in arenas:
                        arenas[level] = (phase, wave)
                if level >= MAX_LEVEL:
                    return arenas
    return arenas


def wave_entry_levels() -> dict[tuple[int, int], int]:
    """Track the level at each wave start using the fixed phase XP budget."""
    level, xp = 1, 0
    entries = {}
    for phase in range(1, 1000):
        phase_budget = phase_xp_budget_for_level(level)
        for wave in range(1, 11):
            entries[(phase, wave)] = level
            for enemy_index in range(enemies_in_wave(wave, phase)):
                xp += enemy_experience_reward(phase, wave, enemy_index, phase_budget)
                while level < MAX_LEVEL and xp >= experience_needed(level):
                    xp -= experience_needed(level)
                    level += 1
    return entries


def first_pass_model(class_id: str, level: int, stats: dict[str, int], arena: tuple[int, int]) -> dict[str, float]:
    """Small, gear-free proposal fitted to the approved solo combat targets."""
    strength, agility = stats["strength"], stats["agility"]
    vitality, energy = stats["vitality"], stats["energy"]
    if class_id == "guardian":
        basic_damage = 10 + .5 * strength + .2 * agility
    elif class_id == "ash_weaver":
        basic_damage = 20 + .35 * energy + .2 * agility
    elif class_id == "wild_scout":
        basic_damage = 15 + .35 * agility + .2 * strength
    else:
        basic_damage = 10 + .4 * strength + .4 * energy + .1 * agility
    max_health = 100 + 1.5 * (level - 1) + 2 * vitality
    max_mana = 60 + (level - 1) + 1.5 * energy
    cooldown_reduction = min(.35, agility * .0004)
    basic_cooldown = 1.15 * (1 - cooldown_reduction)

    starting_damage = []
    for candidate_id, class_info in CLASSES.items():
        base = class_info["base_attributes"]
        if candidate_id == "guardian":
            starting_damage.append(10 + .5 * base["strength"] + .2 * base["agility"])
        elif candidate_id == "ash_weaver":
            starting_damage.append(20 + .35 * base["energy"] + .2 * base["agility"])
        elif candidate_id == "wild_scout":
            starting_damage.append(10 + .35 * base["agility"] + .2 * base["strength"])
        else:
            starting_damage.append(10 + .4 * base["strength"] + .4 * base["energy"] + .1 * base["agility"])
    baseline_enemy_hp = round(sum(starting_damage) / len(starting_damage) * 5)
    phase, wave = arena
    enemy_level = 5 * phase + wave
    enemy_hp = round(baseline_enemy_hp * COMMON_HP_MULTIPLIER * (1 + .06 * max(0, enemy_level - 6)))
    enemy_damage = 12 + .65 * enemy_level
    return {
        "basic_damage": basic_damage,
        "max_health": max_health,
        "max_mana": max_mana,
        "basic_cooldown": basic_cooldown,
        "enemy_level": enemy_level,
        "enemy_hp": enemy_hp,
        "enemy_damage": enemy_damage,
        "hits_to_kill": math.ceil(enemy_hp / basic_damage),
        "basic_only_seconds": max(0, math.ceil(enemy_hp / basic_damage) - 1) * basic_cooldown,
        "hits_to_die": max_health / enemy_damage,
    }


def rotation_time_to_kill(
    class_id: str,
    level: int,
    stats: dict[str, int],
    enemy_hp: float,
) -> dict[str, float]:
    """Simulate separate basic/skill cooldowns and finite starting mana."""
    basic = first_pass_model(class_id, level, stats, (1, 1))
    skill = CANDIDATE_SKILLS[class_id]
    cdr = min(.35, max(0, stats["agility"]) * .0004)
    basic_cd = 1.15 * (1 - cdr)
    skill_cd = skill["cooldown"] * (1 - cdr)
    skill_damage = basic["basic_damage"] * skill["multiplier"]
    mana = basic["max_mana"]
    time = 0.0
    next_basic = 0.0
    next_skill = 0.0
    total_skill_casts = 0
    damage = 0.0
    # No mana regeneration is assumed; this intentionally isolates the
    # starting pool and prevents inventing an unapproved recovery mechanic.
    while damage < enemy_hp and time < 1800:
        time = min(next_basic, next_skill if mana >= skill["mana"] else float("inf"))
        did_action = False
        if next_skill <= time + 1e-9 and mana >= skill["mana"]:
            damage += skill_damage
            mana -= skill["mana"]
            total_skill_casts += 1
            next_skill += skill_cd
            did_action = True
        if next_basic <= time + 1e-9:
            damage += basic["basic_damage"]
            next_basic += basic_cd
            did_action = True
        if not did_action:
            break
    return {"seconds": time, "skill_casts": total_skill_casts, "remaining_mana": mana}


def simulate_candidate_effects(
    class_id: str,
    level: int,
    stats: dict[str, int],
    enemy_hp: float,
    target_count: int = 1,
    boss_phase: int | None = None,
    area_targets: int | None = None,
) -> dict[str, float]:
    """Simulate area caps, resistance and expected DoT ticks.

    ``area_targets`` represents enemies caught by the skill. It makes
    positioning explicit without inventing hit chances or player movement.
    """
    basic = first_pass_model(class_id, level, stats, (1, 1))
    skill = CANDIDATE_SKILLS[class_id]
    cdr = min(.35, max(0, stats["agility"]) * .0004)
    basic_cd = 1.15 * (1 - cdr)
    skill_cd = skill["cooldown"] * (1 - cdr)
    skill_damage = basic["basic_damage"] * skill["multiplier"]
    affinity = boss_affinity(boss_phase) if boss_phase else None
    resistance = PROTOTYPE_BOSS_RESISTANCE if affinity and skill["element"].lower() == affinity["name"].lower() else 0.0
    enemies = [{"hp": float(enemy_hp), "dot_next": float("inf"), "dot_end": 0.0} for _ in range(target_count)]
    mana = basic["max_mana"]
    now = next_basic = next_skill = 0.0
    casts = 0

    while any(enemy["hp"] > 0 for enemy in enemies) and now < 1800:
        next_dot = min((enemy["dot_next"] for enemy in enemies if enemy["hp"] > 0), default=float("inf"))
        next_action = min(next_basic, next_skill if mana >= skill["mana"] else float("inf"))
        now = min(next_dot, next_action)
        if now == float("inf"):
            break

        # Expected DoT ticks model proc chance as fractional average damage.
        due_dots = [enemy for enemy in enemies if enemy["hp"] > 0 and enemy["dot_next"] <= now + 1e-9]
        if due_dots and next_dot <= next_action + 1e-9:
            for enemy in due_dots:
                enemy["hp"] = max(0.0, enemy["hp"] - skill_damage * skill["dot_rate"] * skill["chance"] * (1 - resistance))
                enemy["dot_next"] = now + 1.0 if now + 1.0 <= enemy["dot_end"] + 1e-9 else float("inf")
            continue

        if next_skill <= now + 1e-9 and mana >= skill["mana"]:
            target_cap = skill["target_limit"] if area_targets is None else min(skill["target_limit"], area_targets)
            targets = [enemy for enemy in enemies if enemy["hp"] > 0][:target_cap]
            for enemy in targets:
                enemy["hp"] = max(0.0, enemy["hp"] - skill_damage * (1 - resistance))
                if skill["dot_rate"] and enemy["hp"] > 0:
                    enemy["dot_end"] = now + skill["duration"]
                    enemy["dot_next"] = now + 1.0
            mana -= skill["mana"]
            casts += 1
            next_skill += skill_cd
        elif next_basic <= now + 1e-9:
            target = next((enemy for enemy in enemies if enemy["hp"] > 0), None)
            if target:
                target["hp"] = max(0.0, target["hp"] - basic["basic_damage"])
            next_basic += basic_cd

    return {"seconds": now, "skill_casts": casts, "remaining_mana": mana, "resistance": resistance}


def simulate_party_boss(
    class_ids: tuple[str, ...], level: int, boss_hp: float, boss_phase: int
) -> dict[str, float]:
    """Simulate party damage against one boss without inventing utility value.

    This intentionally excludes utility effects, healing, defensive synergies,
    targeting mistakes, equipment and player deaths. It is only a damage
    baseline for comparing party composition.
    """
    affinity = boss_affinity(boss_phase)
    players = []
    for class_id in class_ids:
        stats = candidate_auto_allocation_at_level(class_id, level)
        basic = first_pass_model(class_id, level, stats, (1, 1))
        skill = CANDIDATE_SKILLS[class_id]
        resistance = PROTOTYPE_BOSS_RESISTANCE if skill["element"].lower() == affinity["name"].lower() else 0.0
        cdr = min(.35, max(0, stats["agility"]) * .0004)
        players.append({
            "basic_damage": basic["basic_damage"], "basic_cd": 1.15 * (1 - cdr),
            "skill": skill, "skill_damage": basic["basic_damage"] * skill["multiplier"],
            "skill_cd": skill["cooldown"] * (1 - cdr), "mana": basic["max_mana"],
            "resistance": resistance, "next_basic": 0.0, "next_skill": 0.0,
            "dot_next": float("inf"), "dot_end": 0.0,
        })

    now = damage = 0.0
    while damage < boss_hp and now < 1800:
        next_action = min(
            min(player["next_basic"], player["next_skill"] if player["mana"] >= player["skill"]["mana"] else float("inf"))
            for player in players
        )
        next_dot = min(player["dot_next"] for player in players)
        now = min(next_action, next_dot)
        if now == float("inf"):
            break

        for player in players:
            skill = player["skill"]
            if player["dot_next"] <= now + 1e-9:
                damage += player["skill_damage"] * skill["dot_rate"] * skill["chance"] * (1 - player["resistance"])
                player["dot_next"] = now + 1.0 if now + 1.0 <= player["dot_end"] + 1e-9 else float("inf")
            if player["next_skill"] <= now + 1e-9 and player["mana"] >= skill["mana"]:
                damage += player["skill_damage"] * (1 - player["resistance"])
                player["mana"] -= skill["mana"]
                player["next_skill"] += player["skill_cd"]
                if skill["dot_rate"]:
                    player["dot_end"] = now + skill["duration"]
                    player["dot_next"] = min(player["dot_next"], now + 1.0)
            if player["next_basic"] <= now + 1e-9:
                damage += player["basic_damage"]
                player["next_basic"] += player["basic_cd"]

    return {"seconds": now, "damage": damage}


def simulate_party_common(
    class_ids: tuple[str, ...], level: int, enemy_hp: float, enemy_count: int = 1,
    player_start_time: float = 0.0,
) -> dict[str, float]:
    """Simulate a party clearing a wave with simultaneous attacks and AoE caps."""
    players = []
    for class_id in class_ids:
        stats = candidate_auto_allocation_at_level(class_id, level)
        basic = first_pass_model(class_id, level, stats, (1, 1))
        skill = CANDIDATE_SKILLS[class_id]
        cdr = min(.35, max(0, stats["agility"]) * .0004)
        players.append({
            "basic": basic["basic_damage"], "basic_cd": 1.15 * (1 - cdr),
            "skill": skill, "skill_damage": basic["basic_damage"] * skill["multiplier"],
            "skill_cd": skill["cooldown"] * (1 - cdr), "mana": basic["max_mana"],
            "dot_next": float("inf"), "dot_end": 0.0,
            "next_basic": player_start_time, "next_skill": player_start_time,
        })
    enemies = [{"hp": float(enemy_hp), "dot_next": float("inf"), "dot_end": 0.0, "dot_damage": 0.0, "death_time": None} for _ in range(enemy_count)]
    now = 0.0
    while any(enemy["hp"] > 0 for enemy in enemies) and now < 1800:
        next_action = min(
            min(p["next_basic"], p["next_skill"] if p["mana"] >= p["skill"]["mana"] else float("inf"))
            for p in players
        )
        next_dot = min((enemy["dot_next"] for enemy in enemies if enemy["hp"] > 0), default=float("inf"))
        now = min(next_action, next_dot)
        if now == float("inf"):
            break
        # Apply every event due at this timestamp before checking for victory.
        for enemy in enemies:
            if enemy["hp"] > 0 and enemy["dot_next"] <= now + 1e-9:
                enemy["hp"] -= enemy["dot_damage"]
                enemy["dot_next"] = now + 1 if now + 1 <= enemy["dot_end"] + 1e-9 else float("inf")
        for p in players:
            skill = p["skill"]
            if p["next_skill"] <= now + 1e-9 and p["mana"] >= skill["mana"]:
                targets = [enemy for enemy in enemies if enemy["hp"] > 0][:skill["target_limit"]]
                for enemy in targets:
                    enemy["hp"] -= p["skill_damage"]
                    if skill["dot_rate"] and enemy["hp"] > 0:
                        enemy["dot_end"] = now + skill["duration"]
                        enemy["dot_damage"] = p["skill_damage"] * skill["dot_rate"] * skill["chance"]
                        enemy["dot_next"] = min(enemy["dot_next"], now + 1)
                p["mana"] -= skill["mana"]
                p["next_skill"] += p["skill_cd"]
            if p["next_basic"] <= now + 1e-9:
                target = next((enemy for enemy in enemies if enemy["hp"] > 0), None)
                if target:
                    target["hp"] -= p["basic"]
                p["next_basic"] += p["basic_cd"]
        for enemy in enemies:
            if enemy["hp"] <= 0 and enemy["death_time"] is None:
                enemy["death_time"] = now
    return {
        "seconds": now,
        "damage": sum(max(0, enemy_hp - enemy["hp"]) for enemy in enemies),
        "kill_times": tuple(
            enemy["death_time"] if enemy["death_time"] is not None else now
            for enemy in enemies
        ),
    }


def horde_approach_times(phase: int, wave: int, enemy_count: int) -> tuple[float, tuple[float, ...]]:
    """Estimate first combat/attack times from seeded positions and current client movement speeds."""
    positions = enemy_spawn_positions(f"simulation:{phase}:{wave}", enemy_count)
    attack_starts = []
    player_access = []
    for index, (x, y) in enumerate(positions):
        distance = math.hypot(x - 1200, y - 900)
        ranged = index % 2 == 1
        attack_range = 390 if ranged else 150
        chase_speed = 54 if ranged else 62 + (index % 3) * 8
        attack = ENEMY_ATTACKS["ranged_shadow_bolt" if ranged else "melee_slam"]
        enemy_arrival = max(0.0, distance - attack_range) / chase_speed
        initial_delay = .85 + (index % 3) * .36
        attack_starts.append(enemy_arrival + initial_delay + attack["windup_ms"] / 1000)
        player_access.append(max(0.0, distance - 150) / chase_speed)
    return (min(player_access, default=0.0), tuple(attack_starts))


def estimate_party_survival(
    class_ids: tuple[str, ...], level: int, arena: tuple[int, int],
    enemy_count: int, clear_seconds: float, hit_rate: float,
    kill_times: tuple[float, ...] | None = None,
    attack_start_times: tuple[float, ...] | None = None,
    enemy_damage_scale: float = 1.0,
) -> dict[str, float]:
    """Estimate pressure after approach, only while each enemy remains alive."""
    players = []
    for class_id in class_ids:
        stats = candidate_auto_allocation_at_level(class_id, level)
        players.append(derived_combat_stats({"class_id": class_id, "level": level, **stats})["max_health"])
    damage_per_player = [0.0] * len(players)
    hits = 0
    for index in range(enemy_count):
        attack = ENEMY_ATTACKS["melee_slam" if index % 2 == 0 else "ranged_shadow_bolt"]
        first_hit = (
            attack_start_times[index]
            if attack_start_times and index < len(attack_start_times)
            else attack["windup_ms"] / 1000
        )
        alive_until = kill_times[index] if kill_times and index < len(kill_times) else clear_seconds
        attack_count = max(0, 1 + math.floor((alive_until - first_hit) / attack["cooldown"])) if alive_until >= first_hit else 0
        for attack_index in range(attack_count):
            target = (index + attack_index) % len(players)
            damage_per_player[target] += attack["damage"] * hit_rate * enemy_damage_scale
            hits += 1
    remaining = [hp - damage for hp, damage in zip(players, damage_per_player)]
    return {"lowest_hp": min(remaining), "hits": hits, "party_hp_remaining": sum(remaining)}


def elite_health_multiplier(target: str, level: int) -> float:
    """Scale elite durability gently through the level-400 cycle."""
    base = MINIBOSS_HP_MULTIPLIER if target == "Semichefe" else BOSS_HP_MULTIPLIER
    cycle_progress = min(1.0, max(0.0, (level - 1) / (MAX_LEVEL - 1)))
    return base * (0.75 + 0.25 * cycle_progress)


def main() -> None:
    arenas = checkpoint_arenas()
    entry_levels = wave_entry_levels()
    print("Candidate reference formulas with current auto-allocation weights")
    print("Class,Level,STR,AGI,VIT,ENE,Damage range,Max HP,Max MP,Defense,Speed index")
    for class_id, class_info in CLASSES.items():
        for level in CHECKPOINTS:
            stats = auto_build_at_level(class_id, level)
            result = reference_outputs(class_id, level, stats)
            print(
                f"{class_info['name']},{level},"
                f"{stats['strength']},{stats['agility']},{stats['vitality']},{stats['energy']},"
                f"{result['damage']},{result['health']:.1f},{result['mana']:.1f},"
                f"{result['defense']:.1f},{result['speed_index']:.1f}"
            )
    print("\nFirst-pass gear-free proposal (basic attack only; all values provisional)")
    print("Class,Level,Basic damage,Max HP,Max MP,Basic CD,Enemy level,Enemy HP,Enemy hit,Hits to kill,TTK seconds,Hits survived")
    for class_id, class_info in CLASSES.items():
        for level in CHECKPOINTS:
            stats = auto_build_at_level(class_id, level)
            result = first_pass_model(class_id, level, stats, arenas[level])
            print(
                f"{class_info['name']},{level},{result['basic_damage']:.1f},"
                f"{result['max_health']:.1f},{result['max_mana']:.1f},"
                f"{result['basic_cooldown']:.2f},{result['enemy_level']},"
                f"{result['enemy_hp']},{result['enemy_damage']:.1f},"
                f"{result['hits_to_kill']:.1f},{result['basic_only_seconds']:.1f},"
                f"{result['hits_to_die']:.1f}"
            )
    print("\nAllocation comparison (same provisional formula; no gear or skills)")
    print("Class,Level,Distribution,STR,AGI,VIT,ENE,TTK seconds,Hits survived")
    for class_id, class_info in CLASSES.items():
        for level in CHECKPOINTS:
            for build_name, build_fn in (
                ("Automática atual", auto_build_at_level),
                ("Automática candidata", candidate_auto_allocation_at_level),
                ("Manual de referência", representative_manual_build),
            ):
                stats = build_fn(class_id, level)
                result = first_pass_model(class_id, level, stats, arenas[level])
                print(
                    f"{class_info['name']},{level},{build_name},"
                    f"{stats['strength']},{stats['agility']},{stats['vitality']},{stats['energy']},"
                    f"{result['basic_only_seconds']:.1f},{result['hits_to_die']:.1f}"
                )
    print("\nCandidate skill rotations (finite starting mana; no gear, regen, status or elemental modifiers)")
    print("Class,Level,Distribution,Target,Skill,Skill damage,Mana cost,Skill CD,Target HP,TTK,Skill casts,Mana left")
    for class_id, class_info in CLASSES.items():
        skill = CANDIDATE_SKILLS[class_id]
        for level in CHECKPOINTS:
            for build_name, build_fn in (
                ("Automática atual", auto_build_at_level),
                ("Automática candidata", candidate_auto_allocation_at_level),
                ("Manual de referência", representative_manual_build),
            ):
                stats = build_fn(class_id, level)
                common = first_pass_model(class_id, level, stats, arenas[level])
                for target in ("Comum", "Semichefe", "Chefe"):
                    multiplier = 1.0 if target == "Comum" else elite_health_multiplier(target, level)
                    target_hp = common["enemy_hp"] * multiplier
                    result = rotation_time_to_kill(class_id, level, stats, target_hp)
                    print(
                        f"{class_info['name']},{level},{build_name},{target},{skill['name']},"
                        f"{common['basic_damage'] * skill['multiplier']:.1f},{skill['mana']},"
                        f"{skill['cooldown']:.1f},{target_hp:.0f},{result['seconds']:.1f},"
                        f"{result['skill_casts']},{result['remaining_mana']:.1f}"
                    )
    print("\nCandidate skill profiles (design inputs, not active gameplay)")
    print("Class,Skill,Target,Element,Area,Status,Chance,Duration,Effect,Expected DoT per hit")
    for class_id, class_info in CLASSES.items():
        skill = CANDIDATE_SKILLS[class_id]
        print(
            f"{class_info['name']},{skill['name']},{skill['target']},{skill['element']},"
            f"{skill['area']},{skill['status']},{skill['chance']:.0%},"
            f"{skill['duration']:.1f}s,{skill['status_value']},"
            f"{skill['dot_rate'] * skill['duration'] * skill['chance']:.1%} expected DoT"
        )
    print("\nThird-pass effects simulation (candidate auto distribution; AoE assumes ideal alignment)")
    print("Class,Level,Three common enemies clear s,Boss TTK range across four affinities s")
    for class_id, class_info in CLASSES.items():
        for level in CHECKPOINTS:
            stats = candidate_auto_allocation_at_level(class_id, level)
            common = first_pass_model(class_id, level, stats, arenas[level])
            group = simulate_candidate_effects(class_id, level, stats, common["enemy_hp"], target_count=3)
            boss_hp = common["enemy_hp"] * elite_health_multiplier("Chefe", level)
            affinity_times = [
                simulate_candidate_effects(class_id, level, stats, boss_hp, boss_phase=phase)["seconds"]
                for phase in range(1, 5)
            ]
            print(
                f"{class_info['name']},{level},{group['seconds']:.1f},"
                f"{min(affinity_times):.1f}-{max(affinity_times):.1f}"
            )
    print("\nArea-positioning scenarios (three common enemies; candidate auto distribution)")
    print("Class,Level,One target caught s,Two targets caught s,Three targets caught s")
    for class_id, class_info in CLASSES.items():
        for level in CHECKPOINTS:
            stats = candidate_auto_allocation_at_level(class_id, level)
            common = first_pass_model(class_id, level, stats, arenas[level])
            scenarios = [
                simulate_candidate_effects(
                    class_id, level, stats, common["enemy_hp"], target_count=3, area_targets=caught
                )["seconds"]
                for caught in (1, 2, 3)
            ]
            print(f"{class_info['name']},{level},{scenarios[0]:.1f},{scenarios[1]:.1f},{scenarios[2]:.1f}")
    print("\nParty boss TTK with candidate cooperative boss-health scaling")
    print("Party,Level,Players,Boss HP multiplier,Boss TTK range across four affinities s")
    parties = (
        ("guardian", "ash_weaver"),
        ("guardian", "ash_weaver", "wild_scout"),
        ("guardian", "wild_scout", "rune_blade"),
    )
    for party in parties:
        party_name = " + ".join(CLASSES[class_id]["name"] for class_id in party)
        for level in CHECKPOINTS:
            stats = candidate_auto_allocation_at_level(party[0], level)
            common = first_pass_model(party[0], level, stats, arenas[level])
            boss_hp = common["enemy_hp"] * elite_health_multiplier("Chefe", level)
            health_multiplier = COOP_BOSS_HEALTH_MULTIPLIER[len(party)]
            times = [
                simulate_party_boss(party, level, boss_hp * health_multiplier, phase)["seconds"]
                for phase in range(1, 5)
            ]
            print(f"{party_name},{level},{len(party)},{health_multiplier:.1f}x,{min(times):.1f}-{max(times):.1f}")
    print("\nFocused common-enemy TTK with candidate cooperative HP scaling")
    print("Party,Level,Players,Common HP multiplier,TTK s")
    for party in parties:
        party_name = " + ".join(CLASSES[class_id]["name"] for class_id in party)
        for level in CHECKPOINTS:
            stats = candidate_auto_allocation_at_level(party[0], level)
            common_hp = first_pass_model(party[0], level, stats, arenas[level])["enemy_hp"]
            hp_multiplier = COOP_COMMON_HEALTH_MULTIPLIER[len(party)]
            result = simulate_party_common(party, level, common_hp * hp_multiplier)
            print(f"{party_name},{level},{len(party)},{hp_multiplier:.2f}x,{result['seconds']:.1f}")
    print("Wave common-enemy count scenarios (focus fire, sequential targets)")
    print("Party,Level,Common enemies,Per-enemy HP,Estimated wave clear s")
    for party in (("guardian",), ("guardian", "ash_weaver"), ("guardian", "ash_weaver", "wild_scout")):
        party_name = " + ".join(CLASSES[class_id]["name"] for class_id in party)
        for level in CHECKPOINTS:
            stats = candidate_auto_allocation_at_level(party[0], level)
            common_hp = first_pass_model(party[0], level, stats, arenas[level])["enemy_hp"]
            count = COOP_COMMON_COUNT[len(party)]
            result = simulate_party_common(party, level, common_hp, enemy_count=count)
            print(f"{party_name},{level},{count},{common_hp},{result['seconds']:.1f}")
    print("Wave survival with random-spawn approach, live attack ranges/windups, and dodge scenarios")
    print("Party,Checkpoint,Phase,Wave,Entry level,Enemies,Clear seconds,Scenario,Potential hits,Lowest remaining HP")
    for party in (("guardian",), ("guardian", "ash_weaver"), ("guardian", "ash_weaver", "wild_scout")):
        party_name = " + ".join(CLASSES[class_id]["name"] for class_id in party)
        for checkpoint in CHECKPOINTS:
            phase = arenas[checkpoint][0]
            for wave_number in (1, 4, 8):
                level = entry_levels.get((phase, wave_number), checkpoint)
                count = enemies_in_wave(wave_number, phase)
                common_hp = enemy_max_health(phase, wave_number)
                player_start, attack_starts = horde_approach_times(
                    phase, wave_number, count
                )
                wave = simulate_party_common(
                    party, level, common_hp, enemy_count=count,
                    player_start_time=player_start,
                )
                clear = wave["seconds"]
                for scenario, hit_rate in (("Sem esquiva", 1.0), ("50% esquiva", .5), ("80% esquiva", .2), ("90% esquiva", .1)):
                    pressure = estimate_party_survival(
                        party, level, (phase, wave_number), count, clear, hit_rate,
                        wave["kill_times"], attack_starts,
                    )
                    print(f"{party_name},{checkpoint},{phase},{wave_number},{level},{count},{clear:.1f},{scenario},{pressure['hits']},{pressure['lowest_hp']:.1f}")
    print("Candidate common-wave correction only (simulation; not applied to gameplay)")
    print("Class,Checkpoint,Phase,Wave,Entry level,Enemies,HP scale,Attack scale,Clear seconds,HP at 50% hits,HP at 80% hits")
    for checkpoint in CHECKPOINTS:
        phase = arenas[checkpoint][0]
        for wave_number in (4, 8):
            level = entry_levels.get((phase, wave_number), checkpoint)
            count = enemies_in_wave(wave_number, phase)
            player_start, attack_starts = horde_approach_times(phase, wave_number, count)
            candidate_hp = enemy_max_health(phase, wave_number) * CANDIDATE_COMMON_HP_SCALE
            for class_id, class_info in CLASSES.items():
                wave = simulate_party_common(
                    (class_id,), level, candidate_hp, enemy_count=count,
                    player_start_time=player_start,
                )
                remaining = []
                for hit_rate in (0.5, 0.2):
                    pressure = estimate_party_survival(
                        (class_id,), level, (phase, wave_number), count,
                        wave["seconds"], hit_rate, wave["kill_times"],
                        attack_starts, CANDIDATE_COMMON_ATTACK_SCALE,
                    )
                    remaining.append(pressure["lowest_hp"])
                print(
                    f"{class_info['name']},{checkpoint},{phase},{wave_number},{level},{count},"
                    f"{CANDIDATE_COMMON_HP_SCALE:.2f},{CANDIDATE_COMMON_ATTACK_SCALE:.2f},"
                    f"{wave['seconds']:.1f},{remaining[0]:.1f},{remaining[1]:.1f}"
                )
    phases, kills = current_xp_projection()
    print(f"Current XP curve reaches level 400 in phase {phases}, after {kills} monster kills.")


if __name__ == "__main__":
    main()
