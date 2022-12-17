from django.test import TestCase
from store.logic import operations

class LogicTestCase(TestCase):
    def test_plus(self):
        result = operations(6, 7, '+')
        self.assertEqual(13, result)

    def test_minus(self):
        result = operations(6, 7, '-')
        self.assertEqual(-1, result)

    def test_multiply(self):
        result = operations(6, 7, '*')
        self.assertEqual(42, result)