"""Class legacy talent records and the current radial passive graphs."""

from __future__ import annotations

from .abilities import (
    CLASS_BASE_SKILLS,
    SPECIALIZATION_ABILITIES,
    SPECIALIZATION_EPIC_ABILITIES,
    epic_unlock_talent_id,
    keystone_talent_id,
    skill_upgrade_talent_id,
)


def _node(node_id, name, branch, tier, cost, prerequisite, category, effect, agility_bonus=0, **extra):
    node = {
        "id": node_id,
        "name": name,
        "branch": branch,
        "tier": tier,
        "cost": cost,
        "prerequisite": prerequisite,
        "category": category,
        "effect": effect,
        "agility_bonus": agility_bonus,
    }
    node.update(extra)
    return node


TREES = {
    "guardian": {
        "title": "Trilhas do Guardião",
        "subtitle": "Resistência, impacto e proteção da linha de frente.",
        "branches": ["Vanguarda", "Bastião", "Juramento"],
        "nodes": [
            _node("guard_might", "Força do Umbral", "Vanguarda", 1, 1, None, "Atributo", "+2 Força permanente."),
            _node("guard_vigor", "Pulso de Granito", "Bastião", 1, 1, None, "Atributo", "+2 Vitalidade permanente."),
            _node("guard_ward", "Guarda de Aço", "Juramento", 1, 1, None, "Defesa", "+2% de defesa permanente."),
            _node("guard_breaker", "Golpe Demolidor", "Vanguarda", 2, 2, "guard_might", "Vantagem", "+4% de dano contra inimigos resistentes."),
            _node("guard_wall", "Muralha Viva", "Bastião", 2, 2, "guard_vigor", "Vantagem", "+5% de vida máxima."),
            _node("guard_rebuke", "Revide do Bastião", "Juramento", 2, 2, "guard_ward", "Habilidade passiva", "Bloqueios fortalecem o próximo ataque."),
            _node("guard_stance", "Postura Inabalável", "Vanguarda", 3, 3, "guard_breaker", "Vantagem", "Reduz dano recebido enquanto estiver cercado."),
            _node("guard_last_oath", "Último Juramento", "Bastião", 3, 3, "guard_wall", "Habilidade passiva", "Uma vez por sala, sobrevive a um golpe fatal com pouca vida."),
        ],
    },
    "ash_weaver": {
        "title": "Trilhas do Tecelão",
        "subtitle": "Energia arcana, domínio de área e controle das cinzas.",
        "branches": ["Pirotecelagem", "Véu Arcano", "Ressonância"],
        "nodes": [
            _node("weaver_energy", "Fonte de Cinzas", "Pirotecelagem", 1, 1, None, "Atributo", "+2 Energia permanente."),
            _node("weaver_focus", "Foco Silencioso", "Véu Arcano", 1, 1, None, "Atributo", "+2 Agilidade permanente.", 2),
            _node("weaver_barrier", "Véu Protetor", "Ressonância", 1, 1, None, "Defesa", "+2% de resistência mágica permanente."),
            _node("weaver_cinder", "Chuva de Brasas", "Pirotecelagem", 2, 2, "weaver_energy", "Habilidade passiva", "Habilidades de área ganham alcance."),
            _node("weaver_mirror", "Espelho de Cinzas", "Véu Arcano", 2, 2, "weaver_focus", "Vantagem", "+4% de esquiva após conjurar."),
            _node("weaver_echo", "Eco Ressonante", "Ressonância", 2, 2, "weaver_barrier", "Habilidade passiva", "Habilidades têm chance de repetir com força reduzida."),
            _node("weaver_wildfire", "Fogo Errante", "Pirotecelagem", 3, 3, "weaver_cinder", "Vantagem", "+8% de dano mágico contra grupos."),
            _node("weaver_ashform", "Forma de Fuligem", "Véu Arcano", 3, 3, "weaver_mirror", "Habilidade passiva", "Ao receber dano alto, ganha uma barreira temporária."),
        ],
    },
    "wild_scout": {
        "title": "Trilhas do Vigia",
        "subtitle": "Precisão, mobilidade e domínio da distância.",
        "branches": ["Precisão", "Errância", "Caçada"],
        "nodes": [
            _node("scout_aim", "Olho do Ermo", "Precisão", 1, 1, None, "Atributo", "+2 Agilidade permanente.", 2),
            _node("scout_instinct", "Instinto Selvagem", "Errância", 1, 1, None, "Atributo", "+2 Vitalidade permanente."),
            _node("scout_mark", "Marca de Caça", "Caçada", 1, 1, None, "Vantagem", "+2% de chance de acerto crítico permanente."),
            _node("scout_pierce", "Ponta Perfurante", "Precisão", 2, 2, "scout_aim", "Habilidade passiva", "Projéteis atravessam um alvo adicional."),
            _node("scout_stride", "Passada Ligeira", "Errância", 2, 2, "scout_instinct", "Vantagem", "+5% de velocidade de movimento."),
            _node("scout_pursuit", "Perseguição Implacável", "Caçada", 2, 2, "scout_mark", "Vantagem", "+5% de dano contra alvos marcados."),
            _node("scout_volley", "Rajada do Crepúsculo", "Precisão", 3, 3, "scout_pierce", "Habilidade passiva", "Acertos críticos podem disparar um projétil adicional."),
            _node("scout_ghost", "Rastro Fantasma", "Errância", 3, 3, "scout_stride", "Defesa", "Esquivas concedem redução de dano breve."),
        ],
    },
    "rune_blade": {
        "title": "Trilhas da Lâmina Arcana",
        "subtitle": "Força marcial, energia rúnica e equilíbrio entre ambas.",
        "branches": ["Lâmina", "Runas", "Convergência"],
        "nodes": [
            _node("rune_force", "Corte Rúnico", "Lâmina", 1, 1, None, "Atributo", "+2 Força permanente."),
            _node("rune_energy", "Núcleo Arcano", "Runas", 1, 1, None, "Atributo", "+2 Energia permanente."),
            _node("rune_balance", "Equilíbrio Marcial", "Convergência", 1, 1, None, "Atributo", "+1 Força e +1 Energia permanentes."),
            _node("rune_combo", "Sequência Vinculada", "Lâmina", 2, 2, "rune_force", "Habilidade passiva", "Ataques físicos fortalecem a próxima habilidade rúnica."),
            _node("rune_surge", "Surto Inscrito", "Runas", 2, 2, "rune_energy", "Vantagem", "+5% de dano mágico após um golpe corpo a corpo."),
            _node("rune_guard", "Guarda Convergente", "Convergência", 2, 2, "rune_balance", "Defesa", "+3% de defesa e resistência mágica."),
            _node("rune_tempest", "Tempestade de Aço", "Lâmina", 3, 3, "rune_combo", "Habilidade passiva", "Habilidades podem repetir parte do último golpe físico."),
            _node("rune_overload", "Sobrecarga Rúnica", "Runas", 3, 3, "rune_surge", "Vantagem", "+8% de dano de habilidade contra chefes."),
        ],
    },
}


