import unittest

from game_app.combat import enemy_spawn_positions
from game_app.map_geometry import terminal_vilar_collides


class TerminalVilarMapTests(unittest.TestCase):
    def test_phase_one_scenery_blocks_buses_and_pillars_but_keeps_spawn_clear(self):
        self.assertTrue(terminal_vilar_collides(245, 985, 13))
        self.assertTrue(terminal_vilar_collides(1370, 990, 13))
        self.assertFalse(terminal_vilar_collides(1200, 900, 13))

    def test_phase_one_enemy_spawns_avoid_static_scenery(self):
        positions = enemy_spawn_positions("terminal-vilar-phase-one", 10, phase=1)

        self.assertEqual(len(positions), 10)
        for x, y in positions:
            with self.subTest(position=(x, y)):
                self.assertFalse(terminal_vilar_collides(x, y, 28))
