"""Season 1 campaign structure and encounter schedule."""

SEASON_1_PHASES = 30
ACT_PHASES = 10
SEASON_1_ACTS = tuple(
    {
        "number": act,
        "first_phase": (act - 1) * ACT_PHASES + 1,
        "last_phase": min(act * ACT_PHASES, SEASON_1_PHASES),
    }
    for act in range(1, (SEASON_1_PHASES + ACT_PHASES - 1) // ACT_PHASES + 1)
)

CAMPAIGN_MAPS = (
    {
        "id": "ato1-terminal",
        "act": 1,
        "first_phase": 1,
        "last_phase": 3,
        "name": "Perímetro do Terminal de Vilar",
        "visual_index": 0,
    },
    {
        "id": "ato1-meriti",
        "act": 1,
        "first_phase": 4,
        "last_phase": 6,
        "name": "Setor das Ruínas de Meriti",
        "visual_index": 1,
    },
    {
        "id": "ato1-antena",
        "act": 1,
        "first_phase": 7,
        "last_phase": 10,
        "name": "Distrito da Antena",
        "visual_index": 2,
    },
    {
        "id": "ato2-setor-1",
        "act": 2,
        "first_phase": 11,
        "last_phase": 13,
        "name": "Ato 2 · Setor 1 (provisório)",
        "visual_index": 3,
    },
    {
        "id": "ato2-setor-2",
        "act": 2,
        "first_phase": 14,
        "last_phase": 16,
        "name": "Ato 2 · Setor 2 (provisório)",
        "visual_index": 4,
    },
    {
        "id": "ato2-setor-3",
        "act": 2,
        "first_phase": 17,
        "last_phase": 20,
        "name": "Ato 2 · Setor 3 (provisório)",
        "visual_index": 5,
    },
    {
        "id": "ato3-setor-1",
        "act": 3,
        "first_phase": 21,
        "last_phase": 23,
        "name": "Ato 3 · Setor 1 (provisório)",
        "visual_index": 6,
    },
    {
        "id": "ato3-setor-2",
        "act": 3,
        "first_phase": 24,
        "last_phase": 26,
        "name": "Ato 3 · Setor 2 (provisório)",
        "visual_index": 7,
    },
    {
        "id": "ato3-setor-3",
        "act": 3,
        "first_phase": 27,
        "last_phase": 30,
        "name": "Ato 3 · Setor 3 (provisório)",
        "visual_index": 8,
    },
)


def encounter_type(phase: int, wave: int) -> str:
    """Return the special encounter type for an act's final wave."""
    if wave != 10:
        return "common"
    if phase % ACT_PHASES == 0:
        return "boss"
    if phase % ACT_PHASES == ACT_PHASES // 2:
        return "miniboss"
    return "common"


def campaign_map_for_phase(phase: int) -> dict | None:
    """Return the approved map grouping for a Season 1 phase."""
    for campaign_map in CAMPAIGN_MAPS:
        if campaign_map["first_phase"] <= phase <= campaign_map["last_phase"]:
            return campaign_map
    return None


def season_act_for_phase(phase: int) -> int | None:
    """Return the act number for a Season 1 phase."""
    if not 1 <= phase <= SEASON_1_PHASES:
        return None
    return (phase - 1) // ACT_PHASES + 1
