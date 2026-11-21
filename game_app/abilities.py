"""Class and specialization abilities used by the talent tree and combat."""

CLASS_BASE_SKILLS = {
    "guardian": {
        "id": "shield_bash",
        "name": "Golpe de Escudo",
        "mana": 18,
        "cooldown": 5.0,
        "damage_multiplier": 1.0,
        "damage_type": "physical",
        "basic_damage_type": "physical",
        "projectile": False,
        "description": "Atinge um inimigo e causa 100% do dano de habilidade.",
    },
    "ash_weaver": {
        "id": "cinder_bolt",
        "name": "Projétil de Cinzas",
        "mana": 20,
        "cooldown": 5.0,
        "damage_multiplier": 1.0,
        "damage_type": "magical",
        "element": "fire",
        "basic_damage_type": "magical",
        "basic_element": "fire",
        "projectile": True,
        "description": "Lança um projétil de Fogo que causa 100% do dano de habilidade ao atingir.",
    },
    "wild_scout": {
        "id": "precision_shot",
        "name": "Tiro Preciso",
        "mana": 16,
        "cooldown": 4.5,
        "damage_multiplier": 1.0,
        "damage_type": "physical",
        "basic_damage_type": "physical",
        "projectile": True,
        "description": "Dispara uma flecha que causa 100% do dano de habilidade ao atingir.",
    },
    "rune_blade": {
        "id": "rune_slash",
        "name": "Corte Rúnico",
        "mana": 25,
        "cooldown": 6.0,
        "damage_multiplier": 1.0,
        "damage_type": "magical",
        "element": "umbral",
        "basic_damage_type": "physical",
        "projectile": False,
        "description": "Atinge um inimigo com energia Umbral e causa 100% do dano de habilidade.",
    },
}

