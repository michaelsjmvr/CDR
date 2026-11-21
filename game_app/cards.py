"""Catálogo de cartas temporárias e escolha ponderada de ofertas."""

from __future__ import annotations

import random

from .abilities import SPECIALIZATION_ABILITIES, active_class_skill


RARITY_WEIGHTS = {
    "common": 50,
    "uncommon": 25,
    "rare": 14,
    "excellent": 7,
    "epic": 3,
    "legendary": 1,
}

RARITIES = {
    "common": {"name": "Comum", "color": "#475569"},
    "uncommon": {"name": "Incomum / Mágico", "color": "#10B981"},
    "rare": {"name": "Raro", "color": "#38BDF8"},
    "excellent": {"name": "Excelente", "color": "#F59E0B"},
    "epic": {"name": "Épico / Ancestral", "color": "#A855F7"},
    "legendary": {"name": "Lendário / Mítico", "color": "#F43F5E"},
}
RARITY_RANK = {
    rarity: rank
    for rank, rarity in enumerate(("common", "uncommon", "rare", "excellent", "epic", "legendary"))
}

# Passivas temporárias aplicadas pelo servidor durante o combate.
CARD_CATALOG = (
    ("ember_edge", "Fio de Brasa", "common", "Ataque", "+5% de dano causado."),
    ("steady_guard", "Guarda Constante", "common", "Defesa", "Reduz em 5% o dano recebido."),
    ("stone_lungs", "Pulmões de Pedra", "common", "Vitalidade", "+6% de vida máxima."),
    ("light_foot", "Passo Leve", "common", "Mobilidade", "+5% de velocidade de movimento."),
    ("clear_mind", "Mente Serena", "common", "Energia", "+5% de poder mágico."),
    ("keen_aim", "Mira Firme", "common", "Precisão", "+5% de chance de acerto crítico."),
    ("quick_breath", "Fôlego Rápido", "common", "Recarga", "-4% no tempo de recarga."),
    ("iron_skin", "Pele de Ferro", "common", "Resistência", "Reduz em 4% o dano recebido."),
    ("warmash", "Cinza Revigorante", "common", "Recuperação", "Recupera 3% da Vida máxima ao concluir uma onda."),
    ("long_reach", "Alcance Alongado", "common", "Alcance", "Aumenta em 5% o alcance dos ataques."),
    ("sure_step", "Passo Seguro", "common", "Esquiva", "+3% de chance de esquiva."),
    ("battle_focus", "Foco de Batalha", "common", "Concentração", "+4% de dano contra inimigos comuns."),
    ("rune_spark", "Centelha Rúnica", "uncommon", "Magia", "+8% de dano mágico."),
    ("guardian_pulse", "Pulso Guardião", "uncommon", "Defesa", "Reduz em 3% o dano recebido."),
    ("hunter_mark", "Marca do Caçador", "uncommon", "Ataque", "+8% de dano causado."),
    ("blood_echo", "Eco Vital", "uncommon", "Recuperação", "Acertos críticos recuperam 3% da Vida máxima."),
    ("twin_flame", "Chama Gêmea", "uncommon", "Magia", "+5% de dano com habilidades."),
    ("swift_recovery", "Recuperação Veloz", "uncommon", "Recarga", "Uma eliminação reduz em 0,75 s a recarga da habilidade usada."),
    ("arcane_shell", "Casca Arcana", "uncommon", "Defesa mágica", "Reduz em 8% o dano de ataques à distância."),
    ("rune_burst", "Explosão de Runas", "rare", "Explosão", "Habilidades têm 20% de chance de causar 50% de dano adicional."),
    ("last_stand", "Última Resistência", "rare", "Sobrevivência", "Abaixo de 30% de Vida, reduz em 15% o dano recebido."),
    ("storm_draw", "Tração da Tempestade", "rare", "Ataque", "Ataques em sequência aumentam o dano em até 10%."),
    ("piercing_volley", "Saraivada Perfurante", "rare", "Magia", "+10% de dano com habilidades."),
    ("vital_siphon", "Sifão Vital", "rare", "Recuperação", "Recupera Vida igual a 5% do dano causado."),
    ("mirror_ward", "Proteção Espelhada", "rare", "Defesa", "Devolve ao atacante 10% do dano recebido."),
    ("ember_rebirth", "Renascimento das Brasas", "excellent", "Ressurgimento", "Recupera 15% da Vida máxima ao concluir uma onda."),
    ("void_anchor", "Âncora do Vazio", "excellent", "Defesa", "Reduz em 4% o dano recebido."),
    ("war_chorus", "Coro de Guerra", "excellent", "Aprimoramento", "+10% de dano contra semichefes e chefes e 4% de redução de dano recebido."),
    ("ashen_phoenix", "Fênix de Cinzas", "epic", "Magia", "+12% de dano com habilidades."),
    ("worldbreaker", "Rompemundos", "epic", "Chefe", "+15% de dano contra semichefes e chefes."),
    ("umbral_crown", "Coroa do Umbral", "legendary", "Poder", "+5% de dano causado e +3% de Vida máxima."),
    ("endless_oath", "Juramento Infindável", "legendary", "Energia", "+8% de Mana máxima."),
    ("piercing_spark", "Faísca Perfurante", "rare", "Projétil", "Projéteis causam 8% mais dano ao atingir."),
    ("elemental_conduit", "Conduto Elemental", "rare", "Elemento", "Habilidades elementais causam 8% mais dano."),
    ("mana_harvest", "Colheita de Mana", "uncommon", "Energia", "Abates restauram 5% da Mana máxima."),
    ("healing_resonance", "Ressonância Restauradora", "excellent", "Recuperação", "Habilidades restauram 20% mais Vida."),
)

