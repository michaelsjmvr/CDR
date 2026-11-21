import sqlite3
import unittest
from contextlib import closing

from game_app.combat import (
    calculate_attack_damage,
    derived_combat_stats,
    enemy_level,
    enemy_max_health,
    scale_enemy_attack_damage,
)
from game_app.campaign import (
    CAMPAIGN_MAPS,
    SEASON_1_ACTS,
    SEASON_1_PHASES,
    campaign_map_for_phase,
    encounter_type,
    season_act_for_phase,
)
from game_app.classes import CLASSES
from game_app.progression import (
    MAX_LEVEL,
    add_experience,
    award_legacy_points,
    enemies_in_wave,
    enemy_experience_reward,
    experience_needed,
    legacy_milestones_crossed,
    legacy_points_for_level,
    phase_xp_budget_for_level,
    WAVES_PER_PHASE,
)
from game_app.talents import CLASS_SPECIALIZATIONS, RADIAL_GRAPHS
from scripts.simulate_balance_model import (
    checkpoint_arenas,
    current_xp_projection,
    wave_entry_levels,
)
from scripts.simulate_live_balance import (
    DAMAGE_SPECIALIZATIONS,
    automatic_attributes_at_level,
    estimate_live_wave_survival,
    simulate_live_rotation,
)