SPECIALIZATION_ABILITIES = {
    "berserker": {
        "class_id": "guardian",
        "passive": {
            "name": "Fúria Crescente",
            "description": "+8% de dano em ataques básicos e habilidades.",
            "modifiers": {"damage": 0.08},
        },
        "skill": {
            "id": "frenzied_cleave",
            "name": "Talho Frenético",
            "mana": 32,
            "cooldown": 7.5,
            "damage_multiplier": 1.35,
            "damage_type": "physical",
            "projectile": False,
            "description": "Atinge um inimigo e causa 135% do dano de habilidade.",
        },
    },
    "guardian_bastion": {
        "class_id": "guardian",
        "passive": {
            "name": "Bastião de Aço",
            "description": "+8% de Vida máxima e +4% de redução de dano.",
            "modifiers": {"max_health": 0.08, "damage_reduction": 0.04},
        },
        "skill": {
            "id": "bastion_impact",
            "name": "Impacto do Bastião",
            "mana": 24,
            "cooldown": 7.0,
            "damage_multiplier": 1.2,
            "damage_type": "physical",
            "projectile": False,
            "description": "Atinge um inimigo e causa 120% do dano de habilidade.",
        },
    },
    "warlord": {
        "class_id": "guardian",
        "passive": {
            "name": "Comando de Batalha",
            "description": "Recargas de habilidades 5% menores; abates restauram 3% da Mana máxima.",
            "modifiers": {"cooldown_reduction": 0.05, "mana_on_kill": 0.03},
        },
        "skill": {
            "id": "commanding_strike",
            "name": "Investida de Comando",
            "mana": 26,
            "cooldown": 7.0,
            "damage_multiplier": 1.2,
            "mana_refund_on_kill_fraction": 0.15,
            "damage_type": "physical",
            "projectile": False,
            "description": "Causa 120% do dano de habilidade; um abate devolve 15% do custo de Mana.",
        },
    },
    "sharpshooter": {
        "class_id": "wild_scout",
        "passive": {
            "name": "Mira Implacável",
            "description": "+6 pontos percentuais de chance crítica e +8% de alcance de ataque.",
            "modifiers": {"critical_chance": 0.06, "attack_range": 0.08},
        },
        "skill": {
            "id": "deadeye_shot",
            "name": "Disparo Perfurante",
            "mana": 28,
            "cooldown": 8.0,
            "damage_multiplier": 1.4,
            "damage_type": "physical",
            "projectile": True,
            "description": "Dispara uma flecha perfurante que causa 140% do dano de habilidade ao atingir.",
        },
    },
    "beast_master": {
        "class_id": "wild_scout",
        "passive": {
            "name": "Instinto de Matilha",
            "description": "+3% de redução de dano; abates restauram 6% da Mana máxima.",
            "modifiers": {"damage_reduction": 0.03, "mana_on_kill": 0.06},
        },
        "skill": {
            "id": "pack_assault",
            "name": "Investida Selvagem",
            "mana": 22,
            "cooldown": 6.5,
            "damage_multiplier": 1.25,
            "damage_type": "physical",
            "projectile": False,
            "description": "Atinge um inimigo e causa 125% do dano de habilidade.",
        },
    },
    "arcane_archer": {
        "class_id": "wild_scout",
        "passive": {
            "name": "Flecha Ressonante",
            "description": "+8% de dano de habilidade e +3 pontos percentuais de chance crítica.",
            "modifiers": {"skill_damage": 0.08, "critical_chance": 0.03},
        },
        "skill": {
            "id": "elemental_arrow",
            "name": "Flecha Elemental",
            "mana": 28,
            "cooldown": 7.5,
            "damage_multiplier": 1.25,
            "damage_type": "magical",
            "element": "lightning",
            "projectile": True,
            "description": "Dispara uma Flecha de Raio que causa 125% do dano de habilidade ao atingir.",
        },
    },
    "archmage": {
        "class_id": "ash_weaver",
        "passive": {
            "name": "Fonte Arcana",
            "description": "+10% de dano de habilidade e +8% de Mana máxima.",
            "modifiers": {"skill_damage": 0.10, "max_mana": 0.08},
        },
        "skill": {
            "id": "ashen_cataclysm",
            "name": "Cataclismo das Cinzas",
            "mana": 38,
            "cooldown": 8.5,
            "damage_multiplier": 1.45,
            "damage_type": "magical",
            "element": "fire",
            "projectile": True,
            "description": "Lança uma explosão de Fogo que causa 145% do dano de habilidade ao atingir.",
        },
    },
    "necromancer": {
        "class_id": "ash_weaver",
        "passive": {
            "name": "Colheita Sombria",
            "description": "+5% de dano de habilidade; abates restauram 7% da Mana máxima.",
            "modifiers": {"skill_damage": 0.05, "mana_on_kill": 0.07},
        },
        "skill": {
            "id": "soul_drain",
            "name": "Dreno de Almas",
            "mana": 26,
            "cooldown": 6.5,
            "damage_multiplier": 1.05,
            "heal_damage_fraction": 0.2,
            "damage_type": "magical",
            "element": "umbral",
            "projectile": False,
            "description": "Causa 105% do dano de habilidade e restaura Vida igual a 20% do dano causado.",
        },
    },
    "sage": {
        "class_id": "ash_weaver",
        "passive": {
            "name": "Equilíbrio Restaurador",
            "description": "+3% de redução de dano e +5% de cura ao avançar de onda.",
            "modifiers": {"damage_reduction": 0.03, "wave_heal": 0.05},
        },
        "skill": {
            "id": "restorative_pulse",
            "name": "Pulso Restaurador",
            "mana": 30,
            "cooldown": 7.0,
            "damage_multiplier": 1.0,
            "heal_max_health_fraction": 0.05,
            "damage_type": "magical",
            "element": "ice",
            "projectile": True,
            "description": "Lança um pulso de Gelo que causa 100% do dano de habilidade e restaura 5% da Vida máxima ao atingir.",
        },
    },
    "spellblade": {
        "class_id": "rune_blade",
        "passive": {
            "name": "Canalização Marcial",
            "description": "+5% de dano em ataques básicos e habilidades.",
            "modifiers": {"damage": 0.05, "skill_damage": 0.05},
        },
        "skill": {
            "id": "arcane_edge",
            "name": "Lâmina Elemental",
            "mana": 28,
            "cooldown": 6.5,
            "damage_multiplier": 1.3,
            "damage_type": "magical",
            "element": "lightning",
            "projectile": False,
            "description": "Atinge um inimigo com um corte de Raio e causa 130% do dano de habilidade.",
        },
    },
    "ethereal_gladiator": {
        "class_id": "rune_blade",
        "passive": {
            "name": "Passo Etéreo",
            "description": "+7 pontos percentuais de esquiva e +5% de velocidade de movimento.",
            "modifiers": {"dodge_chance": 0.07, "move_speed": 0.05},
        },
        "skill": {
            "id": "ethereal_rift",
            "name": "Fenda Etérea",
            "mana": 25,
            "cooldown": 6.0,
            "damage_multiplier": 1.2,
            "damage_type": "physical",
            "projectile": False,
            "description": "Atinge um inimigo e causa 120% do dano de habilidade.",
        },
    },
    "soul_forger": {
        "class_id": "rune_blade",
        "passive": {
            "name": "Arsenal de Almas",
            "description": "+8 pontos percentuais de chance de surto de habilidade e +15% de dano do surto.",
            "modifiers": {"skill_burst_chance": 0.08, "skill_burst_damage": 0.15},
        },
        "skill": {
            "id": "spectral_blades",
            "name": "Lâminas Espectrais",
            "mana": 30,
            "cooldown": 7.0,
            "damage_multiplier": 1.3,
            "damage_type": "magical",
            "element": "umbral",
            "projectile": True,
            "description": "Atinge um inimigo e causa 130% do dano de habilidade.",
        },
    },
}