SPECIALIZATION_UNLOCK_LEVEL = 100
CLASS_SPECIALIZATIONS = {
    "guardian": (
        {"id": "berserker", "name": "Furioso", "description": "Aumenta o dano dos seus ataques e pode liberar um golpe ainda mais poderoso."},
        {"id": "guardian_bastion", "name": "Guardião", "description": "Aumenta sua Vida máxima e reduz o dano recebido. Seu golpe de escudo também fica mais forte."},
        {"id": "warlord", "name": "Senhor da Guerra", "description": "Suas habilidades recarregam mais rápido, e derrotar inimigos recupera Mana. Sua investida pode devolver parte da Mana gasta."},
    ),
    "wild_scout": (
        {"id": "sharpshooter", "name": "Atirador de Elite", "description": "Aumenta o alcance e a chance de acerto crítico, além de liberar um disparo poderoso."},
        {"id": "beast_master", "name": "Domador de Feras", "description": "Reduz o dano recebido, recupera Mana ao derrotar inimigos e fortalece seu ataque."},
        {"id": "arcane_archer", "name": "Arqueiro Arcano", "description": "Aumenta o dano das habilidades e a chance de acerto crítico com uma flecha mágica poderosa."},
    ),
    "ash_weaver": (
        {"id": "archmage", "name": "Arquimago", "description": "Aumenta o dano das habilidades e sua reserva de Mana, além de liberar uma poderosa magia."},
        {"id": "necromancer", "name": "Necromante", "description": "Recupera Mana ao derrotar inimigos e transforma parte do dano causado em Vida."},
        {"id": "sage", "name": "Sábio", "description": "Reduz o dano recebido, aumenta a cura entre ondas e pode recuperar Vida ao atingir um inimigo."},
    ),
    "rune_blade": (
        {"id": "spellblade", "name": "Lâmina Arcana", "description": "Fortalece seus ataques e habilidades com uma lâmina elemental poderosa."},
        {"id": "ethereal_gladiator", "name": "Gladiador Etéreo", "description": "Aumenta sua esquiva e velocidade, além de liberar uma habilidade que recarrega rapidamente."},
        {"id": "soul_forger", "name": "Forjador de Almas", "description": "Aumenta a chance e o dano dos seus golpes especiais, além de fortalecer seu ataque."},
    ),
}

_ATTRIBUTE_LABELS = {
    "strength": "Força",
    "agility": "Agilidade",
    "vitality": "Vitalidade",
    "energy": "Energia",
}
_ATTRIBUTE_SECONDARIES = {
    "guardian": {"strength": "vitality", "agility": "vitality", "vitality": "strength", "energy": "strength"},
    "ash_weaver": {"strength": "agility", "agility": "energy", "vitality": "energy", "energy": "agility"},
    "wild_scout": {"strength": "agility", "agility": "strength", "vitality": "agility", "energy": "agility"},
    "rune_blade": {"strength": "energy", "agility": "strength", "vitality": "energy", "energy": "strength"},
}


def _attribute_path_nodes(class_id: str) -> list[dict]:
    """Generate three choice tiers for each permanent attribute path."""
    nodes = []
    for stat in _ATTRIBUTE_LABELS:
        secondary = _ATTRIBUTE_SECONDARIES[class_id][stat]
        label = _ATTRIBUTE_LABELS[stat]
        secondary_label = _ATTRIBUTE_LABELS[secondary]
        root_id = f"{class_id}_attribute_{stat}"
        nodes.append(_node(
            root_id, f"Fundamento de {label}", "Fundamentos", 1, 1, None,
            "Atributo", f"+2 {label} permanente.", is_attribute_path=True,
            attribute_path_stat=stat, stat_bonuses={stat: 2},
        ))
        paths = (
            ("mastery", f"Domínio de {label}", {stat: 4}, f"+4 {label} permanente."),
            ("cross", f"Confluência de {label}", {stat: 2, secondary: 2}, f"+2 {label} e +2 {secondary_label} permanentes."),
        )
        for path_id, path_name, bonuses, description in paths:
            second_id = f"{root_id}_{path_id}"
            nodes.append(_node(
                second_id, path_name, "Fundamentos", 2, 2, root_id,
                "Atributo", description, is_attribute_path=True,
                attribute_path_stat=stat, stat_bonuses=bonuses,
            ))
            third_options = (
                ("focus", f"Apogeu de {label}", {stat: 6}, f"+6 {label} permanente."),
                ("balance", f"Harmonia de {label}", {stat: 3, secondary: 3}, f"+3 {label} e +3 {secondary_label} permanentes."),
            ) if path_id == "mastery" else (
                ("focus", f"Aprofundar {label}", {stat: 4, secondary: 2}, f"+4 {label} e +2 {secondary_label} permanentes."),
                ("balance", f"Convergência de {secondary_label}", {stat: 2, secondary: 4}, f"+2 {label} e +4 {secondary_label} permanentes."),
            )
            for end_id, end_name, end_bonuses, end_description in third_options:
                nodes.append(_node(
                    f"{second_id}_{end_id}", end_name, "Fundamentos", 3, 3, second_id,
                    "Atributo", end_description, is_attribute_path=True,
                    attribute_path_stat=stat, stat_bonuses=end_bonuses,
                ))
    return nodes


for _class_id, _tree in TREES.items():
    _tree["attribute_nodes"] = _attribute_path_nodes(_class_id)

LEGACY_NODE_INDEX = {
    node["id"]: {**node, "class_id": class_id}
    for class_id, tree in TREES.items()
    for node in (*tree["nodes"], *tree["attribute_nodes"])
}


# Estrutura radial de grafo: coordenadas no viewBox 1200 × 1200. Os setores
# são estilos de combate disponíveis para qualquer classe; os atributos
# concedidos em cada setor variam conforme a classe selecionada.
MAP_CENTER = {"x": 0, "y": 0}
RADIAL_SECTORS = (
    {"id": "vanguard", "name": "Vanguarda", "angle": -90, "primary": "strength", "secondary": "agility"},
    {"id": "bastion", "name": "Bastião", "angle": -30, "primary": "vitality", "secondary": "strength"},
    {"id": "precision", "name": "Precisão", "angle": 30, "primary": "agility", "secondary": "energy"},
    {"id": "hunt", "name": "Caçada", "angle": 90, "primary": "agility", "secondary": "strength"},
    {"id": "arcane", "name": "Arcano", "angle": 150, "primary": "energy", "secondary": "vitality"},
    {"id": "convergence", "name": "Convergência", "angle": 210, "primary": "strength", "secondary": "energy"},
)
_CLASS_SECTOR_STATS = {
    "guardian": {
        "vanguard": ("strength", "vitality"), "bastion": ("vitality", "strength"),
        "precision": ("agility", "vitality"), "hunt": ("strength", "agility"),
        "arcane": ("energy", "vitality"), "convergence": ("strength", "vitality"),
    },
    "wild_scout": {
        "vanguard": ("strength", "agility"), "bastion": ("vitality", "agility"),
        "precision": ("agility", "strength"), "hunt": ("agility", "vitality"),
        "arcane": ("energy", "agility"), "convergence": ("agility", "strength"),
    },
    "ash_weaver": {
        "vanguard": ("strength", "agility"), "bastion": ("vitality", "energy"),
        "precision": ("agility", "energy"), "hunt": ("agility", "vitality"),
        "arcane": ("energy", "vitality"), "convergence": ("energy", "agility"),
    },
    "rune_blade": {
        "vanguard": ("strength", "energy"), "bastion": ("vitality", "strength"),
        "precision": ("agility", "strength"), "hunt": ("strength", "agility"),
        "arcane": ("energy", "strength"), "convergence": ("energy", "strength"),
    },
}
_STAT_LABELS = {"strength": "Força", "agility": "Agilidade", "vitality": "Vitalidade", "energy": "Energia"}


def _point(radius: float, angle: float) -> tuple[int, int]:
    import math

    radians = math.radians(angle)
    return round(MAP_CENTER["x"] + radius * math.cos(radians)), round(MAP_CENTER["y"] + radius * math.sin(radians))


