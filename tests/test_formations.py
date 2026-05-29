import unittest

from src.algorithms.formations import get_formation, interpolate_transition


class FormationTests(unittest.TestCase):
    def test_square_formation_has_expected_number_of_points(self) -> None:
        points = get_formation("square", count=5, spacing=2.0, altitude=3.0)
        self.assertEqual(len(points), 5)
        self.assertTrue(all(p[2] == 3.0 for p in points))

    def test_transition_interpolation_respects_target(self) -> None:
        start = [(0.0, 0.0, 3.0), (1.0, 0.0, 3.0)]
        end = [(2.0, 2.0, 4.0), (3.0, 2.0, 4.0)]
        frames = interpolate_transition(start, end, steps=2)
        self.assertEqual(frames[-1], end)
