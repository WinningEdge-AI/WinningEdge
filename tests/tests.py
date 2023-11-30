import os
import unittest

from winedge import Card, Evaluator

class test(unittest.TestCase):

    def test_evaluator(self):
        """
        Testing whether the input of card is formatted correctly.

        """
        hand = ['2h', '5s', 'Jc', 'Kh', 'Ah']
        board = []
        result = self.evaluator.evaluate(hand, board)
        self.assertEqual(result, 33292) 
