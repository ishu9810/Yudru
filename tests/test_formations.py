import unittest

from src.algorithms.formations import named_formation_offsets


class TestFormations(unittest.TestCase):
    def test_square_returns_5_offsets(self):
        offsets = named_formation_offsets("SQUARE", 5)
        self.assertEqual(5, len(offsets))
        self.assertEqual((-10, -10, 0), offsets[0])

    def test_circle_returns_5_offsets(self):
        offsets = named_formation_offsets("CIRCLE", 5, 20)
        self.assertEqual(5, len(offsets))


if __name__ == "__main__":
    unittest.main()