CARDS = {
    card_id: {
        "id": card_id,
        "name": name,
        "rarity_key": rarity,
        "rarity": RARITIES[rarity]["name"],
        "color": RARITIES[rarity]["color"],
        "category": category,
        "description": description,
    }
    for card_id, name, rarity, category, description in CARD_CATALOG
}

# Cada chave abaixo é consumida por uma fórmula/evento de combate ativo.
# Os valores são provisórios e só duram enquanto a carta estiver ativa.
CARD_EFFECTS = {
    "ember_edge": {"damage": .05},
    "steady_guard": {"damage_reduction": .05},
    "stone_lungs": {"max_health": .06},
    "light_foot": {"move_speed": .05},
    "clear_mind": {"skill_damage": .05},
    "keen_aim": {"critical_chance": .05},
    "quick_breath": {"cooldown_reduction": .04},
    "iron_skin": {"damage_reduction": .04},
    "warmash": {"wave_heal": .03},
    "long_reach": {"attack_range": .05},
    "sure_step": {"dodge_chance": .03},
    "battle_focus": {"common_damage": .04},
    "rune_spark": {"skill_damage": .08},
    "guardian_pulse": {"damage_reduction": .03},
    "hunter_mark": {"damage": .08},
    "blood_echo": {"critical_heal": .03},
    "twin_flame": {"skill_damage": .05},
    "swift_recovery": {"cooldown_refund_on_kill": .75},
    "arcane_shell": {"ranged_reduction": .08},
    "rune_burst": {"skill_burst_chance": .20, "skill_burst_damage": .50},
    "last_stand": {"low_health_reduction": .15},
    "storm_draw": {"attack_streak_damage": .02, "attack_streak_cap": 5},
    "piercing_volley": {"skill_damage": .10},
    "vital_siphon": {"life_steal": .05},
    "mirror_ward": {"damage_reflection": .10},
    "ember_rebirth": {"wave_heal": .15},
    "void_anchor": {"damage_reduction": .04},
    "war_chorus": {"boss_damage": .10, "damage_reduction": .04},
    "ashen_phoenix": {"skill_damage": .12},
    "worldbreaker": {"boss_damage": .15},
    "umbral_crown": {"damage": .05, "max_health": .03},
    "endless_oath": {"max_mana": .08},
    "piercing_spark": {"projectile_damage": .08},
    "elemental_conduit": {"elemental_damage": .08},
    "mana_harvest": {"mana_on_kill": .05},
    "healing_resonance": {"skill_healing": .20},
}


