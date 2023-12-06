import unittest

from winedge.evaluator import Evaluator
from winedge.lookup import LookupTable
from winedge.card import Card

class TestEvaluator(unittest.TestCase):
    """
    Create test environment
    """
    def setUp(self):
        # Initialize the Evaluator and LookupTable
        self.evaluator = Evaluator()
        self.table = LookupTable()

    def test_evaluate_hand(self):
        """
        Simple smoke test using a plain example
        """
        # Test a specific hand evaluation
        hand = [
            Card.new('2h'),
            Card.new('2s'),
            Card.new('5s'),
            Card.new('Jc'),
            Card.new('Ah')
        ]

        board = []
        result = self.evaluator.evaluate(hand, board)
        self.assertEqual(result, 5618)
        