def _graph_node(class_id: str, node_id: str, name: str, category: str, x: int, y: int,
                cost: int, effect: str, stat_bonuses=None, **extra) -> dict:
    return {
        "id": node_id, "class_id": class_id, "name": name, "short_name": name,
        "category": category, "x": x, "y": y, "cost": cost,
        "effect": effect, "stat_bonuses": stat_bonuses or {}, **extra,
    }


def radial_graph_for_class(class_id: str) -> dict:
    """Build a connected, undirected six-sector passive graph for one class."""
    nodes = []
    edges = set()
    roots = []
    center_id = f"{class_id}_start_core"
    nodes.append(_graph_node(
        class_id, center_id, "Núcleo do Recomeço", "starting", 0, 0, 0,
        "Origem central gratuita. O ponto de partida não concede atributos por si só.",
        {}, is_root_option=True,
    ))
    roots.append({"id": center_id, "name": "Núcleo do Recomeço", "description": "Origem central e equilibrada."})
    sector_roads = {}

    def connect(left: str, right: str):
        edges.add(tuple(sorted((left, right))))

    for sector in RADIAL_SECTORS:
        sector_id = sector["id"]
        angle = sector["angle"]
        primary, secondary = _CLASS_SECTOR_STATS[class_id][sector_id]
        root_id = f"{class_id}_start_{sector_id}"
        root_x, root_y = _point(110, angle)
        nodes.append(_graph_node(
            class_id, root_id, sector["name"], "starting", root_x, root_y, 0,
            f"Origem gratuita do setor {sector['name']}. O ponto de partida não concede atributos por si só.",
            {}, is_root_option=True, sector=sector_id,
        ))
        roots.append({"id": root_id, "name": sector["name"], "description": f"Origem de {sector['name']} · afinidade: {_STAT_LABELS[primary]}."})
        connect(center_id, root_id)

        road_ids = []
        for road_number, radius in enumerate((220, 295, 365), start=1):
            node_id = f"{class_id}_{sector_id}_road_{road_number}"
            x, y = _point(radius, angle)
            nodes.append(_graph_node(
                class_id, node_id, f"Trilha de {sector['name']} {road_number}", "small", x, y, 1,
                f"+1 {_STAT_LABELS[primary]} permanente.", {primary: 1}, sector=sector_id,
            ))
            road_ids.append(node_id)
        connect(root_id, road_ids[0])
        connect(center_id, road_ids[0])
        connect(road_ids[0], road_ids[1])
        connect(road_ids[1], road_ids[2])
        sector_roads[sector_id] = road_ids

        wheel_ids = []
        for index, offset in enumerate((-24, -12, 0, 12, 24), start=1):
            wheel_id = f"{class_id}_{sector_id}_wheel_{index}"
            x, y = _point(400, angle + offset)
            bonus = {primary: 1}
            effect = f"+1 {_STAT_LABELS[primary]} permanente."
            if index in (1, 5):
                bonus[secondary] = bonus.get(secondary, 0) + 1
                effect += f" +1 {_STAT_LABELS[secondary]} permanente."
            nodes.append(_graph_node(
                class_id, wheel_id, f"Roda de {sector['name']} · {index}", "small", x, y, 1,
                effect, bonus, sector=sector_id, cluster_id=f"{class_id}_{sector_id}_wheel",
            ))
            wheel_ids.append(wheel_id)
        connect(road_ids[2], wheel_ids[2])
        for left, right in zip(wheel_ids, wheel_ids[1:]):
            connect(left, right)

        notable_id = f"{class_id}_{sector_id}_notable"
        notable_x, notable_y = _point(455, angle)
        nodes.append(_graph_node(
            class_id, notable_id, f"Notável: {sector['name']}", "notable", notable_x, notable_y, 2,
            f"+3 {_STAT_LABELS[primary]} e +2 {_STAT_LABELS[secondary]} permanentes.",
            {primary: 3, secondary: 2}, sector=sector_id,
        ))
        for wheel_id in wheel_ids:
            connect(wheel_id, notable_id)

        socket_id = f"{class_id}_{sector_id}_socket"
        socket_x, socket_y = _point(300, angle + 32)
        nodes.append(_graph_node(
            class_id, socket_id, f"Encaixe: {sector['name']}", "socket", socket_x, socket_y, 1,
            "Espaço para modificador externo. Encaixes serão ativados com o sistema de itens.",
            {}, sector=sector_id, allocatable=False,
        ))
        connect(road_ids[1], socket_id)

        keystone_id = f"{class_id}_{sector_id}_keystone"
        key_x, key_y = _point(540, angle)
        nodes.append(_graph_node(
            class_id, keystone_id, f"Keystone: {sector['name']}", "keystone", key_x, key_y, 4,
            "Alteração de alto impacto com risco e recompensa. Efeito será definido no balanceamento da classe.",
            {}, sector=sector_id, allocatable=False,
        ))
        connect(notable_id, keystone_id)

    # Estradas circulares conectam os seis setores sem depender de uma única
    # hierarquia; cada aresta é não direcionada e as adjacências são simétricas.
    for index, sector in enumerate(RADIAL_SECTORS):
        next_sector = RADIAL_SECTORS[(index + 1) % len(RADIAL_SECTORS)]
        connect(sector_roads[sector["id"]][0], sector_roads[next_sector["id"]][0])
        connect(sector_roads[sector["id"]][2], sector_roads[next_sector["id"]][2])

    edges_list = [{"from": left, "to": right} for left, right in sorted(edges)]
    adjacency = {node["id"]: set() for node in nodes}
    for edge in edges_list:
        adjacency[edge["from"]].add(edge["to"])
        adjacency[edge["to"]].add(edge["from"])
    for node in nodes:
        node["neighbors"] = sorted(adjacency[node["id"]])
    sectors = []
    for sector in RADIAL_SECTORS:
        x, y = _point(165, sector["angle"])
        sectors.append({"id": sector["id"], "name": sector["name"], "x": x, "y": y})
    return {"nodes": nodes, "edges": edges_list, "roots": roots,
            "sectors": sectors, "adjacency": adjacency}


RADIAL_GRAPHS_V102 = {class_id: radial_graph_for_class(class_id) for class_id in TREES}
NODE_INDEX = dict(LEGACY_NODE_INDEX)
for _class_id, _graph in RADIAL_GRAPHS_V102.items():
    _old_nodes = {node["id"]: node for node in _graph["nodes"]}
    NODE_INDEX.update(_old_nodes)
    LEGACY_NODE_INDEX.update(_old_nodes)


