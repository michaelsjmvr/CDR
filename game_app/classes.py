"""Initial playable class definitions used by the character prototype."""

# Class-specific attack ranges drive both the combat target check and the two
# corresponding range circles. Values are prototype tuning and remain balanceable.
CLASSES = {
    "guardian": {
        "name": "Guerreiro",
        "archetype": "Guerreiro",
        "role": "Combate corpo a corpo",
        "portrait_mark": "GU",
        "portrait_style": "guardian",
        "base_attack_range": 125,
        "base_skill_range": 170,
        "base_attributes": {"strength": 28, "agility": 20, "vitality": 25, "energy": 10},
    },
    "ash_weaver": {
        "name": "Tecelão",
        "archetype": "Mago",
        "role": "Magia e controle",
        "portrait_mark": "TE",
        "portrait_style": "mage",
        "base_attack_range": 190,
        "base_skill_range": 255,
        "base_attributes": {"strength": 18, "agility": 18, "vitality": 15, "energy": 30},
    },
    "wild_scout": {
        "name": "Caçador",
        "archetype": "Arqueiro",
        "role": "Combate à distância",
        "portrait_mark": "CA",
        "portrait_style": "archer",
        "base_attack_range": 225,
        "base_skill_range": 305,
        "base_attributes": {"strength": 22, "agility": 25, "vitality": 20, "energy": 15},
    },
    "rune_blade": {
        "name": "Lâmina Arcana",
        "archetype": "Gladiador mágico",
        "role": "Combate físico e magia",
        "portrait_mark": "LA",
        "portrait_style": "rune-blade",
        "base_attack_range": 155,
        "base_skill_range": 210,
        "base_attributes": {"strength": 26, "agility": 26, "vitality": 26, "energy": 26},
    },
}
