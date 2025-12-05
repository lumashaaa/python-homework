import unittest
from models.user import User
from models.currency import Currency

class TestModels(unittest.TestCase):
    def test_user(self):
        u = User(1, "Alice")
        self.assertEqual(u.id, 1)
        self.assertEqual(u.name, "Alice")
        with self.assertRaises(ValueError):
            User(-1, "x")

    def test_currency(self):
        c = Currency("R000", 123, "USD", "Dollar", "75.5", 1)
        self.assertAlmostEqual(c.value, 75.5)
        self.assertEqual(c.char_code, "USD")
        with self.assertRaises(ValueError):
            Currency("", 0, "", "", "0", 0)

if __name__ == "__main__":
    unittest.main()
