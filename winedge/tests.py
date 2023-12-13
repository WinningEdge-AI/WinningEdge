"""
This module defines all the testing classes and methods for the WinningEdge
software package and all it's modules.

Classes:
--------------
- TestEvaluator(unittest.TestCase):
    Unit testing class for the evaluator.py module. Contains methods to unittest
    the evaluator.py module including hand evaluation and hand comparision
    one shot tests.

- TestCard(unittest.TestCase):
    Unit testing class for the card.py module. Contains methods to unittest the
    card.py module including a smoke test for card generation.


"""

import unittest

from .evaluator import Evaluator
from .lookup import LookupTable
from .card import Card

class TestEvaluator(unittest.TestCase):
    """
    This class defines methods for testing the evaluator module. It contains ... FINISH LATER
    """
    def setUp(self):
        """The setUp method initializes the Evaluator and LookupTable modules required for
        subsequent unittests defined in this class."""
        # Initialize the Evaluator and LookupTable
        self.evaluator = Evaluator()
        self.table = LookupTable()

    def test_evaluate_hand(self):
        """
        This method is a oneshot test of the evaluator and lookup table modules.
        The module should return a value of 5990 given the inputs (2h,2s,5s,Jc,Ah).
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
        self.assertEqual(result, 5990)

    def test_compare_hands(self):
        """
        This method is a oneshot test to see if the evaluator handles
        the comparison of two sets of hands appropriately.
        """
        board = [
            # Flop cards
            Card.new('Ac'),
            Card.new('Ah'),
            Card.new('8d'),
            # Turn card
            Card.new('7d'),
            # River card
            Card.new('Jh')
        ]

        hand1 = [
            Card.new('Ad'),
            Card.new('6h')
        ]

        hand2 = [
            Card.new('6c'),
            Card.new('Js')
        ]

        result1 = self.evaluator.evaluate(hand1, board)
        result2 = self.evaluator.evaluate(hand2, board)

        self.assertLess(result1, result2)

    #def test_evaluate_
class TestCard(unittest.TestCase):
    """
    This class defines methods for testing the card.py module... FINISH LATER
    """
    def new_card_smoke_test(self):
        """
        Smoke test to test if the Card.new() method generates a new card.
        """
        card = Card.new('Ah')
        self.assertIsNotNone(card)