SPECIALIZATION_EPIC_ABILITIES = {
    "berserker": (
        {
            "id": "crimson_rupture",
            "name": "Ruptura Carmesim",
            "mana": 38,
            "cooldown": 28.0,
            "damage_multiplier": 1.65,
            "damage_type": "physical",
            "projectile": False,
            "ultimate": True,
            "effect_kind": "combo",
            "strike_count": 3,
            "description": "Desfere três impactos em sequência; o último golpe concentra a força do combo.",
        },
    ),
    "guardian_bastion": (
        {
            "id": "unyielding_wall",
            "name": "Muralha Inabalável",
            "mana": 36,
            "cooldown": 30.0,
            "damage_multiplier": 1.1,
            "damage_type": "physical",
            "projectile": False,
            "ultimate": True,
            "effect_kind": "guard",
            "damage_reduction_bonus": .35,
            "effect_duration": 5.0,
            "description": "Golpeia o alvo e ergue uma proteção que reduz o dano recebido por alguns instantes.",
        },
        {
            "id": "firmament_impact",
            "name": "Impacto do Firmamento",
            "mana": 42,
            "cooldown": 32.0,
            "damage_multiplier": 1.2,
            "damage_type": "physical",
            "projectile": False,
            "ultimate": True,
            "effect_kind": "repulse",
            "area_radius": 190,
            "knockback_distance": 125,
            "description": "Libera uma onda de impacto que fere e afasta os inimigos ao redor.",
        },
    ),
    "warlord": (
        {
            "id": "vanguard_decree",
            "name": "Decreto da Vanguarda",
            "mana": 34,
            "cooldown": 27.0,
            "damage_multiplier": 1.9,
            "damage_type": "physical",
            "projectile": False,
            "ultimate": True,
            "effect_kind": "execution",
            "mana_refund_on_kill_fraction": .30,
            "description": "Marca o alvo com um golpe de comando; derrotá-lo devolve parte da Mana gasta.",
        },
    ),
    "sharpshooter": (
        {
            "id": "horizon_line",
            "name": "Linha do Horizonte",
            "mana": 36,
            "cooldown": 29.0,
            "damage_multiplier": 1.8,
            "damage_type": "physical",
            "projectile": True,
            "ultimate": True,
            "effect_kind": "precision",
            "force_critical": True,
            "description": "Dispara um projétil de precisão que sempre acerta um golpe crítico.",
        },
    ),
    "beast_master": (
        {
            "id": "threefold_hunt",
            "name": "Chamado das Três Presas",
            "mana": 40,
            "cooldown": 30.0,
            "damage_multiplier": 1.65,
            "damage_type": "physical",
            "projectile": False,
            "ultimate": True,
            "effect_kind": "echo_strikes",
            "echo_count": 3,
            "description": "Coordena três ataques de energia selvagem contra o mesmo alvo.",
        },
    ),
    "arcane_archer": (
        {
            "id": "lightning_constellation",
            "name": "Constelação de Raios",
            "mana": 42,
            "cooldown": 31.0,
            "damage_multiplier": 1.35,
            "damage_type": "magical",
            "element": "lightning",
            "projectile": True,
            "ultimate": True,
            "effect_kind": "chain",
            "area_radius": 260,
            "chain_count": 3,
            "chain_damage_fraction": .60,
            "description": "Dispara um raio que salta para até dois inimigos próximos.",
        },
    ),
    "archmage": (
        {
            "id": "collapsing_core",
            "name": "Núcleo em Colapso",
            "mana": 46,
            "cooldown": 34.0,
            "damage_multiplier": 1.55,
            "damage_type": "magical",
            "element": "fire",
            "projectile": True,
            "ultimate": True,
            "effect_kind": "area_burst",
            "area_radius": 185,
            "description": "Lança uma concentração de Fogo que explode e atinge inimigos próximos.",
        },
        {
            "id": "inertia_well",
            "name": "Poço de Inércia",
            "mana": 48,
            "cooldown": 36.0,
            "damage_multiplier": 1.25,
            "damage_type": "magical",
            "element": "umbral",
            "projectile": False,
            "ultimate": True,
            "effect_kind": "gravity_well",
            "area_radius": 210,
            "pull_distance": 105,
            "immobilize_duration": 1.5,
            "description": "Cria um núcleo gravitacional que atrai, prende por alguns instantes e fere inimigos próximos.",
        },
    ),
    "necromancer": (
        {
            "id": "void_tribute",
            "name": "Tributo ao Vazio",
            "mana": 38,
            "cooldown": 29.0,
            "damage_multiplier": 1.45,
            "heal_damage_fraction": .35,
            "damage_type": "magical",
            "element": "umbral",
            "projectile": False,
            "ultimate": True,
            "effect_kind": "drain",
            "description": "Drena a essência do alvo e converte parte do dano em Vida.",
        },
        {
            "id": "harvest_echoes",
            "name": "Erga-se",
            "mana": 44,
            "cooldown": 34.0,
            "damage_multiplier": 1.4,
            "damage_type": "magical",
            "element": "umbral",
            "projectile": False,
            "ultimate": True,
            "effect_kind": "shadow_raise",
            "summon_attacks": 3,
            "summon_duration": 15.0,
            "summon_damage_fraction": .35,
            "summon_limit": 3,
            "description": "Se o golpe derrotar o alvo, transforma sua sombra em aliada. Até três soldados acrescentam 35% de dano aos próximos três ataques cada; desaparecem após 15 segundos.",
        },
    ),
    "sage": (
        {
            "id": "winter_sanctuary",
            "name": "Santuário de Inverno",
            "mana": 40,
            "cooldown": 32.0,
            "damage_multiplier": 1.0,
            "heal_max_health_fraction": .18,
            "damage_type": "magical",
            "element": "ice",
            "projectile": True,
            "ultimate": True,
            "effect_kind": "sanctuary",
            "area_radius": 165,
            "area_center": "player",
            "damage_reduction_bonus": .20,
            "effect_duration": 5.0,
            "description": "Libera uma onda de Gelo que restaura Vida e reduz o dano recebido por alguns instantes.",
        },
    ),
    "spellblade": (
        {
            "id": "rune_convergence",
            "name": "Convergência Rúnica",
            "mana": 40,
            "cooldown": 30.0,
            "damage_multiplier": 1.75,
            "damage_type": "magical",
            "element": "lightning",
            "projectile": False,
            "ultimate": True,
            "effect_kind": "rune_combo",
            "description": "Une força marcial e energia rúnica em um corte concentrado.",
        },
    ),
    "ethereal_gladiator": (
        {
            "id": "instant_crossing",
            "name": "Travessia do Instante",
            "mana": 36,
            "cooldown": 28.0,
            "damage_multiplier": 1.45,
            "damage_type": "physical",
            "projectile": False,
            "ultimate": True,
            "effect_kind": "evasion",
            "dodge_chance_bonus": .35,
            "effect_duration": 4.0,
            "description": "Executa um corte veloz e aumenta muito a chance de esquiva por alguns instantes.",
        },
    ),
    "soul_forger": (
        {
            "id": "echo_forge",
            "name": "Forja do Eco",
            "mana": 42,
            "cooldown": 31.0,
            "damage_multiplier": 1.7,
            "damage_type": "magical",
            "element": "umbral",
            "projectile": True,
            "ultimate": True,
            "effect_kind": "echo_strikes",
            "echo_count": 3,
            "description": "Lança lâminas espectrais que repetem o impacto contra o alvo.",
        },
    ),
}

