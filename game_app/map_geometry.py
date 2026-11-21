"""Shared map geometry for server-side spawn validation and client rendering."""

import json
import math
import os
import re
import tempfile
from copy import deepcopy
from pathlib import Path


_MAP_CONFIG_PATH = Path(__file__).parent / "data" / "maps" / "terminal_vilar_fase1.json"
_WORLD = {"width": 2400, "height": 1800}
_DEFAULT_PLAYER_BOUNDS = {
    "min_x": 130, "max_x": 2270, "min_y": 130, "max_y": 1670,
}


def _finite_number(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"O valor de {name} deve ser um número finito.")
    try:
        is_finite = math.isfinite(value)
    except OverflowError as error:
        raise ValueError(f"O valor de {name} deve ser um número finito.") from error
    if not is_finite:
        raise ValueError(f"O valor de {name} deve ser um número finito.")
    return value


def _validate_bounds(bounds, name, world):
    expected = {"min_x", "max_x", "min_y", "max_y"}
    if not isinstance(bounds, dict) or set(bounds) != expected:
        raise ValueError(f"Os limites de {name} estão incompletos.")
    result = {
        key: _finite_number(bounds[key], f"{name}.{key}")
        for key in expected
    }
    if (
        result["min_x"] < 0
        or result["min_y"] < 0
        or result["max_x"] > world["width"]
        or result["max_y"] > world["height"]
        or result["min_x"] >= result["max_x"]
        or result["min_y"] >= result["max_y"]
    ):
        raise ValueError(f"Os limites de {name} precisam ficar dentro do mundo.")
    return result


def _validate_points(points, name, minimum_count):
    if not isinstance(points, list) or not minimum_count <= len(points) <= 256:
        raise ValueError(f"A geometria {name} deve conter de {minimum_count} a 256 pontos.")
    normalized = []
    for index, point in enumerate(points):
        if not isinstance(point, list) or len(point) != 2:
            raise ValueError(f"Cada ponto de {name} deve conter coordenadas X e Y.")
        x = _finite_number(point[0], f"{name}[{index}].x")
        y = _finite_number(point[1], f"{name}[{index}].y")
        if not -_WORLD["width"] <= x <= _WORLD["width"] * 2:
            raise ValueError(f"A coordenada X de {name} está fora do limite permitido.")
        if not -_WORLD["height"] <= y <= _WORLD["height"] * 2:
            raise ValueError(f"A coordenada Y de {name} está fora do limite permitido.")
        normalized.append([x, y])
    return normalized


def _validate_geometry_id(value, name, seen_ids):
    if (
        not isinstance(value, str)
        or len(value) > 64
        or re.fullmatch(r"[a-z0-9][a-z0-9_-]*", value) is None
        or value in seen_ids
    ):
        raise ValueError(f"O ID de {name} deve ser único e usar letras minúsculas, números, hífen ou sublinhado.")
    seen_ids.add(value)
    return value


