import itertools

def evaluate_hand(cards):
    """
    Evaluates a 5-card hand and returns its rank.

    This version includes the prime product calculation.
    """
    prime_products = [get_prime_product(rank) for rank in cards]
    prime_product = max(prime_products)
    return prime_product

def get_prime_product(rank):
    """
    Returns the prime product of a card rank.

    This function includes the logic from the original Card class.
    """
    PRIMES = [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41,
    ]
    # Calculate prime product using the rank
    return PRIMES[rank - 2]

def hand_summary(hands):
    """
    Provides a summary of the hands with their ranks.
    """
    for i, hand in enumerate(hands, 1):
        rank = evaluate_hand(hand)
        print(f"Player {i} hand rank: {rank}")

# Example usage:
hands = [
    [10, 11, 12, 13, 14],  # Royal Flush
    [2, 3, 4, 5, 6],       # Straight
    [7, 7, 7, 3, 3],       # Full House
    [8, 8, 8, 8, 2],       # Four of a Kind
    [9, 10, 11, 12, 13],   # Straight Flush
]

hand_summary(hands)