# Os seis caminhos v0.103 ficam apenas no índice de legado: não são opções
# atuais nem novos caminhos de classe. Seus custos continuam contabilizados.
LEGACY_CLASS_PATHS_V103 = {
    "guardian": (("berserker", "Furioso"), ("bastion", "Guardião / Bastião"), ("warlord", "Senhor da Guerra"), ("veteran", "Veterano de Guerra"), ("duelist", "Duelista de Aço"), ("oathkeeper", "Juramento do Guardião")),
    "wild_scout": (("sharpshooter", "Atirador de Elite"), ("beast_master", "Domador de Feras"), ("arcane_archer", "Arqueiro Arcano"), ("pathfinder", "Batedor Errante"), ("hunter", "Caçador de Alvos"), ("survivalist", "Sobrevivente do Ermo")),
    "ash_weaver": (("archmage", "Arquimago"), ("necromancer", "Necromante"), ("sage", "Sábio / Erudito"), ("elementalist", "Tecelão Elemental"), ("arcane_ward", "Véu Protetor"), ("summoner", "Invocador de Cinzas")),
    "rune_blade": (("spellblade", "Lâmina Arcana"), ("ethereal_gladiator", "Gladiador Etéreo"), ("soul_forger", "Forjador de Almas"), ("rune_duelist", "Duelista Rúnico"), ("astral_guard", "Égide Astral"), ("spectral_arsenal", "Arsenal Espectral")),
}
for _class_id, _paths in LEGACY_CLASS_PATHS_V103.items():
    _legacy_v103 = {
        f"{_class_id}_v103_start_core": {"id": f"{_class_id}_v103_start_core", "class_id": _class_id, "name": "Núcleo anterior", "cost": 0},
    }
    for _path_id, _path_name in _paths:
        _legacy_v103[f"{_class_id}_v103_start_{_path_id}"] = {"id": f"{_class_id}_v103_start_{_path_id}", "class_id": _class_id, "name": _path_name, "cost": 0}
        for _number in range(1, 4):
            _node_id = f"{_class_id}_v103_{_path_id}_road_{_number}"
            _legacy_v103[_node_id] = {"id": _node_id, "class_id": _class_id, "name": f"Fundamento de {_path_name} {_number}", "cost": 1}
        for _number in range(1, 6):
            _node_id = f"{_class_id}_v103_{_path_id}_wheel_{_number}"
            _legacy_v103[_node_id] = {"id": _node_id, "class_id": _class_id, "name": f"Roda de {_path_name} · {_number}", "cost": 1}
        for _suffix, _label, _cost in (("notable", f"Notável: {_path_name}", 2), ("socket", f"Encaixe: {_path_name}", 1), ("keystone", f"Keystone: {_path_name}", 4)):
            _node_id = f"{_class_id}_v103_{_path_id}_{_suffix}"
            _legacy_v103[_node_id] = {"id": _node_id, "class_id": _class_id, "name": _label, "cost": _cost}
    LEGACY_NODE_INDEX.update(_legacy_v103)
NODE_INDEX.update(LEGACY_NODE_INDEX)


# Existem somente três evoluções por classe. Cada uma é um dos três ramos da
# árvore; depois da escolha, apenas o ramo ativo pode receber Pontos de Legado.
CLASS_TREE_PROFILES = {
    "guardian": (
        {"id": "berserker", "name": "Furioso", "angle": -90, "primary": "strength", "secondary": "agility"},
        {"id": "guardian_bastion", "name": "Guardião", "angle": 30, "primary": "vitality", "secondary": "strength"},
        {"id": "warlord", "name": "Senhor da Guerra", "angle": 150, "primary": "energy", "secondary": "vitality"},
    ),
    "wild_scout": (
        {"id": "sharpshooter", "name": "Atirador de Elite", "angle": -90, "primary": "agility", "secondary": "strength"},
        {"id": "beast_master", "name": "Domador de Feras", "angle": 30, "primary": "vitality", "secondary": "agility"},
        {"id": "arcane_archer", "name": "Arqueiro Arcano", "angle": 150, "primary": "energy", "secondary": "agility"},
    ),
    "ash_weaver": (
        {"id": "archmage", "name": "Arquimago", "angle": -90, "primary": "energy", "secondary": "vitality"},
        {"id": "necromancer", "name": "Necromante", "angle": 30, "primary": "energy", "secondary": "agility"},
        {"id": "sage", "name": "Sábio", "angle": 150, "primary": "vitality", "secondary": "energy"},
    ),
    "rune_blade": (
        {"id": "spellblade", "name": "Lâmina Arcana", "angle": -90, "primary": "strength", "secondary": "energy"},
        {"id": "ethereal_gladiator", "name": "Gladiador Etéreo", "angle": 30, "primary": "agility", "secondary": "vitality"},
        {"id": "soul_forger", "name": "Forjador de Almas", "angle": 150, "primary": "energy", "secondary": "strength"},
    ),
}
CLASS_TREE_CORES = {
    "guardian": {"name": "Coração do Umbral", "description": "Raiz da árvore do Guardião."},
    "wild_scout": {"name": "Olho do Ermo", "description": "Raiz da árvore do Arqueiro."},
    "ash_weaver": {"name": "Círculo das Cinzas", "description": "Raiz da árvore do Mago."},
    "rune_blade": {"name": "Núcleo Rúnico", "description": "Raiz da árvore do Gladiador Mágico."},
}


def _radial_graph_for_class_v104(class_id: str) -> dict:
    """Build the previous tree shape to preserve its saved node definitions."""
    nodes = []
    edges = set()
    core_id = f"{class_id}_v104_core"
    core = CLASS_TREE_CORES[class_id]
    nodes.append(_graph_node(class_id, core_id, core["name"], "starting", 0, 0, 0,
                             core["description"], {}, is_root_option=True))

    def connect(left: str, right: str):
        edges.add(tuple(sorted((left, right))))

    sectors = []
    for path in CLASS_TREE_PROFILES[class_id]:
        path_id = path["id"]
        name = path["name"]
        angle = path["angle"]
        primary, secondary = path["primary"], path["secondary"]
        common = {"sector": path_id, "specialization_id": path_id}
        road_ids = []
        for road_number, radius in enumerate((220, 295, 365), start=1):
            node_id = f"{class_id}_v104_{path_id}_road_{road_number}"
            x, y = _point(radius, angle)
            nodes.append(_graph_node(
                class_id, node_id, f"Fundamento · {name} {road_number}", "small", x, y, 1,
                f"+1 {_STAT_LABELS[primary]} permanente no caminho {name}.",
                {primary: 1}, **common,
            ))
            road_ids.append(node_id)
        connect(core_id, road_ids[0])
        connect(road_ids[0], road_ids[1])
        connect(road_ids[1], road_ids[2])

        wheel_ids = []
        for index, offset in enumerate((-24, -12, 0, 12, 24), start=1):
            node_id = f"{class_id}_v104_{path_id}_wheel_{index}"
            x, y = _point(410, angle + offset)
            bonuses = {primary: 1}
            effect = f"+1 {_STAT_LABELS[primary]} permanente."
            if index in (1, 5):
                bonuses[secondary] = bonuses.get(secondary, 0) + 1
                effect += f" +1 {_STAT_LABELS[secondary]} permanente."
            nodes.append(_graph_node(
                class_id, node_id, f"Talento · {name} {index}", "small", x, y, 1,
                effect, bonuses, cluster_id=f"{class_id}_v104_{path_id}_wheel", **common,
            ))
            wheel_ids.append(node_id)
        connect(road_ids[2], wheel_ids[2])
        for left, right in zip(wheel_ids, wheel_ids[1:]):
            connect(left, right)

        notable_id = f"{class_id}_v104_{path_id}_notable"
        notable_x, notable_y = _point(470, angle)
        nodes.append(_graph_node(
            class_id, notable_id, f"Talento especial · {name}", "notable", notable_x, notable_y, 2,
            f"+3 {_STAT_LABELS[primary]} e +2 {_STAT_LABELS[secondary]} permanentes.",
            {primary: 3, secondary: 2}, **common,
        ))
        for wheel_id in wheel_ids:
            connect(wheel_id, notable_id)

        socket_id = f"{class_id}_v104_{path_id}_socket"
        socket_x, socket_y = _point(310, angle + 32)
        nodes.append(_graph_node(
            class_id, socket_id, f"Encaixe · {name}", "socket", socket_x, socket_y, 1,
            f"Este espaço de melhoria do caminho {name} ainda não está disponível.",
            {}, allocatable=False, **common,
        ))
        connect(road_ids[1], socket_id)

        keystone_id = f"{class_id}_v104_{path_id}_keystone"
        specialization_ability = SPECIALIZATION_ABILITIES[path_id]
        base_skill = CLASS_BASE_SKILLS[class_id]
        signature_skill = specialization_ability["skill"]
        key_x, key_y = _point(545, angle)
        nodes.append(_graph_node(
            class_id, keystone_id, f"Talento principal · {name}", "keystone", key_x, key_y, 4,
            (
                f"Desbloqueia {signature_skill['name']} por 4 Pontos de Legado e "
                f"troca sua habilidade comum, {base_skill['name']}, por ela. "
                f"{signature_skill['description']} Custa {signature_skill['mana']} "
                f"Mana e recarrega em {signature_skill['cooldown']:g}s."
            ),
            {}, allocatable=True, grants_skill_id=signature_skill["id"], **common,
        ))
        connect(notable_id, keystone_id)

        label_x, label_y = _point(165, angle)
        sectors.append({"id": path_id, "name": name, "x": label_x, "y": label_y})

    edges_list = [{"from": left, "to": right} for left, right in sorted(edges)]
    adjacency = {node["id"]: set() for node in nodes}
    for edge in edges_list:
        adjacency[edge["from"]].add(edge["to"])
        adjacency[edge["to"]].add(edge["from"])
    for node in nodes:
        node["neighbors"] = sorted(adjacency[node["id"]])
    roots = [{"id": core_id, "name": core["name"], "description": core["description"]}]
    return {"nodes": nodes, "edges": edges_list, "roots": roots,
            "root_id": core_id, "sectors": sectors, "adjacency": adjacency}


