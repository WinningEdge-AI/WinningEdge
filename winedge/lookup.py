import itertools
from .card import Card

class LookupTable(object):
    """
    Number of Distinct Hand Values:

    Straight Flush   10 
    Four of a Kind   156      [(13 choose 2) * (2 choose 1)]
    Full Houses      156      [(13 choose 2) * (2 choose 1)]
    Flush            1277     [(13 choose 5) - 10 straight flushes]
    Straight         10 
    Three of a Kind  858      [(13 choose 3) * (3 choose 1)]
    Two Pair         858      [(13 choose 3) * (3 choose 2)]
    One Pair         2860     [(13 choose 4) * (4 choose 1)]
    High Card      + 1277     [(13 choose 5) - 10 straights]
    -------------------------
    TOTAL            7462

    Here we create a lookup table which maps:
        5 card hand's unique prime product => rank in range [1, 7462]

    Examples:
    * Royal flush (best hand possible)          => 1
    * 7-5-4-3-2 unsuited (worst hand possible)  => 7462
    """
    MAX_STRAIGHT_FLUSH = 10
    MAX_FOUR_OF_A_KIND = 166
    MAX_FULL_HOUSE = 322
    MAX_FLUSH = 1599
    MAX_STRAIGHT = 1609
    MAX_THREE_OF_A_KIND = 2467
    MAX_TWO_PAIR = 3325
    MAX_PAIR = 6185
    MAX_HIGH_CARD = 7462

    MAX_TO_RANK_CLASS = {
        MAX_STRAIGHT_FLUSH: 1,
        MAX_FOUR_OF_A_KIND: 2,
        MAX_FULL_HOUSE: 3,
        MAX_FLUSH: 4,
        MAX_STRAIGHT: 5,
        MAX_THREE_OF_A_KIND: 6,
        MAX_TWO_PAIR: 7,
        MAX_PAIR: 8,
        MAX_HIGH_CARD: 9
    }

    RANK_CLASS_TO_STRING = {
        1: "Straight Flush",
        2: "Four of a Kind",
        3: "Full House",
        4: "Flush",
        5: "Straight",
        6: "Three of a Kind",
        7: "Two Pair",
        8: "Pair",
        9: "High Card"
    }

    def __init__(self):
        """
        Calculates lookup tables
        """
        # create dictionaries
        self.flush_lookup = {}
        self.unsuited_lookup = {}

        # create the lookup table in a piecewise fashion
        self.flushes()
        self.multiples()

    def prime_product_from_rankbits(self, bits):
        """
        Calculate prime product from rank bits
        """
        prime_product = 1
        rank = 0

        while bits:
            if bits & 1:
                prime_product *= Card.PRIMES[rank]
            bits >>= 1
            rank += 1

        return prime_product

    def flushes(self):
        """
        Straight flushes and flushes.

        Lookup is done on a 13-bit integer (2^13 > 7462):
        xxxbbbbb bbbbbbbb => integer hand index
        """

        # straight flushes in rank order
        straight_flushes = [
            7936, 3968, 1984, 992, 496, 248, 124, 62, 31, 4111
        ]

        # now, we'll dynamically generate all the other flushes (including straight flushes)
        flushes = []
        gen = self.get_lexicographically_next_bit_sequence(int('0b11111', 2))

        for i in range(1277 + len(straight_flushes) - 1):
            f = next(gen)

            not_sf = all(f ^ sf for sf in straight_flushes)
            if not_sf:
                flushes.append(f)

        flushes.reverse()

        rank = 1
        for sf in straight_flushes:
            prime_product = self.prime_product_from_rankbits(sf)
            self.flush_lookup[prime_product] = rank
            rank += 1

        rank = self.MAX_FULL_HOUSE + 1
        for f in flushes:
            prime_product = self.prime_product_from_rankbits(f)
            self.flush_lookup[prime_product] = rank
            rank += 1

        self.straight_and_highcards(straight_flushes, flushes)

    def straight_and_highcards(self, straights, highcards):
        """
        Unique five card sets. Straights and high cards.

        Reuses bit sequences from flush calculations.
        """
        rank = self.MAX_FLUSH + 1

        for s in straights:
            prime_product = self.prime_product_from_rankbits(s)
            self.unsuited_lookup[prime_product] = rank
            rank += 1

        rank = self.MAX_PAIR + 1
        for h in highcards:
            prime_product = self.prime_product_from_rankbits(h)
            self.unsuited_lookup[prime_product] = rank
            rank += 1

    def multiples(self):
        """
        Pair, Two Pair, Three of a Kind, Full House, and 4 of a Kind.
        """
        backwards_ranks = range(len(range(2, 15)) - 1, -1, -1)

        # 1) Four of a Kind
        rank = self.MAX_STRAIGHT_FLUSH + 1

        # for each choice of a set of four rank
        for i in backwards_ranks:

            # and for each possible kicker rank
            kickers = list(backwards_ranks[:])
            kickers.remove(i)
            for k in kickers:
                product = (Card.PRIMES[i - 2]) ** 4 * (Card.PRIMES[k - 2])
                self.unsuited_lookup[product] = rank
                rank += 1

        # 2) Full House
        rank = self.MAX_FOUR_OF_A_KIND + 1

        # for each three of a kind
        for i in backwards_ranks:

            # and for each choice of pair rank
            pairranks = list(backwards_ranks[:])
            pairranks.remove(i)
            for pr in pairranks:
                product = (Card.PRIMES[i - 2]) ** 3 * (Card.PRIMES[pr - 2]) ** 2
                self.unsuited_lookup[product] = rank
                rank += 1

        # 3) Three of a Kind
        rank = self.MAX_STRAIGHT + 1

        # pick three of one rank
        for r in backwards_ranks:

            kickers = list(backwards_ranks[:])
            kickers.remove(r)
            gen = itertools.combinations(kickers, 2)

            for kickers in gen:

                c1, c2 = kickers
                product = (Card.PRIMES[r - 2]) ** 3 * (Card.PRIMES[c1 - 2]) * (Card.PRIMES[c2 - 2])
                self.unsuited_lookup[product] = rank
                rank += 1

        # 4) Two Pair
        rank = self.MAX_THREE_OF_A_KIND + 1

        tpgen = itertools.combinations(backwards_ranks, 2)
        for tp in tpgen:

            pair1, pair2 = tp
            kickers = list(backwards_ranks[:])
            kickers.remove(pair1)
            kickers.remove(pair2)
            for kicker in kickers:

                product = (Card.PRIMES[pair1 - 2]) ** 2 * (Card.PRIMES[pair2 - 2]) ** 2 * (Card.PRIMES[kicker - 2])
                self.unsuited_lookup[product] = rank
                rank += 1

        # 5) Pair
        rank = self.MAX_TWO_PAIR + 1

        # choose a pair
        for pairrank in backwards_ranks:

            kickers = list(backwards_ranks[:])
            kickers.remove(pairrank)
            kgen = itertools.combinations(kickers, 3)

            for kickers in kgen:

                k1, k2, k3 = kickers
                product = (Card.PRIMES[pairrank - 2]) ** 2 * (Card.PRIMES[k1 - 2]) * (Card.PRIMES[k2 - 2]) * (Card.PRIMES[k3 - 2])
                self.unsuited_lookup[product] = rank
                rank += 1

    def write_table_to_disk(self, table, filepath):
        """
        Writes lookup table to disk
        """
        with open(filepath, 'w') as f:
            for prime_prod, rank in table.items():
                f.write(str(prime_prod) + "," + str(rank) + '\n')

    def get_lexicographically_next_bit_sequence(self, bits):
        """
        Bit hack from here:
        http://www-graphics.stanford.edu/~seander/bithacks.html#NextBitPermutation

        Generator even does this in poker order rank
        so no need to sort when done! Perfect.
        """
        t = (bits | (bits - 1)) + 1
        next_val = t | ((((t & -t) // (bits & -bits)) >> 1) - 1)
        yield next_val
        while True:
            t = (next_val | (next_val - 1)) + 1
            next_val = t | ((((t & -t) // (next_val & -next_val)) >> 1) - 1)
            yield next_val
