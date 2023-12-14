"""
This is Card class, containing card information like ranks and suits.
The class is a 32-bit structure, storing info about rank, suit and prime number.

Also contains functions that map the card rank to prime numbers so each
rank is assigned with a unique prime number. This allows us to generate
unique identifiers, aka prime product, for different hands.
"""

class Card ():
    """
    Card class structure:
                          bitrank     suit rank   prime
                    +--------+--------+--------+--------+
                    |xxxbbbbb|bbbbbbbb|cdhsrrrr|xxpppppp|
                    +--------+--------+--------+--------+

        1) p = prime number of rank (refer to list PRIMES)
        2) r = rank of card
        3) cdhs = suit of card (bit turned on based on suit of card)
        4) b = bit turned on depending on rank of card
        5) x = unused
    """

    # initialize
    STR_RANKS = '23456789TJQKA'
    INT_RANKS = range(13)
    PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]

    # converstion from string => int
    CHAR_RANK_TO_INT_RANK = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, 
        '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 
        'K': 13, 'A': 14
    }
    CHAR_SUIT_TO_INT_SUIT = {
        's' : 1, # spade
        'h' : 2, # hearts
        'd' : 4, # diamonds
        'c' : 8, # clubs
    }
    INT_SUIT_TO_CHAR_SUIT = 'xshxdxxxc'


    @staticmethod
    def new(string):
        """
        Converts Card string to binary integer representation of card
        """

        rank_char = string[0]
        suit_char = string[1]
        rank_int = Card.CHAR_RANK_TO_INT_RANK[rank_char]
        suit_int = Card.CHAR_SUIT_TO_INT_SUIT[suit_char]
        rank_prime = Card.PRIMES[rank_int - 2]

        # perform bitwise shifts to generate unique card attributes
        bitrank = 1 << (rank_int - 2) << 16
        suit = suit_int << 12
        rank = rank_int << 8

        return bitrank | suit | rank | rank_prime

    @staticmethod
    def int_to_str(card_int):
        """
        Convert integer ranks to strings so human like us can comprehend
        """
        rank_int = Card.get_rank_int(card_int)
        suit_int = Card.get_suit_int(card_int)
        return Card.STR_RANKS[rank_int] + Card.INT_SUIT_TO_CHAR_SUIT[suit_int]

    @staticmethod
    def get_rank_int(card_int):
        """
        Get the 4-bit bin representing the rank from the 32-bit bin that stores all the info
        """
        return (card_int >> 8) & 0xF

    @staticmethod
    def get_suit_int(card_int):
        """
        Get the 4-bit bin representing the suit from the 32-bit bin that stores all the info
        """
        return (card_int >> 12) & 0xF

    @staticmethod
    def get_bitrank_int(card_int):
        """
        Get the 16-bit bin representing the bitrank from the 32-bit bin that stores all the info
        """
        return (card_int >> 16) & 0x1FFF

    @staticmethod
    def get_prime(card_int):
        """
        Get the 4-bit bin representing the prime number from the 32-bit bin that stores all the info
        """
        return card_int & 0x3F

    @staticmethod
    def hand_to_binary(card_strs):
        """
        Expects a list of cards as strings and returns a list
        of integers of same length corresponding to those strings. 
        """
        bhand = []
        for c in card_strs:
            bhand.append(Card.new(c))
        return bhand

    @staticmethod
    def prime_product_from_hand(card_ints):
        """
        Expects a list of cards in integer form. 
        """

        product = 1
        for c in card_ints:
            product *= (c & 0xFF)

        return product

    @staticmethod
    def prime_product_from_rankbits(rankbits):
        """
        Returns the prime product using the bitrank (b)
        bits of the hand. Each 1 in the sequence is converted
        to the correct prime and multiplied in.

        Params:
            rankbits = a single 32-bit (only 13-bits set) integer representing 
                    the ranks of 5 _different_ ranked cards 
                    (5 of 13 bits are set)

        Primarily used for evaulating flushes and straights, 
        two occasions where we know the ranks are *ALL* different.

        Assumes that the input is in form (set bits):

                              rankbits     
                        +--------+--------+
                        |xxxbbbbb|bbbbbbbb|
                        +--------+--------+

        """
        product = 1
        for i in Card.INT_RANKS:
            # if the ith bit is set
            if rankbits & (1 << i):
                product *= Card.PRIMES[i]

        return product
