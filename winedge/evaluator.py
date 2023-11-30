"""
Missing methods to determine the highest card in High Card rank class.
"""

import itertools
from .card import Card
from .lookup import LookupTable

class Evaluator(object):
    """
    Evaluate hand strengths. The first edition would focus on assessing the River round.
    """

    def __init__(self):

        self.table = LookupTable()

        self.hand_size_map = {
            5: self._flop,
            6: self._turn,
            7: self._river
        }

    def evaluate(self, cards, board):
        """
        The function to be called for getting the strength of a given hand. 

        Given the cards on deck, the function maps the scenario to specific evaluations.
        """

        all_cards = cards + board

        return self.hand_size_map[len(all_cards)](all_cards)

    def _flop(self, cards):
        """
        Fundamental evaluation function. It provides a rank in the range [1, 7462].
        """

        # check flush
        if cards[0] & cards[1] & cards[2] & cards[3] & cards[4] & 0xF000:
            handOR = (cards[0] | cards[1] | cards[2] | cards[3] | cards[4]) >> 16
            prime = Card.prime_product_from_rankbits(handOR)
            return self.table.flush_lookup[prime]

        # other patterns
        else:
            prime = Card.prime_product_from_hand(cards)
            return self.table.unsuited_lookup[prime]

    def _turn(self, cards):
        """
        Iterate all possible combinations of 5 cards from a 
        total of 6 cards and apply the five-card evaluation 
        on each combination. Then determine the best rank.
        """

        # set initial rank to be the lowest(unsuited 7-5-4-3-2), which
        # numerically is essentially the largest: 7462
        max_rank = LookupTable.MAX_HIGH_CARD

        allcombos = itertools.combinations(cards, 5)

        for combo in allcombos:

            score = self._flop(combo)
            if score < max_rank:
                # since the strength of a given hand is higher when the rank is smaller,
                # we should always return the smallest possible score.
                max_rank = score

        return max_rank

    def _river(self, cards):
        """
        Iterate all possible combinations of 5 cards from a 
        total of 7 cards and apply the five-card evaluation 
        on each combination. Then determine the best rank.
        """

        # set initial rank to be the lowest(unsuited 7-5-4-3-2),
        # which numerically is essentially the largest: 7462
        max_rank = LookupTable.MAX_HIGH_CARD

        allcombos = itertools.combinations(cards, 5)

        for combo in allcombos:

            score = self._flop(combo)
            if score < max_rank:
                # since the strength of a given hand is higher when the rank is smaller, we
                # should always return the smallest possible score.
                max_rank = score

        return max_rank

    def get_rank_class(self, hand_rank):
        """
        Returns the class of hand given the hand hand_rank
        returned from evaluate. 
        """
        if hand_rank >= 0 and hand_rank <= LookupTable.MAX_STRAIGHT_FLUSH:
            return LookupTable.MAX_TO_RANK_CLASS[LookupTable.MAX_STRAIGHT_FLUSH]
        elif hand_rank <= LookupTable.MAX_FOUR_OF_A_KIND:
            return LookupTable.MAX_TO_RANK_CLASS[LookupTable.MAX_FOUR_OF_A_KIND]
        elif hand_rank <= LookupTable.MAX_FULL_HOUSE:
            return LookupTable.MAX_TO_RANK_CLASS[LookupTable.MAX_FULL_HOUSE]
        elif hand_rank <= LookupTable.MAX_FLUSH:
            return LookupTable.MAX_TO_RANK_CLASS[LookupTable.MAX_FLUSH]
        elif hand_rank <= LookupTable.MAX_STRAIGHT:
            return LookupTable.MAX_TO_RANK_CLASS[LookupTable.MAX_STRAIGHT]
        elif hand_rank <= LookupTable.MAX_THREE_OF_A_KIND:
            return LookupTable.MAX_TO_RANK_CLASS[LookupTable.MAX_THREE_OF_A_KIND]
        elif hand_rank <= LookupTable.MAX_TWO_PAIR:
            return LookupTable.MAX_TO_RANK_CLASS[LookupTable.MAX_TWO_PAIR]
        elif hand_rank <= LookupTable.MAX_PAIR:
            return LookupTable.MAX_TO_RANK_CLASS[LookupTable.MAX_PAIR]
        elif hand_rank <= LookupTable.MAX_HIGH_CARD:
            return LookupTable.MAX_TO_RANK_CLASS[LookupTable.MAX_HIGH_CARD]
        else:
            raise ValueError("Inavlid hand rank, cannot return rank class")


    def class_to_string(self, class_int):
        """
        Converts the integer class hand score into names.
        """
        return LookupTable.RANK_CLASS_TO_STRING[class_int]

    def get_rank_percentage(self, hand_rank):
        """
        Normalize the hand rank score. From intergers ranging in [1, 7462]
        to floating numbers ranging from 0 to 1. The mapping is in such a 
        way that the given hand would have a value representing that 
        it is stronger than p of the total hand, with p being the percent 
        of hands weaker than the given hand.
        """
        return 1 - (float(hand_rank) / float(LookupTable.MAX_HIGH_CARD))