_CLASS_CARD_WEIGHTS = {
    "guardian": {
        "damage": 1.05, "skill_damage": .75, "damage_reduction": 1.7,
        "max_health": 1.65, "dodge_chance": 1.35, "wave_heal": 1.4,
        "low_health_reduction": 1.75, "boss_damage": 1.0,
        "damage_reflection": 1.6,
        "projectile_damage": .45, "elemental_damage": .45,
        "mana_on_kill": 1.0, "skill_healing": .85,
    },
    "ash_weaver": {
        "damage": .75, "skill_damage": 1.8, "skill_burst_chance": 1.55,
        "max_mana": 1.5, "cooldown_reduction": 1.35, "damage_reduction": 1.0,
        "max_health": 1.0, "boss_damage": 1.0, "life_steal": 1.2,
        "projectile_damage": 1.35, "elemental_damage": 1.55,
        "mana_on_kill": 1.0, "skill_healing": 1.2,
    },
    "wild_scout": {
        "damage": 1.2, "critical_chance": 1.75, "attack_range": 1.5,
        "move_speed": 1.35, "attack_streak_damage": 1.65,
        "skill_damage": 1.0, "dodge_chance": 1.25, "boss_damage": 1.0,
        "life_steal": 1.2,
        "projectile_damage": 1.7, "elemental_damage": .8,
        "mana_on_kill": .85, "skill_healing": .7,
    },
    "rune_blade": {
        "damage": 1.35, "skill_damage": 1.4, "critical_chance": 1.25,
        "damage_reduction": 1.2, "max_health": 1.1, "max_mana": 1.0,
        "cooldown_reduction": 1.2, "boss_damage": 1.0,
        "damage_reflection": 1.1,
        "projectile_damage": .75, "elemental_damage": 1.55,
        "mana_on_kill": .9, "skill_healing": .8,
    },
}

_CARD_SCORE_SCALE = {
    # Normaliza efeitos medidos em segundos ou acúmulos antes da comparação.
    "cooldown_refund_on_kill": .15,
    "attack_streak_damage": 5.0,
    "attack_streak_cap": .02,
    "skill_burst_damage": .25,
}


def card_recommendation_score(card_id: str, class_id: str,
                              health_ratio: float = 1.0, wave: int = 1,
                              specialization_id: str | None = None,
                              purchased_talents=()) -> float:
    """Pontua a carta pela classe, especialização, situação e raridade."""
    weights = dict(_CLASS_CARD_WEIGHTS.get(class_id, _CLASS_CARD_WEIGHTS["guardian"]))
    health_ratio = max(0.0, min(1.0, float(health_ratio)))
    if health_ratio <= .45:
        for stat in ("damage_reduction", "max_health", "dodge_chance", "wave_heal",
                     "low_health_reduction", "ranged_reduction"):
            weights[stat] = weights.get(stat, 1.0) * 1.8
    if wave in (9, 10):
        weights["boss_damage"] = weights.get("boss_damage", 1.0) * 1.5
    effects = CARD_EFFECTS.get(card_id)
    if effects is None:
        return float("-inf")
    specialization = SPECIALIZATION_ABILITIES.get(specialization_id)
    if specialization and specialization["class_id"] != class_id:
        specialization = None
    skill = active_class_skill(class_id, specialization_id, purchased_talents)
    passive_modifiers = (
        specialization["passive"]["modifiers"] if specialization else {}
    )
    effect_score = 0.0
    for stat, value in effects.items():
        build_fit = 1.0
        if stat == "projectile_damage" and skill.get("projectile"):
            build_fit = 1.35
        elif (
            stat == "elemental_damage"
            and skill.get("damage_type") == "magical"
            and skill.get("element")
        ):
            build_fit = 1.35
        elif stat == "skill_healing" and (
            skill.get("heal_damage_fraction")
            or skill.get("heal_max_health_fraction")
        ):
            build_fit = 1.5
        elif stat == "mana_on_kill" and passive_modifiers.get("mana_on_kill"):
            build_fit = 1.25
        effect_score += (
            value * _CARD_SCORE_SCALE.get(stat, 1.0)
            * weights.get(stat, .72) * build_fit
        )
    rarity_rank = RARITY_RANK.get(CARDS.get(card_id, {}).get("rarity_key"), 0)
    # A raridade desempata cartas próximas sem superar um efeito claramente
    # mais útil para a classe e a situação.
    return effect_score * (1 + rarity_rank * .04) + rarity_rank * .001