class ProgressionTests(unittest.TestCase):
    def test_visible_class_names_preserve_internal_class_ids(self):
        self.assertEqual(
            {class_id: info["name"] for class_id, info in CLASSES.items()},
            {
                "guardian": "Guerreiro",
                "ash_weaver": "Tecelão",
                "rune_blade": "Lâmina Arcana",
                "wild_scout": "Caçador",
            },
        )

    def test_legacy_points_at_progression_milestones(self):
        expected = {
            1: 0,
            10: 1,
            25: 3,
            49: 5,
            50: 8,
            100: 16,
            400: 64,
        }
        for level, points in expected.items():
            with self.subTest(level=level):
                self.assertEqual(legacy_points_for_level(level), points)

    def test_legacy_milestones_crossed_without_duplicate_awards(self):
        self.assertEqual(legacy_milestones_crossed(49, 50), 1)
        self.assertEqual(legacy_milestones_crossed(50, 100), 1)
        self.assertEqual(legacy_milestones_crossed(100, 100), 0)
        self.assertEqual(legacy_milestones_crossed(100, 50), 0)

    def test_legacy_points_are_persisted_once_as_levels_are_gained(self):
        with closing(sqlite3.connect(":memory:")) as db:
            db.execute(
                "CREATE TABLE characters (id INTEGER PRIMARY KEY, legacy_points INTEGER)"
            )
            db.execute(
                "INSERT INTO characters (id, legacy_points) VALUES (?, ?)", (1, 0)
            )

            first_award = award_legacy_points(db, 1, 1, 50)
            repeat_award = award_legacy_points(db, 1, 50, 50)
            final_award = award_legacy_points(db, 1, 50, 400)
            balance = db.execute(
                "SELECT legacy_points FROM characters WHERE id = ?", (1,)
            ).fetchone()[0]

        self.assertEqual(first_award, (8, 1))
        self.assertEqual(repeat_award, (0, 0))
        self.assertEqual(final_award, (56, 7))
        self.assertEqual(balance, 64)

    def test_experience_carries_across_levels_and_stops_at_cap(self):
        reward = sum(experience_needed(level) for level in range(1, 4))
        self.assertEqual(add_experience(1, 0, reward), (4, 0, 3))
        self.assertEqual(
            add_experience(MAX_LEVEL - 1, 0, 10**9),
            (MAX_LEVEL, 0, 1),
        )

    def test_phase_xp_is_fully_shared_by_actual_enemy_count(self):
        for phase in (1, 5, 80):
            budget = phase_xp_budget_for_level(100)
            earned = sum(
                enemy_experience_reward(phase, wave, enemy_index, budget)
                for wave in range(1, WAVES_PER_PHASE + 1)
                for enemy_index in range(enemies_in_wave(wave, phase))
            )
            with self.subTest(phase=phase):
                self.assertEqual(earned, budget)

    def test_future_xp_projection_reaches_level_cap_at_expected_phase_and_kills(self):
        self.assertEqual(current_xp_projection(), (69, 6502))

    def test_enemy_density_increases_by_phase(self):
        self.assertEqual(enemies_in_wave(1, 1), 3)
        self.assertEqual(enemies_in_wave(1, 5), 4)
        self.assertEqual(enemies_in_wave(9, 5), 12)
        self.assertEqual(enemies_in_wave(10, 5), 1)

    def test_season_one_covers_nine_maps_and_thirty_phases(self):
        self.assertEqual(
            [
                (act["number"], act["first_phase"], act["last_phase"])
                for act in SEASON_1_ACTS
            ],
            [(1, 1, 10), (2, 11, 20), (3, 21, 30)],
        )
        self.assertEqual(len(CAMPAIGN_MAPS), 9)
        self.assertEqual(CAMPAIGN_MAPS[0]["first_phase"], 1)
        self.assertEqual(CAMPAIGN_MAPS[-1]["last_phase"], SEASON_1_PHASES)
        for campaign_map, next_map in zip(CAMPAIGN_MAPS, CAMPAIGN_MAPS[1:]):
            self.assertEqual(campaign_map["last_phase"] + 1, next_map["first_phase"])
        self.assertEqual(campaign_map_for_phase(1)["id"], "ato1-terminal")
        self.assertEqual(campaign_map_for_phase(30)["id"], "ato3-setor-3")
        self.assertIsNone(campaign_map_for_phase(31))
        self.assertEqual(season_act_for_phase(1), 1)
        self.assertEqual(season_act_for_phase(20), 2)
        self.assertEqual(season_act_for_phase(30), 3)

    def test_special_encounters_only_appear_at_campaign_milestones(self):
        self.assertEqual(encounter_type(1, 10), "common")
        self.assertEqual(encounter_type(5, 9), "common")
        self.assertEqual(encounter_type(5, 10), "miniboss")
        self.assertEqual(encounter_type(15, 10), "miniboss")
        self.assertEqual(encounter_type(25, 10), "miniboss")
        self.assertEqual(encounter_type(10, 10), "boss")
        self.assertEqual(encounter_type(20, 10), "boss")
        self.assertEqual(encounter_type(30, 10), "boss")
        self.assertEqual(encounter_type(70, 10), "boss")

    def test_season_one_progression_ends_near_level_170_and_26_legacy_points(self):
        level, experience = 1, 0
        for phase in range(1, SEASON_1_PHASES + 1):
            budget = phase_xp_budget_for_level(level)
            for wave in range(1, WAVES_PER_PHASE + 1):
                for enemy_index in range(enemies_in_wave(wave, phase)):
                    reward = enemy_experience_reward(
                        phase, wave, enemy_index, budget
                    )
                    level, experience, _ = add_experience(
                        level, experience, reward
                    )
        self.assertEqual(level, 170)
        self.assertEqual(legacy_points_for_level(level), 26)


