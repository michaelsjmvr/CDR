import unittest

from game_app.abilities import CLASS_BASE_SKILLS, keystone_talent_id
from game_app.cards import (
    CARD_CATALOG,
    CARD_EFFECTS,
    CARDS,
    card_modifiers,
    card_recommendation_score,
)
from game_app.combat import calculate_attack_damage, derived_combat_stats


class CardSystemTests(unittest.TestCase):
    def test_catalog_and_combat_effects_include_new_build_synergies(self):
        self.assertGreaterEqual(len(CARD_CATALOG), 30)
        self.assertEqual(set(CARDS), set(CARD_EFFECTS))
        modifiers = card_modifiers({
            "piercing_spark",
            "elemental_conduit",
            "mana_harvest",
            "healing_resonance",
        })
        self.assertEqual(modifiers["projectile_damage"], .08)
        self.assertEqual(modifiers["elemental_damage"], .08)
        self.assertEqual(modifiers["mana_on_kill"], .05)
        self.assertEqual(modifiers["skill_healing"], .20)

    def test_projectile_and_elemental_cards_increase_matching_skill_damage(self):
        scout = {
            "class_id": "wild_scout", "specialization_id": None, "level": 10,
            "strength": 0, "agility": 0, "vitality": 0, "energy": 0,
        }
        scout_skill = CLASS_BASE_SKILLS["wild_scout"]
        base_projectile_damage = calculate_attack_damage(
            derived_combat_stats(scout), scout_skill, "physical", None, 1, 1
        )
        improved_projectile_damage = calculate_attack_damage(
            derived_combat_stats(scout, {"piercing_spark"}),
            scout_skill, "physical", None, 1, 1,
        )
        self.assertGreater(improved_projectile_damage, base_projectile_damage)

        weaver = {
            "class_id": "ash_weaver", "specialization_id": None, "level": 10,
            "strength": 0, "agility": 0, "vitality": 0, "energy": 0,
        }
        weaver_skill = CLASS_BASE_SKILLS["ash_weaver"]
        base_elemental_damage = calculate_attack_damage(
            derived_combat_stats(weaver), weaver_skill,
            "magical", "fire", 1, 1,
        )
        improved_elemental_damage = calculate_attack_damage(
            derived_combat_stats(weaver, {"elemental_conduit"}),
            weaver_skill, "magical", "fire", 1, 1,
        )
        self.assertGreater(improved_elemental_damage, base_elemental_damage)

    def test_recommendations_account_for_signature_healing_and_passive_mana(self):
        healing_card = "healing_resonance"
        mana_card = "mana_harvest"
        necromancer_keystone = {
            keystone_talent_id("ash_weaver", "necromancer")
        }
        arcane_archer_keystone = {
            keystone_talent_id("wild_scout", "arcane_archer")
        }
        beast_master_keystone = {
            keystone_talent_id("wild_scout", "beast_master")
        }

        self.assertGreater(
            card_recommendation_score(
                healing_card, "ash_weaver",
                specialization_id="necromancer",
                purchased_talents=necromancer_keystone,
            ),
            card_recommendation_score(healing_card, "ash_weaver"),
        )
        self.assertGreater(
            card_recommendation_score(
                mana_card, "ash_weaver", specialization_id="necromancer"
            ),
            card_recommendation_score(mana_card, "ash_weaver"),
        )
        self.assertGreater(
            card_recommendation_score(
                "elemental_conduit", "wild_scout",
                specialization_id="arcane_archer",
                purchased_talents=arcane_archer_keystone,
            ),
            card_recommendation_score("elemental_conduit", "wild_scout"),
        )
        self.assertLess(
            card_recommendation_score(
                "piercing_spark", "wild_scout",
                specialization_id="beast_master",
                purchased_talents=beast_master_keystone,
            ),
            card_recommendation_score("piercing_spark", "wild_scout"),
        )


if __name__ == "__main__":
    unittest.main()