SKILLS = {
    skill["id"]: skill
    for skill in (
        *CLASS_BASE_SKILLS.values(),
        *(specialization["skill"] for specialization in SPECIALIZATION_ABILITIES.values()),
        *(skill for epic_skills in SPECIALIZATION_EPIC_ABILITIES.values()
          for skill in epic_skills),
    )
}


def keystone_talent_id(class_id: str, specialization_id: str) -> str:
    return f"{class_id}_v105_{specialization_id}_keystone"


def epic_unlock_talent_id(class_id: str, specialization_id: str, skill_id: str) -> str:
    return f"{class_id}_v106_{specialization_id}_{skill_id}_unlock"


def skill_upgrade_talent_id(
    class_id: str, specialization_id: str, skill_id: str
) -> str:
    return f"{class_id}_v106_{specialization_id}_{skill_id}_mastery"


def available_class_skills(class_id: str, specialization_id=None, purchased_talents=()):
    """Return the base, signature, and purchased epic skills for this character."""
    skills = [dict(CLASS_BASE_SKILLS[class_id])]
    specialization = SPECIALIZATION_ABILITIES.get(specialization_id)
    if not specialization or specialization["class_id"] != class_id:
        return skills

    owned = set(purchased_talents)
    signature_id = keystone_talent_id(class_id, specialization_id)
    if signature_id in owned:
        skills.append(dict(specialization["skill"]))
    for epic_skill in SPECIALIZATION_EPIC_ABILITIES.get(specialization_id, ()):
        if epic_unlock_talent_id(
            class_id, specialization_id, epic_skill["id"]
        ) in owned:
            skills.append(dict(epic_skill))
    return skills