RADIAL_GRAPHS_V104 = {
    class_id: _radial_graph_for_class_v104(class_id) for class_id in TREES
}
LEGACY_V104_NODE_INDEX = {
    node["id"]: node
    for graph in RADIAL_GRAPHS_V104.values()
    for node in graph["nodes"]
}
LEGACY_NODE_INDEX.update(LEGACY_V104_NODE_INDEX)
NODE_INDEX.update(LEGACY_V104_NODE_INDEX)


# Cada especialização tem nomes, efeitos e modificadores próprios. O formato
# radial é compartilhado, mas nenhum talento funcional é reaproveitado entre
# classes ou caminhos.
CLASS_TREE_PROFILES = {
    "guardian": (
        {
            "id": "berserker", "name": "Furioso", "angle": -90,
            "primary": "strength", "secondary": "agility",
            "road": (
                ("Punho de Ruptura", "Seus ataques básicos causam 2% mais dano.", {"damage": .02}),
                ("Ritmo da Carnificina", "Cada ataque seguido fortalece o próximo golpe, até três ataques seguidos.", {"attack_streak_damage": .01, "attack_streak_cap": 3}),
                ("Talho da Fúria", "Suas habilidades causam 2% mais dano.", {"skill_damage": .02}),
            ),
            "wheel": (
                ("Sangue de Ferro", "Aumenta sua Vida máxima em 2%.", {"max_health": .02}),
                ("Olhar do Duelista", "Aumenta a chance de acerto crítico em 1 ponto percentual.", {"critical_chance": .01}),
                ("Investida Violenta", "Seus ataques básicos causam 2% mais dano.", {"damage": .02}),
                ("Pressão de Guerra", "Causa 2% mais dano a chefes.", {"boss_damage": .02}),
                ("Frenesi Ascendente", "Cada ataque seguido fortalece ainda mais seus golpes.", {"attack_streak_damage": .01}),
            ),
            "amplifier": ("Fio da Execução", "Aumenta a chance de acerto crítico em 2 pontos percentuais.", {"critical_chance": .02}),
            "notable": ("Ímpeto do Carniceiro", "Seus ataques básicos causam 5% mais dano.", {"damage": .05}),
        },
        {
            "id": "guardian_bastion", "name": "Guardião", "angle": 30,
            "primary": "vitality", "secondary": "strength",
            "road": (
                ("Couraça de Granito", "Aumenta sua Vida máxima em 2%.", {"max_health": .02}),
                ("Guarda Inquebrável", "Reduz em 1% o dano recebido.", {"damage_reduction": .01}),
                ("Retorno do Bastião", "Reflete 1% do dano recebido de volta ao atacante.", {"damage_reflection": .01}),
            ),
            "wheel": (
                ("Muralha Interior", "Aumenta sua Vida máxima em 3%.", {"max_health": .03}),
                ("Escudo Reativo", "Reflete 2% do dano recebido.", {"damage_reflection": .02}),
                ("Postura Defensiva", "Reduz em 1% o dano recebido.", {"damage_reduction": .01}),
                ("Último Reduto", "Com pouca Vida, reduz ainda mais o dano recebido.", {"low_health_reduction": .02}),
                ("Fôlego do Guardião", "Aumenta em 2% a cura recebida ao avançar de onda.", {"wave_heal": .02}),
            ),
            "amplifier": ("Revanche de Aço", "Reflete 3% do dano recebido.", {"damage_reflection": .03}),
            "notable": ("Baluarte do Umbral", "Reduz em 3% o dano recebido.", {"damage_reduction": .03}),
        },
        {
            "id": "warlord", "name": "Senhor da Guerra", "angle": 150,
            "primary": "energy", "secondary": "vitality",
            "road": (
                ("Comando Acelerado", "Reduz em 2% o tempo de recarga das habilidades.", {"cooldown_reduction": .02}),
                ("Reserva de Campanha", "Aumenta sua Mana máxima em 2%.", {"max_mana": .02}),
                ("Golpe de Comando", "Suas habilidades causam 2% mais dano.", {"skill_damage": .02}),
            ),
            "wheel": (
                ("Reabastecimento Tático", "Ao derrotar inimigos, recupera 2% da Mana máxima.", {"mana_on_kill": .02}),
                ("Investida Coordenada", "Suas habilidades causam 2% mais dano.", {"skill_damage": .02}),
                ("Execução de Campo", "Abates reduzem em meio segundo a recarga da habilidade.", {"cooldown_refund_on_kill": .5}),
                ("Sinal de Ataque", "Aumenta em 2 pontos percentuais a chance e em 10% o dano dos golpes especiais.", {"skill_burst_chance": .02, "skill_burst_damage": .10}),
                ("Ordem de Extermínio", "Causa 2% mais dano a chefes.", {"boss_damage": .02}),
            ),
            "amplifier": ("Suprimento de Guerra", "Ao derrotar inimigos, recupera mais 2% da Mana máxima.", {"mana_on_kill": .02}),
            "notable": ("Ataque Irrefreável", "Suas habilidades causam 5% mais dano.", {"skill_damage": .05}),
        },
    ),
    "wild_scout": (
        {
            "id": "sharpshooter", "name": "Atirador de Elite", "angle": -90,
            "primary": "agility", "secondary": "strength",
            "road": (
                ("Mira Ajustada", "Aumenta a chance de acerto crítico em 1 ponto percentual.", {"critical_chance": .01}),
                ("Ponta Perfurante", "Projéteis causam 2% mais dano ao atingir.", {"projectile_damage": .02}),
                ("Distância Segura", "Aumenta em 2% o alcance dos ataques.", {"attack_range": .02}),
            ),
            "wheel": (
                ("Flecha de Caça", "Projéteis causam 2% mais dano ao atingir.", {"projectile_damage": .02}),
                ("Olho de Águia", "Aumenta a chance de acerto crítico em 1 ponto percentual.", {"critical_chance": .01}),
                ("Passo de Mira", "Aumenta em 2% o alcance dos ataques.", {"attack_range": .02}),
                ("Alvo Prioritário", "Causa 2% mais dano a chefes.", {"boss_damage": .02}),
                ("Disparo Preparado", "Suas habilidades causam 2% mais dano.", {"skill_damage": .02}),
            ),
            "amplifier": ("Ponto Vulnerável", "Aumenta a chance de acerto crítico em 2 pontos percentuais.", {"critical_chance": .02}),
            "notable": ("Disparo Perfurante", "Projéteis causam 5% mais dano ao atingir.", {"projectile_damage": .05}),
        },
        {
            "id": "beast_master", "name": "Domador de Feras", "angle": 30,
            "primary": "vitality", "secondary": "agility",
            "road": (
                ("Pele de Caçador", "Reduz em 1% o dano recebido.", {"damage_reduction": .01}),
                ("Corrida da Matilha", "Aumenta em 2% sua velocidade de movimento.", {"move_speed": .02}),
                ("Instinto de Fuga", "Aumenta a chance de esquiva em 1 ponto percentual.", {"dodge_chance": .01}),
            ),
            "wheel": (
                ("Mordida Revigorante", "Recupera Vida igual a 1% do dano causado.", {"life_steal": .01}),
                ("Rastro de Presas", "Ao derrotar inimigos, recupera 2% da Mana máxima.", {"mana_on_kill": .02}),
                ("Reflexo Selvagem", "Aumenta a chance de esquiva em 1 ponto percentual.", {"dodge_chance": .01}),
                ("Passada do Predador", "Aumenta em 2% sua velocidade de movimento.", {"move_speed": .02}),
                ("Vigor de Caça", "Aumenta sua Vida máxima em 2%.", {"max_health": .02}),
            ),
            "amplifier": ("Colheita da Matilha", "Recupera Vida igual a mais 2% do dano causado.", {"life_steal": .02}),
            "notable": ("Sobrevivência do Ermo", "Recupera Vida igual a 3% do dano causado.", {"life_steal": .03}),
        },
        {
            "id": "arcane_archer", "name": "Arqueiro Arcano", "angle": 150,
            "primary": "energy", "secondary": "agility",
            "road": (
                ("Flecha Condutora", "Projéteis causam 2% mais dano ao atingir.", {"projectile_damage": .02}),
                ("Faísca Elemental", "Habilidades elementais causam 2% mais dano.", {"elemental_damage": .02}),
                ("Técnica Ressonante", "Suas habilidades causam 2% mais dano.", {"skill_damage": .02}),
            ),
            "wheel": (
                ("Mira Ressonante", "Aumenta a chance de acerto crítico em 1 ponto percentual.", {"critical_chance": .01}),
                ("Arco de Energia", "Projéteis causam 2% mais dano ao atingir.", {"projectile_damage": .02}),
                ("Raio Concentrado", "Habilidades elementais causam 2% mais dano.", {"elemental_damage": .02}),
                ("Disparo Místico", "Suas habilidades causam 2% mais dano.", {"skill_damage": .02}),
                ("Tempestade Arcana", "Causa 2% mais dano a chefes.", {"boss_damage": .02}),
            ),
            "amplifier": ("Núcleo de Raio", "Habilidades elementais causam 3% mais dano.", {"elemental_damage": .03}),
            "notable": ("Flecha de Ressonância", "Suas habilidades causam 5% mais dano.", {"skill_damage": .05}),
        },
    ),
    "ash_weaver": (
        {
            "id": "archmage", "name": "Arquimago", "angle": -90,
            "primary": "energy", "secondary": "vitality",
            "road": (
                ("Foco das Cinzas", "Suas habilidades causam 2% mais dano.", {"skill_damage": .02}),
                ("Chama Condensada", "Habilidades elementais causam 2% mais dano.", {"elemental_damage": .02}),
                ("Reserva Arcana", "Aumenta sua Mana máxima em 2%.", {"max_mana": .02}),
            ),
            "wheel": (
                ("Conjuração Potente", "Suas habilidades causam 2% mais dano.", {"skill_damage": .02}),
                ("Brasa Explosiva", "Habilidades elementais causam 2% mais dano.", {"elemental_damage": .02}),
                ("Projétil Incandescente", "Projéteis causam 2% mais dano ao atingir.", {"projectile_damage": .02}),
                ("Fonte de Mana", "Aumenta sua Mana máxima em 3%.", {"max_mana": .03}),
                ("Sobrecarga Mágica", "Aumenta em 2 pontos percentuais a chance e em 10% o dano dos golpes especiais.", {"skill_burst_chance": .02, "skill_burst_damage": .10}),
            ),
            "amplifier": ("Catalisador de Cinzas", "Suas habilidades causam 3% mais dano.", {"skill_damage": .03}),
            "notable": ("Cataclismo Arcano", "Suas habilidades causam 5% mais dano.", {"skill_damage": .05}),
        },
        {
            "id": "necromancer", "name": "Necromante", "angle": 30,
            "primary": "energy", "secondary": "agility",
            "road": (
                ("Sifão de Almas", "Suas habilidades causam 2% mais dano.", {"skill_damage": .02}),
                ("Essência Roubada", "Recupera Vida igual a 1% do dano causado.", {"life_steal": .01}),
                ("Último Suspiro", "Ao derrotar inimigos, recupera 2% da Mana máxima.", {"mana_on_kill": .02}),
            ),
            "wheel": (
                ("Colheita Vital", "Recupera Vida igual a 1% do dano causado.", {"life_steal": .01}),
                ("Colheita de Mana", "Ao derrotar inimigos, recupera 2% da Mana máxima.", {"mana_on_kill": .02}),
                ("Feitiço Sepulcral", "Suas habilidades causam 2% mais dano.", {"skill_damage": .02}),
                ("Alívio Sombrio", "Aumenta a chance crítica em 1 ponto percentual; acertos críticos restauram Vida adicional.", {"critical_chance": .01, "critical_heal": .02}),
                ("Reservatório Espectral", "Aumenta sua Mana máxima em 2%.", {"max_mana": .02}),
            ),
            "amplifier": ("Dreno Persistente", "Recupera Vida igual a mais 2% do dano causado.", {"life_steal": .02}),
            "notable": ("Ceifador de Almas", "Suas habilidades causam 4% mais dano.", {"skill_damage": .04}),
        },
        {
            "id": "sage", "name": "Sábio", "angle": 150,
            "primary": "vitality", "secondary": "energy",
            "road": (
                ("Véu de Gelo", "Reduz em 1% o dano recebido.", {"damage_reduction": .01}),
                ("Pulso Restaurador", "Aumenta em 1% a cura recebida ao avançar de onda.", {"wave_heal": .01}),
                ("Corpo Equilibrado", "Aumenta sua Vida máxima em 2%.", {"max_health": .02}),
            ),
            "wheel": (
                ("Ritual de Recuperação", "Aumenta em 2% a cura recebida ao avançar de onda.", {"wave_heal": .02}),
                ("Barreira de Geada", "Reduz em 1% o dano recebido.", {"damage_reduction": .01}),
                ("Reserva Serena", "Aumenta sua Mana máxima em 2%.", {"max_mana": .02}),
                ("Onda Harmônica", "Suas habilidades causam 2% mais dano.", {"skill_damage": .02}),
                ("Proteção do Sábio", "Com pouca Vida, reduz ainda mais o dano recebido.", {"low_health_reduction": .02}),
            ),
            "amplifier": ("Círculo de Restauração", "Aumenta em 2% a cura recebida ao avançar de onda.", {"wave_heal": .02}),
            "notable": ("Equilíbrio Perfeito", "Reduz em 3% o dano recebido.", {"damage_reduction": .03}),
        },
    ),
    "rune_blade": (
        {
            "id": "spellblade", "name": "Lâmina Arcana", "angle": -90,
            "primary": "strength", "secondary": "energy",
            "road": (
                ("Corte de Convergência", "Seus ataques básicos causam 2% mais dano.", {"damage": .02}),
                ("Runa de Impacto", "Suas habilidades causam 2% mais dano.", {"skill_damage": .02}),
                ("Selo Elemental", "Habilidades elementais causam 2% mais dano.", {"elemental_damage": .02}),
            ),
            "wheel": (
                ("Marca de Ruptura", "Aumenta a chance de acerto crítico em 1 ponto percentual.", {"critical_chance": .01}),
                ("Canalização Rápida", "Reduz em 2% o tempo de recarga das habilidades.", {"cooldown_reduction": .02}),
                ("Raio na Lâmina", "Habilidades elementais causam 2% mais dano.", {"elemental_damage": .02}),
                ("Corte Ressonante", "Suas habilidades causam 2% mais dano.", {"skill_damage": .02}),
                ("Desafio Rúnico", "Causa 2% mais dano a chefes.", {"boss_damage": .02}),
            ),
            "amplifier": ("Lâmina da Tempestade", "Aumenta a chance de acerto crítico em 2 pontos percentuais.", {"critical_chance": .02}),
            "notable": ("Convergência Arcana", "Seus ataques básicos causam 4% mais dano.", {"damage": .04}),
        },
        {
            "id": "ethereal_gladiator", "name": "Gladiador Etéreo", "angle": 30,
            "primary": "agility", "secondary": "vitality",
            "road": (
                ("Passo Desvanecido", "Aumenta a chance de esquiva em 1 ponto percentual.", {"dodge_chance": .01}),
                ("Corrida Etérea", "Aumenta em 2% sua velocidade de movimento.", {"move_speed": .02}),
                ("Guarda Espectral", "Reduz em 1% o dano recebido.", {"damage_reduction": .01}),
            ),
            "wheel": (
                ("Reflexo Sobrenatural", "Aumenta a chance de esquiva em 1 ponto percentual.", {"dodge_chance": .01}),
                ("Ataque em Movimento", "Seus ataques básicos causam 2% mais dano.", {"damage": .02}),
                ("Recuperação Rápida", "Reduz em 2% o tempo de recarga das habilidades.", {"cooldown_reduction": .02}),
                ("Deslocamento Espectral", "Aumenta em 2% sua velocidade de movimento.", {"move_speed": .02}),
                ("Alcance do Duelista", "Aumenta em 2% o alcance dos ataques.", {"attack_range": .02}),
            ),
            "amplifier": ("Evasão do Crepúsculo", "Aumenta a chance de esquiva em 2 pontos percentuais.", {"dodge_chance": .02}),
            "notable": ("Dança da Arena", "Seus ataques básicos causam 4% mais dano.", {"damage": .04}),
        },
        {
            "id": "soul_forger", "name": "Forjador de Almas", "angle": 150,
            "primary": "energy", "secondary": "strength",
            "road": (
                ("Forja de Impacto", "Aumenta em 2 pontos percentuais a chance de um golpe especial e em 10% seu dano extra.", {"skill_burst_chance": .02, "skill_burst_damage": .10}),
                ("Núcleo de Almas", "Aumenta sua Mana máxima em 2%.", {"max_mana": .02}),
                ("Lâmina de Essência", "Suas habilidades causam 2% mais dano.", {"skill_damage": .02}),
            ),
            "wheel": (
                ("Estouro de Almas", "Aumenta em 2 pontos percentuais a chance de um golpe especial.", {"skill_burst_chance": .02}),
                ("Forja Explosiva", "Aumenta em 2% o dano dos golpes especiais.", {"skill_burst_damage": .02}),
                ("Essência Recuperada", "Ao derrotar inimigos, recupera 2% da Mana máxima.", {"mana_on_kill": .02}),
                ("Ritmo da Forja", "Reduz em 2% o tempo de recarga das habilidades.", {"cooldown_reduction": .02}),
                ("Fogo Interior", "Habilidades elementais causam 2% mais dano.", {"elemental_damage": .02}),
            ),
            "amplifier": ("Cinza Reaproveitada", "Ao derrotar inimigos, recupera mais 2% da Mana máxima.", {"mana_on_kill": .02}),
            "notable": ("Obra-Prima Espiritual", "Suas habilidades causam 4% mais dano.", {"skill_damage": .04}),
        },
    ),
}