class EnemyCurveTests(unittest.TestCase):
    def test_difficulty_profiles_scale_enemy_health_damage_and_common_density(self):
        expected = (
            ("risk_low", (218, 25), (2564, 44), (11671, 60), 3),
            ("risk_moderate", (262, 31), (3077, 55), (14005, 75), 4),
            ("risk_high", (382, 45), (4487, 79), (20424, 108), 3),
            ("risk_extreme", (523, 62), (6154, 110), (28010, 150), 3),
        )
        for difficulty, common, miniboss, boss, enemy_count in expected:
            with self.subTest(difficulty=difficulty):
                self.assertEqual(
                    enemy_max_health(1, 1, difficulty=difficulty),
                    common[0],
                )
                self.assertEqual(
                    scale_enemy_attack_damage(25, 1, 1, difficulty=difficulty),
                    common[1],
                )
                self.assertEqual(
                    enemy_max_health(5, 10, difficulty=difficulty),
                    miniboss[0],
                )
                self.assertEqual(
                    scale_enemy_attack_damage(25, 5, 10, difficulty=difficulty),
                    miniboss[1],
                )
                self.assertEqual(
                    enemy_max_health(10, 10, difficulty=difficulty),
                    boss[0],
                )
                self.assertEqual(
                    scale_enemy_attack_damage(25, 10, 10, difficulty=difficulty),
                    boss[1],
                )
                self.assertEqual(enemies_in_wave(1, 1, difficulty), enemy_count)
                self.assertEqual(enemies_in_wave(10, 5, difficulty), 1)

    def test_common_enemy_curve_at_progression_checkpoints(self):
        checkpoints = (
            (1, 1, 6, 218, 25),
            (19, 5, 100, 1600, 86),
            (43, 5, 220, 3747, 164),
            (79, 5, 400, 7770, 281),
        )
        for phase, wave, expected_level, expected_health, expected_damage in checkpoints:
            with self.subTest(enemy_level=expected_level):
                self.assertEqual(enemy_level(phase, wave), expected_level)
                self.assertEqual(enemy_max_health(phase, wave), expected_health)
                self.assertEqual(
                    scale_enemy_attack_damage(25, phase, wave),
                    expected_damage,
                )

    def test_enemy_level_health_and_damage_stop_at_level_cap(self):
        self.assertEqual(enemy_level(79, 5), MAX_LEVEL)
        self.assertEqual(enemy_level(100, 5), MAX_LEVEL)
        self.assertEqual(enemy_max_health(79, 5), enemy_max_health(100, 5))
        self.assertEqual(
            scale_enemy_attack_damage(25, 79, 5),
            scale_enemy_attack_damage(25, 100, 5),
        )

    def test_enemy_health_increases_before_cap(self):
        self.assertGreater(enemy_max_health(20, 1), enemy_max_health(1, 1))
        self.assertGreater(
            scale_enemy_attack_damage(25, 20, 1),
            scale_enemy_attack_damage(25, 1, 1),
        )


