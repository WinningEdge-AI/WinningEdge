"""
Currently no good method to check flushes.
"""

import itertools

def evaluate_hand(cards):
    """
    Evaluates a 5-card hand and returns its rank.

    This version includes the prime product calculation and a check for a flush.
    """
    suits = [card % 4 for card in cards]
    
    # Check for a flush (all cards have the same suit)
    is_flush = len(set(suits)) == 1
    
    if is_flush:
        # You can handle flush separately, e.g., assign a special rank for flush
        return "Flush"
    
    prime_products = [get_prime_product(rank) for rank in cards]
    max_prime_product = max(prime_products)
    
    return max_prime_product

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
    [2, 4, 6, 8, 10],      # Flush (added example)
]

hand_summary(hands)