def _validate_map_config(config):
    required = {
        "map_id", "world", "player_bounds", "spawn_bounds", "colliders",
        "solid_polygons", "collision_walls", "wall_thickness",
    }
    if not isinstance(config, dict) or set(config) != required:
        raise ValueError("A configuração do mapa tem campos ausentes ou inesperados.")
    if config["map_id"] != "fase_01_terminal_vilar":
        raise ValueError("Identificador de mapa inválido.")
    if config["world"] != _WORLD:
        raise ValueError("O tamanho-base do mundo da Fase 1 é fixo em 2.400 × 1.800.")

    player_bounds = _validate_bounds(config["player_bounds"], "movimento", _WORLD)
    spawn_bounds = _validate_bounds(config["spawn_bounds"], "spawn", _WORLD)
    if not (
        player_bounds["min_x"] <= 1200 <= player_bounds["max_x"]
        and player_bounds["min_y"] <= 900 <= player_bounds["max_y"]
    ):
        raise ValueError("O limite de movimento precisa incluir o ponto inicial (1.200, 900).")
    if (
        spawn_bounds["min_x"] < player_bounds["min_x"]
        or spawn_bounds["max_x"] > player_bounds["max_x"]
        or spawn_bounds["min_y"] < player_bounds["min_y"]
        or spawn_bounds["max_y"] > player_bounds["max_y"]
    ):
        raise ValueError("A área de spawn deve ficar dentro dos limites de movimento.")
    if (
        math.ceil(spawn_bounds["min_x"]) > math.floor(spawn_bounds["max_x"])
        or math.ceil(spawn_bounds["min_y"]) > math.floor(spawn_bounds["max_y"])
    ):
        raise ValueError("A área de spawn precisa conter ao menos uma coordenada inteira em cada eixo.")

    colliders = config["colliders"]
    if not isinstance(colliders, list) or len(colliders) > 100:
        raise ValueError("A lista deve conter de 0 a 100 colisores.")
    normalized_colliders = []
    seen_ids = set()
    collider_keys = {"id", "x", "y", "width", "height", "angle"}
    for collider in colliders:
        if not isinstance(collider, dict) or set(collider) != collider_keys:
            raise ValueError("Cada colisor deve conter id, x, y, width, height e angle.")
        collider_id = _validate_geometry_id(collider["id"], "colisores", seen_ids)
        normalized = {"id": collider_id}
        for key in ("x", "y", "width", "height", "angle"):
            normalized[key] = _finite_number(collider[key], f"{collider_id}.{key}")
        if (
            normalized["width"] <= 0
            or normalized["height"] <= 0
            or normalized["width"] > _WORLD["width"] * 2
            or normalized["height"] > _WORLD["height"] * 2
            or not -math.pi <= normalized["angle"] <= math.pi
        ):
            raise ValueError(f"As dimensões ou a rotação do colisor {collider_id} são inválidas.")
        if not -_WORLD["width"] <= normalized["x"] <= _WORLD["width"] * 2:
            raise ValueError(f"A coordenada X do colisor {collider_id} está fora do limite permitido.")
        if not -_WORLD["height"] <= normalized["y"] <= _WORLD["height"] * 2:
            raise ValueError(f"A coordenada Y do colisor {collider_id} está fora do limite permitido.")
        normalized_colliders.append(normalized)

    solid_polygons = config["solid_polygons"]
    if not isinstance(solid_polygons, list) or len(solid_polygons) > 100:
        raise ValueError("A lista de polígonos sólidos deve conter de 0 a 100 formas.")
    normalized_polygons = []
    for polygon in solid_polygons:
        if not isinstance(polygon, dict) or set(polygon) != {"id", "points"}:
            raise ValueError("Cada polígono sólido deve conter id e points.")
        polygon_id = _validate_geometry_id(polygon["id"], "polígonos sólidos", seen_ids)
        normalized_polygons.append({
            "id": polygon_id,
            "points": _validate_points(polygon["points"], polygon_id, 3),
        })

    collision_walls = config["collision_walls"]
    if not isinstance(collision_walls, list) or len(collision_walls) > 100:
        raise ValueError("A lista de paredes deve conter de 0 a 100 formas.")
    normalized_walls = []
    for wall in collision_walls:
        if not isinstance(wall, dict) or set(wall) != {"id", "points"}:
            raise ValueError("Cada parede deve conter id e points.")
        wall_id = _validate_geometry_id(wall["id"], "paredes", seen_ids)
        normalized_walls.append({
            "id": wall_id,
            "points": _validate_points(wall["points"], wall_id, 2),
        })

    wall_thickness = _finite_number(config["wall_thickness"], "wall_thickness")
    if not 0 <= wall_thickness <= 100:
        raise ValueError("A espessura das paredes deve estar entre 0 e 100.")

    return {
        "map_id": "fase_01_terminal_vilar",
        "world": dict(_WORLD),
        "player_bounds": player_bounds,
        "spawn_bounds": spawn_bounds,
        "colliders": normalized_colliders,
        "solid_polygons": normalized_polygons,
        "collision_walls": normalized_walls,
        "wall_thickness": wall_thickness,
    }


def _read_map_config():
    with _MAP_CONFIG_PATH.open(encoding="utf-8") as config_file:
        return _validate_map_config(json.load(config_file))


TERMINAL_VILAR_MAP_CONFIG = _read_map_config()
TERMINAL_VILAR_COLLIDERS = TERMINAL_VILAR_MAP_CONFIG["colliders"]


