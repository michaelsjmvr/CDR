"""Simulações determinísticas com as regras reais de combate e progressão."""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from game_app.abilities import CLASS_BASE_SKILLS, active_class_skill
from game_app.classes import CLASSES
from game_app.combat import (
    ENEMY_ATTACKS,
    calculate_attack_damage,
    cooldown_for_agility,
    derived_combat_stats,
    enemy_level,
    enemy_max_health,
    scale_enemy_attack_damage,
)
from game_app.progression import (
    distribute_attribute_points,
    enemies_in_wave,
    legacy_points_for_level,
)
from game_app.talents import CLASS_SPECIALIZATIONS, RADIAL_GRAPHS
from scripts.simulate_balance_model import (
    CHECKPOINTS,
    checkpoint_arenas,
    current_xp_projection,
    horde_approach_times,
    wave_entry_levels,
)

DAMAGE_SPECIALIZATIONS = {
    "guardian": "berserker",
    "ash_weaver": "archmage",
    "wild_scout": "sharpshooter",
    "rune_blade": "spellblade",
}
PROJECTED_LEVEL_CAP_PHASE, _ = current_xp_projection()
BOSS_BENCHMARK_PHASE = ((PROJECTED_LEVEL_CAP_PHASE // 10) + 1) * 10


def automatic_attributes_at_level(class_id: str, level: int) -> dict[str, int]:
    """Calcula os atributos automáticos usando a distribuição de produção."""
    attributes = dict(CLASSES[class_id]["base_attributes"])
    attributes, _, _ = distribute_attribute_points(
        class_id, attributes, max(0, level - 1) * 5
    )
    return attributes


def _expected_damage(
    combat_stats: dict,
    skill: dict | None,
    damage_type: str,
    element: str | None,
    phase: int,
    wave: int,
) -> float:
    """Calcula o dano esperado com as chances reais de crítico e surto."""
    expected = 0.0
    critical_chance = combat_stats["critical_chance"]
    burst_chance = combat_stats["skill_burst_chance"] if skill else 0.0
    for critical in (False, True):
        critical_weight = critical_chance if critical else 1 - critical_chance
        for burst in (False, True):
            burst_weight = burst_chance if burst else 1 - burst_chance
            expected += critical_weight * burst_weight * calculate_attack_damage(
                combat_stats,
                skill,
                damage_type,
                element,
                phase,
                wave,
                critical=critical,
                skill_burst=burst,
            )
    return expected


def _player_state(
    class_id: str,
    level: int,
    specialization_id: str | None,
    purchased_talents: tuple[str, ...],
) -> tuple[dict, dict, dict]:
    """Monta o personagem e obtém os valores reais de combate."""
    attributes = automatic_attributes_at_level(class_id, level)
    character = {
        "class_id": class_id,
        "level": level,
        "specialization_id": specialization_id,
        **attributes,
    }
    stats = derived_combat_stats(character, purchased_talents=purchased_talents)
    skill = active_class_skill(class_id, specialization_id, purchased_talents)
    return attributes, stats, skill


def _attack_values(
    class_id: str,
    attributes: dict[str, int],
    stats: dict,
    skill: dict,
    phase: int,
    wave: int,
) -> tuple[float, float, float, float]:
    """Calcula dano e recargas básicos e da habilidade ativa."""
    base_skill = CLASS_BASE_SKILLS[class_id]
    basic_damage = _expected_damage(
        stats,
        None,
        base_skill["basic_damage_type"],
        base_skill.get("basic_element"),
        phase,
        wave,
    )
    skill_damage = _expected_damage(
        stats,
        skill,
        skill["damage_type"],
        skill.get("element"),
        phase,
        wave,
    )
    basic_cooldown = cooldown_for_agility(
        stats["basic_cooldown"] * stats["cooldown_multiplier"],
        attributes["agility"],
    )
    skill_cooldown = cooldown_for_agility(
        skill["cooldown"] * stats["cooldown_multiplier"],
        attributes["agility"],
    )
    return basic_damage, basic_cooldown, skill_damage, skill_cooldown


def simulate_live_rotation(
    class_id: str,
    level: int,
    phase: int,
    wave: int,
    specialization_id: str | None = None,
    purchased_talents: tuple[str, ...] = (),
) -> dict[str, float]:
    """Estima um abate solo com cadência perfeita e fórmulas do servidor."""
    attributes, stats, skill = _player_state(
        class_id, level, specialization_id, purchased_talents
    )
    basic_damage, basic_cooldown, skill_damage, skill_cooldown = _attack_values(
        class_id, attributes, stats, skill, phase, wave
    )
    enemy_health = enemy_max_health(phase, wave)
    mana = stats["max_mana"]
    now = next_basic = next_skill = total_damage = 0.0
    casts = 0

    while total_damage < enemy_health and now < 1800:
        next_event = min(
            next_basic,
            next_skill if mana >= skill["mana"] else math.inf,
        )
        if next_event == math.inf:
            break
        now = next_event
        if next_skill <= now + 1e-9 and mana >= skill["mana"]:
            total_damage += skill_damage
            mana -= skill["mana"]
            casts += 1
            next_skill += skill_cooldown
        if next_basic <= now + 1e-9:
            total_damage += basic_damage
            next_basic += basic_cooldown

    return {
        "seconds": now,
        "enemy_health": enemy_health,
        "enemy_level": enemy_level(phase, wave),
        "skill_casts": casts,
        "remaining_mana": mana,
    }


def simulate_live_wave(
    class_id: str,
    level: int,
    phase: int,
    wave: int,
    specialization_id: str | None = None,
    purchased_talents: tuple[str, ...] = (),
) -> dict[str, object]:
    """Elimina uma onda em sequência, preservando recargas e Mana entre abates."""
    attributes, stats, skill = _player_state(
        class_id, level, specialization_id, purchased_talents
    )
    basic_damage, basic_cooldown, skill_damage, skill_cooldown = _attack_values(
        class_id, attributes, stats, skill, phase, wave
    )
    enemy_health = enemy_max_health(phase, wave)
    enemies = [float(enemy_health)] * enemies_in_wave(wave, phase)
    mana = stats["max_mana"]
    now = next_basic = next_skill = 0.0
    kill_times: list[float | None] = [None] * len(enemies)
    casts = 0

    while any(hp > 0 for hp in enemies) and now < 1800:
        next_event = min(
            next_basic,
            next_skill if mana >= skill["mana"] else math.inf,
        )
        if next_event == math.inf:
            break
        now = next_event
        if next_skill <= now + 1e-9 and mana >= skill["mana"]:
            target = next((i for i, hp in enumerate(enemies) if hp > 0), None)
            if target is not None:
                enemies[target] -= skill_damage
                if enemies[target] <= 0:
                    kill_times[target] = now
            mana -= skill["mana"]
            casts += 1
            next_skill += skill_cooldown
        if next_basic <= now + 1e-9:
            target = next((i for i, hp in enumerate(enemies) if hp > 0), None)
            if target is not None:
                enemies[target] -= basic_damage
                if enemies[target] <= 0:
                    kill_times[target] = now
            next_basic += basic_cooldown

    return {
        "seconds": now,
        "enemy_count": len(enemies),
        "kill_times": tuple(now if time is None else time for time in kill_times),
        "skill_casts": casts,
        "remaining_mana": mana,
    }


def estimate_live_wave_survival(
    class_id: str,
    level: int,
    phase: int,
    wave: int,
    hit_rate: float = 0.5,
    specialization_id: str | None = None,
) -> dict[str, float]:
    """Estima sobrevivência parado, considerando aproximação, esquiva e dano real."""
    attributes, stats, _ = _player_state(
        class_id, level, specialization_id, ()
    )
    wave_result = simulate_live_wave(
        class_id, level, phase, wave, specialization_id
    )
    enemy_count = int(wave_result["enemy_count"])
    attack_starts = horde_approach_times(phase, wave, enemy_count)[1]
    kill_times = wave_result["kill_times"]
    remaining_health = float(stats["max_health"])
    damage_at_full_hit_rate = 0.0
    hits = 0

    for index, death_time in enumerate(kill_times):
        attack_name = (
            "melee_slam" if index % 2 == 0 else "ranged_shadow_bolt"
        )
        attack = ENEMY_ATTACKS[attack_name]
        first_hit = attack_starts[index]
        attack_count = (
            max(0, 1 + math.floor((death_time - first_hit) / attack["cooldown"]))
            if death_time >= first_hit else 0
        )
        damage = scale_enemy_attack_damage(attack["damage"], phase, wave)
        damage_at_full_hit_rate += attack_count * damage * (
            1 - stats["dodge_chance"]
        )
        expected_hit_rate = hit_rate * (1 - stats["dodge_chance"])
        remaining_health -= attack_count * damage * expected_hit_rate
        hits += attack_count

    return {
        "remaining_health": remaining_health,
        "max_health": float(stats["max_health"]),
        "expected_hits": hits * hit_rate * (1 - stats["dodge_chance"]),
        "enemy_count": float(enemy_count),
        "wave_seconds": float(wave_result["seconds"]),
        "survivable_hit_rate": (
            min(1.0, stats["max_health"] / damage_at_full_hit_rate)
            if damage_at_full_hit_rate else 1.0
        ),
    }


def main() -> None:
    arenas = checkpoint_arenas()
    entries = wave_entry_levels()
    print("Combate em produção; sem equipamentos, cartas ou talentos comprados")
    print("Classe,Marco,Alvo,Fase,Onda,Nível do jogador,Nível inimigo,Vida inimiga,Tempo para derrotar (s)")
    for checkpoint in CHECKPOINTS:
        current_phase, _ = arenas[checkpoint]
        common_wave = 1 if checkpoint == 1 else 8
        miniboss_phase = (current_phase // 10) * 10 + 5
        if miniboss_phase <= current_phase:
            miniboss_phase += 10
        boss_phase = ((current_phase + 9) // 10) * 10
        if boss_phase <= current_phase:
            boss_phase += 10
        target_waves = (
            ("Comum", current_phase, common_wave),
            ("Semichefe", miniboss_phase, 10),
            ("Chefe", boss_phase, 10),
        )
        for class_id, class_info in CLASSES.items():
            for target, phase, wave in target_waves:
                level = (
                    1 if checkpoint == 1 and target == "Comum"
                    else entries[(phase, wave)]
                )
                specialization = (
                    DAMAGE_SPECIALIZATIONS[class_id] if level >= 100 else None
                )
                result = simulate_live_rotation(
                    class_id, level, phase, wave, specialization
                )
                print(
                    f"{class_info['name']},{checkpoint},{target},{phase},{wave},"
                    f"{level},{result['enemy_level']},{result['enemy_health']},"
                    f"{result['seconds']:.1f}"
                )
    print("\nModelo de horda; jogador parado, 50% de acerto antes da esquiva")
    print("Classe,Marco,Fase,Onda,Nível do jogador,Inimigos,Duração (s),Vida restante,Acerto limite para sobreviver")
    for checkpoint in CHECKPOINTS:
        phase, _ = arenas[checkpoint]
        wave = 8
        level = entries[(phase, wave)]
        for class_id, class_info in CLASSES.items():
            specialization = (
                DAMAGE_SPECIALIZATIONS[class_id] if level >= 100 else None
            )
            result = estimate_live_wave_survival(
                class_id, level, phase, wave, specialization_id=specialization
            )
            print(
                f"{class_info['name']},{checkpoint},{phase},{wave},{level},"
                f"{int(result['enemy_count'])},{result['wave_seconds']:.1f},"
                f"{result['remaining_health']:.1f},"
                f"{result['survivable_hit_rate']:.1%}"
            )
    print(
        f"\nBuilds completas; chefe teórico da fase {BOSS_BENCHMARK_PHASE}, "
        "onda 10 (fora da campanha atual), sem cartas/equipamento"
    )
    print("Classe,Especialização,PL gastos,PL nível 400,Nível inimigo,Tempo para derrotar (s)")
    for class_id, specializations in CLASS_SPECIALIZATIONS.items():
        graph = RADIAL_GRAPHS[class_id]
        for specialization in specializations:
            nodes = [
                node for node in graph["nodes"]
                if node.get("specialization_id") == specialization["id"]
                and node["category"] != "starting"
            ]
            purchased_talents = tuple(node["id"] for node in nodes)
            result = simulate_live_rotation(
                class_id, 400, BOSS_BENCHMARK_PHASE, 10,
                specialization["id"], purchased_talents
            )
            points_spent = sum(node["cost"] for node in nodes)
            print(
                f"{CLASSES[class_id]['name']},{specialization['name']},"
                f"{points_spent},{legacy_points_for_level(400)},"
                f"{result['enemy_level']},{result['seconds']:.1f}"
            )


if __name__ == "__main__":
    main()
