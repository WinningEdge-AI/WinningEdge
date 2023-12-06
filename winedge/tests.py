"""
This module defines all of the unit tests for the WinningEdge software package and all it's modules.
The module contains testing classes for the poker evaluator function and GUI."
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
        The module should return a value of 5618 given the inputs (2h,2s,5s,Jc,Ah).
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

    def test_evaluate_nonCard_input(self):
        """
        This function tests if the evaluate function throws an error when inproperly
        formatted arguments are input into the function.
        """
    #def test_evaluate_
    