def terminal_vilar_map_config():
    """Return a detached copy of the active Phase 1 map configuration."""
    return deepcopy(TERMINAL_VILAR_MAP_CONFIG)


def save_terminal_vilar_map_config(config):
    """Validate and atomically persist Phase 1 colliders and gameplay bounds."""
    normalized = _validate_map_config(config)
    _MAP_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = None
    try:
        descriptor, temporary_name = tempfile.mkstemp(
            prefix="terminal_vilar_fase1_", suffix=".tmp",
            dir=_MAP_CONFIG_PATH.parent,
        )
        temporary_path = Path(temporary_name)
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as config_file:
            json.dump(normalized, config_file, ensure_ascii=False, indent=2)
            config_file.write("\n")
            config_file.flush()
            os.fsync(config_file.fileno())
        os.replace(temporary_path, _MAP_CONFIG_PATH)
        temporary_path = None
    finally:
        if temporary_path is not None:
            try:
                temporary_path.unlink()
            except FileNotFoundError:
                pass

    global TERMINAL_VILAR_MAP_CONFIG, TERMINAL_VILAR_COLLIDERS
    TERMINAL_VILAR_MAP_CONFIG = normalized
    TERMINAL_VILAR_COLLIDERS = normalized["colliders"]
    return terminal_vilar_map_config()


def clamp_map_position(x, y, phase):
    """Clamp a world position to its phase bounds without changing other maps."""
    bounds = (
        TERMINAL_VILAR_MAP_CONFIG["player_bounds"]
        if phase == 1
        else _DEFAULT_PLAYER_BOUNDS
    )
    return (
        min(bounds["max_x"], max(bounds["min_x"], x)),
        min(bounds["max_y"], max(bounds["min_y"], y)),
    )


def terminal_vilar_collides(x: float, y: float, radius: float) -> bool:
    """Return whether a circle overlaps solid scenery in Phase 1."""
    if radius < 0:
        raise ValueError("O raio de colisão não pode ser negativo.")

    config = TERMINAL_VILAR_MAP_CONFIG
    for collider in config["colliders"]:
        cosine = math.cos(collider["angle"])
        sine = math.sin(collider["angle"])
        offset_x = x - collider["x"]
        offset_y = y - collider["y"]
        local_x = offset_x * cosine + offset_y * sine
        local_y = -offset_x * sine + offset_y * cosine
        nearest_x = max(-collider["width"] / 2, min(local_x, collider["width"] / 2))
        nearest_y = max(-collider["height"] / 2, min(local_y, collider["height"] / 2))
        distance_x = local_x - nearest_x
        distance_y = local_y - nearest_y
        if distance_x * distance_x + distance_y * distance_y <= radius * radius:
            return True

    for polygon in config["solid_polygons"]:
        points = polygon["points"]
        inside = False
        for index, point in enumerate(points):
            previous = points[index - 1]
            if ((point[1] > y) != (previous[1] > y)) and (
                x < (previous[0] - point[0]) * (y - point[1])
                / (previous[1] - point[1]) + point[0]
            ):
                inside = not inside
        if inside:
            return True
        for index, point in enumerate(points):
            next_point = points[(index + 1) % len(points)]
            if _distance_to_segment_squared(
                x, y, point[0], point[1], next_point[0], next_point[1]
            ) <= radius * radius:
                return True

    wall_radius = radius + config["wall_thickness"]
    for wall in config["collision_walls"]:
        for index, point in enumerate(wall["points"][:-1]):
            next_point = wall["points"][index + 1]
            if _distance_to_segment_squared(
                x, y, point[0], point[1], next_point[0], next_point[1]
            ) <= wall_radius * wall_radius:
                return True
    return False


def _distance_to_segment_squared(px, py, ax, ay, bx, by):
    dx = bx - ax
    dy = by - ay
    length_squared = dx * dx + dy * dy
    if length_squared == 0:
        return (px - ax) ** 2 + (py - ay) ** 2
    amount = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / length_squared))
    nearest_x = ax + amount * dx
    nearest_y = ay + amount * dy
    return (px - nearest_x) ** 2 + (py - nearest_y) ** 2


def terminal_vilar_collision_data():
    """Return JSON-ready collision proxies for the Phase 1 client and preview."""
    return [dict(collider) for collider in TERMINAL_VILAR_COLLIDERS]
