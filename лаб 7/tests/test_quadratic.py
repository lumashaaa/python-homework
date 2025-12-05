import unittest
from quadratic import solve_quadratic

class TestQuadratic(unittest.TestCase):

    def test_two_roots(self):
        res = solve_quadratic(1, -3, 2)
        self.assertEqual(res, (2, 1))

    def test_type_error(self):
        with self.assertRaises(TypeError):
            solve_quadratic("abc", 2, 3)