def normalized_skill_slots(
    class_id: str, specialization_id=None, purchased_talents=(), requested_slots=()
):
    """Keep only unlocked, unique skills and limit the hotbar to one ultimate."""
    available = {
        skill["id"]: skill
        for skill in available_class_skills(
            class_id, specialization_id, purchased_talents
        )
    }
    slots = ["basic", "", "", ""]
    equipped = set()
    ultimate_equipped = False
    requested = list(requested_slots) if isinstance(requested_slots, (list, tuple)) else []
    for index, skill_id in enumerate(requested[1:4], start=1):
        skill = available.get(skill_id)
        if not skill or skill_id in equipped:
            continue
        if skill.get("ultimate") and ultimate_equipped:
            continue
        slots[index] = skill_id
        equipped.add(skill_id)
        ultimate_equipped = ultimate_equipped or bool(skill.get("ultimate"))
    if not equipped:
        normal_skills = [
            skill for skill in available.values() if not skill.get("ultimate")
        ]
        ultimate_skills = [
            skill for skill in available.values() if skill.get("ultimate")
        ]
        defaults = [*normal_skills, *ultimate_skills[:1]][:3]
        for index, skill in enumerate(defaults, start=1):
            slots[index] = skill["id"]
    return slots


def active_class_skill(class_id: str, specialization_id=None, purchased_talents=()):
    base_skill = CLASS_BASE_SKILLS[class_id]
    specialization = SPECIALIZATION_ABILITIES.get(specialization_id)
    if specialization and specialization["class_id"] == class_id:
        keystone_ids = {
            keystone_talent_id(class_id, specialization_id),
            f"{class_id}_v104_{specialization_id}_keystone",
        }
        if keystone_ids & set(purchased_talents):
            return dict(specialization["skill"])
    return dict(base_skill)
