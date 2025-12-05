import unittest
from utils.currencies_api import _parse_value_text

class TestAPI(unittest.TestCase):
    def test_parse_value(self):
        self.assertEqual(_parse_value_text("48,6178"), 48.6178)
        self.assertEqual(_parse_value_text("10.5"), 10.5)

if __name__ == "__main__":
    unittest.main()