def radial_graph_for_class(class_id: str) -> dict:
    """Create one class graph whose specialization nodes have distinct effects."""
    nodes = []
    edges = set()
    core_id = f"{class_id}_v105_core"
    core = CLASS_TREE_CORES[class_id]
    nodes.append(_graph_node(
        class_id, core_id, core["name"], "starting", 0, 0, 0,
        core["description"], {}, is_root_option=True,
    ))

    def connect(left: str, right: str):
        edges.add(tuple(sorted((left, right))))

    sectors = []
    for path in CLASS_TREE_PROFILES[class_id]:
        path_id = path["id"]
        name = path["name"]
        angle = path["angle"]
        primary, secondary = path["primary"], path["secondary"]
        common = {"sector": path_id, "specialization_id": path_id}
        road_ids = []
        for road_number, radius in enumerate((220, 295, 365), start=1):
            node_id = f"{class_id}_v105_{path_id}_road_{road_number}"
            x, y = _point(radius, angle)
            talent_name, effect, modifiers = path["road"][road_number - 1]
            nodes.append(_graph_node(
                class_id, node_id, talent_name, "small", x, y, 2,
                f"+1 {_STAT_LABELS[primary]} permanente. {effect}",
                {primary: 1}, combat_modifiers=modifiers, **common,
            ))
            road_ids.append(node_id)
        connect(core_id, road_ids[0])
        connect(road_ids[0], road_ids[1])
        connect(road_ids[1], road_ids[2])

        wheel_ids = []
        for index, offset in enumerate((-24, -12, 0, 12, 24), start=1):
            node_id = f"{class_id}_v105_{path_id}_wheel_{index}"
            x, y = _point(410, angle + offset)
            talent_name, effect, modifiers = path["wheel"][index - 1]
            bonuses = {primary: 1}
            stat_effect = f"+1 {_STAT_LABELS[primary]} permanente."
            if index in (1, 5):
                bonuses[secondary] = bonuses.get(secondary, 0) + 1
                stat_effect += f" +1 {_STAT_LABELS[secondary]} permanente."
            nodes.append(_graph_node(
                class_id, node_id, talent_name, "small", x, y, 6,
                f"{stat_effect} {effect}", bonuses,
                cluster_id=f"{class_id}_v105_{path_id}_wheel",
                combat_modifiers=modifiers, **common,
            ))
            wheel_ids.append(node_id)
        connect(road_ids[2], wheel_ids[2])
        for left, right in zip(wheel_ids, wheel_ids[1:]):
            connect(left, right)

        amplifier_name, amplifier_effect, amplifier_modifiers = path["amplifier"]
        amplifier_id = f"{class_id}_v105_{path_id}_amplifier"
        amplifier_x, amplifier_y = _point(310, angle + 32)
        nodes.append(_graph_node(
            class_id, amplifier_id, amplifier_name, "small",
            amplifier_x, amplifier_y, 2, amplifier_effect, {},
            combat_modifiers=amplifier_modifiers, **common,
        ))
        connect(road_ids[1], amplifier_id)

        notable_name, notable_effect, notable_modifiers = path["notable"]
        notable_id = f"{class_id}_v105_{path_id}_notable"
        notable_x, notable_y = _point(470, angle)
        nodes.append(_graph_node(
            class_id, notable_id, notable_name, "notable", notable_x, notable_y, 6,
            f"+3 {_STAT_LABELS[primary]} e +2 {_STAT_LABELS[secondary]} permanentes. {notable_effect}",
            {primary: 3, secondary: 2},
            combat_modifiers=notable_modifiers, **common,
        ))
        for wheel_id in wheel_ids:
            connect(wheel_id, notable_id)

        keystone_id = f"{class_id}_v105_{path_id}_keystone"
        specialization_ability = SPECIALIZATION_ABILITIES[path_id]
        base_skill = CLASS_BASE_SKILLS[class_id]
        signature_skill = specialization_ability["skill"]
        key_x, key_y = _point(545, angle)
        nodes.append(_graph_node(
            class_id, keystone_id, f"Talento principal · {name}", "keystone", key_x, key_y, 4,
            (
                f"Desbloqueia {signature_skill['name']} por 4 Pontos de Legado e "
                f"troca sua habilidade comum, {base_skill['name']}, por ela. "
                f"{signature_skill['description']} Custa {signature_skill['mana']} "
                f"Mana e recarrega em {signature_skill['cooldown']:g}s."
            ),
            {}, allocatable=True, grants_skill_id=signature_skill["id"], **common,
        ))
        connect(notable_id, keystone_id)

        epic_skills = SPECIALIZATION_EPIC_ABILITIES.get(path_id, ())
        spell_nodes = [
            ("upgrade", base_skill, .12),
            ("upgrade", signature_skill, .12),
        ]
        for epic_skill in epic_skills:
            spell_nodes.extend((
                ("unlock", epic_skill, 0),
                ("upgrade", epic_skill, .15),
            ))
        node_offsets = [
            (index - (len(spell_nodes) - 1) / 2) * 10
            for index in range(len(spell_nodes))
        ]
        epic_unlock_nodes = {}
        for (node_kind, skill, bonus), offset in zip(spell_nodes, node_offsets):
            spell_x, spell_y = _point(570, angle + offset)
            if node_kind == "unlock":
                spell_node_id = epic_unlock_talent_id(
                    class_id, path_id, skill["id"]
                )
                effect = (
                    f"Desbloqueia a habilidade suprema {skill['name']}. "
                    f"{skill['description']} Custa {skill['mana']} Mana e "
                    f"recarrega em {skill['cooldown']:g}s."
                )
                nodes.append(_graph_node(
                    class_id, spell_node_id, f"Suprema · {skill['name']}",
                    "ultimate", spell_x, spell_y, 4, effect, {},
                    allocatable=True, grants_skill_id=skill["id"],
                    is_ultimate=True, **common,
                ))
                connect(keystone_id, spell_node_id)
                epic_unlock_nodes[skill["id"]] = spell_node_id
            else:
                spell_node_id = skill_upgrade_talent_id(
                    class_id, path_id, skill["id"]
                )
                nodes.append(_graph_node(
                    class_id, spell_node_id,
                    f"Maestria · {skill['name']} · {name}",
                    "spell_upgrade", spell_x, spell_y, 2,
                    f"Aumenta em {bonus:.0%} o dano de {skill['name']}.",
                    {}, skill_id=skill["id"], skill_damage_bonus=bonus,
                    **common,
                ))
                unlock_id = epic_unlock_nodes.get(skill["id"])
                connect(unlock_id or keystone_id, spell_node_id)

        label_x, label_y = _point(165, angle)
        sectors.append({"id": path_id, "name": name, "x": label_x, "y": label_y})

    edges_list = [{"from": left, "to": right} for left, right in sorted(edges)]
    adjacency = {node["id"]: set() for node in nodes}
    for edge in edges_list:
        adjacency[edge["from"]].add(edge["to"])
        adjacency[edge["to"]].add(edge["from"])
    for node in nodes:
        node["neighbors"] = sorted(adjacency[node["id"]])
    roots = [{"id": core_id, "name": core["name"], "description": core["description"]}]
    return {
        "nodes": nodes, "edges": edges_list, "roots": roots,
        "root_id": core_id, "sectors": sectors, "adjacency": adjacency,
    }