class LiveBalanceCalibrationTests(unittest.TestCase):
    def test_starting_characters_survive_six_to_ten_common_hits(self):
        enemy_damage = scale_enemy_attack_damage(25, 1, 1)
        for class_id in CLASSES:
            attributes = automatic_attributes_at_level(class_id, 1)
            stats = derived_combat_stats(
                {"class_id": class_id, "level": 1, **attributes}
            )
            hits_to_die = stats["max_health"] / enemy_damage
            with self.subTest(class_id=class_id):
                self.assertGreaterEqual(hits_to_die, 6)
                self.assertLessEqual(hits_to_die, 10)

    def test_live_common_and_miniboss_rotations_match_approved_targets(self):
        arenas = checkpoint_arenas()
        entries = wave_entry_levels()
        for checkpoint in (1, 100, 220, 400):
            phase, _ = arenas[checkpoint]
            common_wave = 1 if checkpoint == 1 else 8
            for class_id in CLASSES:
                level = 1 if checkpoint == 1 else entries[(phase, common_wave)]
                specialization = (
                    DAMAGE_SPECIALIZATIONS[class_id] if level >= 100 else None
                )
                result = simulate_live_rotation(
                    class_id, level, phase, common_wave, specialization
                )
                with self.subTest(
                    checkpoint=checkpoint, class_id=class_id, target="Comum"
                ):
                    self.assertGreaterEqual(result["seconds"], 3)
                    self.assertLessEqual(result["seconds"], 6)

        for phase in (5, 15, 25):
            level = entries[(phase, WAVES_PER_PHASE)]
            for class_id in CLASSES:
                specialization = (
                    DAMAGE_SPECIALIZATIONS[class_id] if level >= 100 else None
                )
                result = simulate_live_rotation(
                    class_id, level, phase, WAVES_PER_PHASE, specialization
                )
                with self.subTest(phase=phase, class_id=class_id, target="Semichefe"):
                    self.assertGreaterEqual(result["seconds"], 18)
                    self.assertLessEqual(result["seconds"], 35)

    def test_live_boss_rotations_match_targets_with_resistance_counterplay(self):
        entries = wave_entry_levels()
        for phase in (10, 20, 30, 80):
            level = entries[(phase, WAVES_PER_PHASE)]
            for class_id in CLASSES:
                specialization = (
                    DAMAGE_SPECIALIZATIONS[class_id] if level >= 100 else None
                )
                result = simulate_live_rotation(
                    class_id, level, phase, WAVES_PER_PHASE, specialization
                )
                with self.subTest(phase=phase, class_id=class_id):
                    self.assertGreaterEqual(result["seconds"], 60)
                    self.assertLessEqual(result["seconds"], 120)

    def test_full_level_400_talent_paths_fit_budget_and_boss_targets(self):
        legacy_points = legacy_points_for_level(MAX_LEVEL)
        for class_id, specializations in CLASS_SPECIALIZATIONS.items():
            graph = RADIAL_GRAPHS[class_id]
            for specialization in specializations:
                nodes = [
                    node for node in graph["nodes"]
                    if node.get("specialization_id") == specialization["id"]
                    and node["category"] != "starting"
                ]
                path_cost = sum(node["cost"] for node in nodes)
                purchased_talents = tuple(node["id"] for node in nodes)
                result = simulate_live_rotation(
                    class_id,
                    MAX_LEVEL,
                    80,
                    WAVES_PER_PHASE,
                    specialization["id"],
                    purchased_talents,
                )
                with self.subTest(class_id=class_id, path=specialization["id"]):
                    self.assertGreater(path_cost, 0)
                    self.assertLessEqual(path_cost, legacy_points)
                    self.assertGreaterEqual(result["seconds"], 60)
                    self.assertLessEqual(result["seconds"], 120)

    def test_matching_elemental_resistance_creates_boss_counterplay(self):
        attributes = automatic_attributes_at_level("ash_weaver", MAX_LEVEL)
        stats = derived_combat_stats({
            "class_id": "ash_weaver", "level": MAX_LEVEL, **attributes
        })
        fire_skill = {
            "id": "test-fire",
            "damage_multiplier": 1.55,
            "projectile": True,
        }
        matched = calculate_attack_damage(
            stats, fire_skill, "magical", "fire", 10, WAVES_PER_PHASE
        )
        unmatched = calculate_attack_damage(
            stats, fire_skill, "magical", "fire", 20, WAVES_PER_PHASE
        )
        self.assertLess(matched, unmatched)

    def test_live_horde_pressure_simulation_is_repeatable(self):
        phase, _ = checkpoint_arenas()[100]
        level = wave_entry_levels()[(phase, 8)]
        first = estimate_live_wave_survival(
            "guardian", level, phase, 8, hit_rate=0.5, specialization_id="berserker"
        )
        second = estimate_live_wave_survival(
            "guardian", level, phase, 8, hit_rate=0.5, specialization_id="berserker"
        )
        self.assertEqual(first, second)
        self.assertEqual(first["enemy_count"], enemies_in_wave(8, phase))
        self.assertGreater(first["wave_seconds"], 0)

    def test_stationary_horde_scenario_requires_active_dodging(self):
        arenas = checkpoint_arenas()
        entries = wave_entry_levels()
        for checkpoint in (1, 100, 220, 400):
            phase, _ = arenas[checkpoint]
            level = entries[(phase, 8)]
            for class_id in CLASSES:
                specialization = (
                    DAMAGE_SPECIALIZATIONS[class_id] if level >= 100 else None
                )
                result = estimate_live_wave_survival(
                    class_id,
                    level,
                    phase,
                    8,
                    hit_rate=0.5,
                    specialization_id=specialization,
                )
                with self.subTest(checkpoint=checkpoint, class_id=class_id):
                    self.assertLess(result["remaining_health"], 0)
                    self.assertLess(result["survivable_hit_rate"], 0.1)


if __name__ == "__main__":
    unittest.main()
