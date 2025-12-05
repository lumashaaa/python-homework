import unittest
from currencies import get_currencies

class TestCurrencies(unittest.TestCase):

    def test_invalid_url(self):
        with self.assertRaises(ConnectionError):
            get_currencies(["USD"], url="https://invalid-url-example")

    def test_missing_currency(self):
        with self.assertRaises(KeyError):
            get_currencies(["LOL"], url="https://www.cbr-xml-daily.ru/daily_json.js")