def recommend_card(card_ids, class_id: str, health_ratio: float = 1.0,
                   wave: int = 1, specialization_id: str | None = None,
                   purchased_talents=()) -> str | None:
    """Escolhe a melhor carta da oferta para a classe e o momento da partida."""
    best_id = None
    best_score = float("-inf")
    for card_id in card_ids:
        score = card_recommendation_score(
            card_id, class_id, health_ratio, wave,
            specialization_id, purchased_talents,
        )
        if score > best_score or (score == best_score and card_id < (best_id or card_id)):
            best_id, best_score = card_id, score
    return best_id


def card_modifiers(card_ids) -> dict[str, float]:
    """Combina cartas ativas sem persistir os modificadores."""
    modifiers: dict[str, float] = {}
    for card_id in card_ids:
        for key, value in CARD_EFFECTS.get(card_id, {}).items():
            modifiers[key] = modifiers.get(key, 0) + value
    modifiers["damage_reduction"] = min(.50, modifiers.get("damage_reduction", 0))
    modifiers["dodge_chance"] = min(.35, modifiers.get("dodge_chance", 0))
    modifiers["critical_chance"] = min(.50, modifiers.get("critical_chance", 0))
    modifiers["skill_burst_chance"] = min(.50, modifiers.get("skill_burst_chance", 0))
    modifiers["attack_streak_cap"] = min(5, int(modifiers.get("attack_streak_cap", 0)))
    return modifiers


def draw_card_offer(
    active_card_ids: set[str],
    amount: int = 3,
    excluded_card_ids: set[str] | None = None,
) -> list[str]:
    """Sorteia cartas únicas por raridade, evitando ofertas repetidas na onda."""
    excluded = excluded_card_ids or set()
    pool = [
        card for card in CARD_CATALOG
        if card[0] not in active_card_ids and card[0] not in excluded
    ]
    # If a wave has shown nearly the whole inactive catalog, keep offering
    # three distinct options rather than letting the draft fail.
    if len(pool) < amount:
        pool = [card for card in CARD_CATALOG if card[0] not in active_card_ids]
    if len(pool) < amount:
        raise ValueError("The card pool does not contain enough unique choices.")

    rng = random.SystemRandom()
    offered: list[str] = []
    while len(offered) < amount:
        available_rarities = {card[2] for card in pool}
        rarities = [rarity for rarity in RARITY_WEIGHTS if rarity in available_rarities]
        rarity = rng.choices(
            rarities,
            weights=[RARITY_WEIGHTS[item] for item in rarities],
            k=1,
        )[0]
        rarity_pool = [card for card in pool if card[2] == rarity]
        chosen = rng.choice(rarity_pool)
        offered.append(chosen[0])
        pool.remove(chosen)
    return offered