RADIAL_GRAPHS = {class_id: radial_graph_for_class(class_id) for class_id in TREES}
NODE_INDEX.update({
    node["id"]: node
    for graph in RADIAL_GRAPHS.values()
    for node in graph["nodes"]
})

for _class_id, _specializations in CLASS_SPECIALIZATIONS.items():
    for _specialization in _specializations:
        _ability = SPECIALIZATION_ABILITIES[_specialization["id"]]
        _path_nodes = [
            node for node in RADIAL_GRAPHS[_class_id]["nodes"]
            if node.get("specialization_id") == _specialization["id"]
            and node.get("allocatable", True)
        ]
        _attribute_gains = {}
        for _node in _path_nodes:
            for _stat, _value in _node["stat_bonuses"].items():
                _attribute_gains[_stat] = _attribute_gains.get(_stat, 0) + _value
        _specialization.update(
            passive=_ability["passive"],
            skill=_ability["skill"],
            base_skill=CLASS_BASE_SKILLS[_class_id],
            epic_skills=list(
                SPECIALIZATION_EPIC_ABILITIES.get(_specialization["id"], ())
            ),
            keystone_cost=4,
            keystone_id=keystone_talent_id(_class_id, _specialization["id"]),
            branch_cost=sum(node["cost"] for node in _path_nodes),
            attribute_cost=sum(
                node["cost"] for node in _path_nodes if node["stat_bonuses"]
            ),
            combat_cost=sum(
                node["cost"] for node in _path_nodes
                if not node["stat_bonuses"]
                and node["id"] != keystone_talent_id(_class_id, _specialization["id"])
            ),
            epic_unlock_cost=sum(
                node["cost"] for node in _path_nodes
                if node.get("grants_skill_id") in {
                    skill["id"]
                    for skill in SPECIALIZATION_EPIC_ABILITIES.get(
                        _specialization["id"], ()
                    )
                }
            ),
            spell_upgrade_cost=sum(
                node["cost"] for node in _path_nodes
                if node.get("skill_damage_bonus")
            ),
            other_combat_cost=(
                sum(
                    node["cost"] for node in _path_nodes
                    if not node["stat_bonuses"]
                    and node["id"] != keystone_talent_id(
                        _class_id, _specialization["id"]
                    )
                )
                - sum(
                    node["cost"] for node in _path_nodes
                    if node.get("grants_skill_id") in {
                        skill["id"]
                        for skill in SPECIALIZATION_EPIC_ABILITIES.get(
                            _specialization["id"], ()
                        )
                    }
                )
                - sum(
                    node["cost"] for node in _path_nodes
                    if node.get("skill_damage_bonus")
                )
            ),
            attribute_gains=_attribute_gains,
            attribute_summary=" · ".join(
                f"+{_attribute_gains[stat]} {_STAT_LABELS[stat]}"
                for stat in _STAT_LABELS if _attribute_gains.get(stat)
            ),
        )


def talent_node(class_id: str, node_id: str) -> dict | None:
    node = NODE_INDEX.get(node_id)
    return node if node and node.get("class_id") == class_id else None


def activated_from_root(class_id: str, root_id: str | None, purchased: set[str]) -> set[str]:
    graph = RADIAL_GRAPHS[class_id]
    if root_id not in {root["id"] for root in graph["roots"]}:
        return set()
    # Acquired nodes are kept only when reachable through acquired neighbours;
    # this prevents stale/corrupt rows from opening disconnected map sections.
    active = {root_id}
    changed = True
    while changed:
        changed = False
        for node_id in purchased - active:
            if graph["adjacency"].get(node_id, set()) & active:
                active.add(node_id)
                changed = True
    return active
