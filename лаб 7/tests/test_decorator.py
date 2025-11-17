import unittest
import io
from logger_decorator import logger

class TestDecorator(unittest.TestCase):

    def setUp(self):
        self.stream = io.StringIO()

        @logger(handle=self.stream)
        def add_one(x):
            return x + 1

        self.fn = add_one

    def test_success_logging(self):
        result = self.fn(10)
        logs = self.stream.getvalue()

        self.assertIn("calling", logs)
        self.assertIn("finished", logs)
        self.assertEqual(result, 11)

    def test_error_logging(self):

        @logger(handle=self.stream)
        def fail():
            raise ValueError("bad")

        with self.assertRaises(ValueError):
            fail()

        logs = self.stream.getvalue()
        self.assertIn("ERROR", logs)
        self.assertIn("ValueError", logs)