"""
This module contains a function to quantify the risk of a straight being present based on
the board card in our historical dataset at the flop, turn, and river stages of the game.
"""
import os
import warnings

import numpy as np
import pandas as pd

from . import Card

def straight_eval_to_df(poker_df_filepath):
    """
    Function creates a modified version of the poker_dataframe from our historical data.
    The modified dataframe contains 3 new columns which quanitify the risk of a straight
    based on the board cards for each game at the flop, turn, and river stages of the game.

    Risk Quantification:
    --------------
        - 1 (Low): 3 or more cards + board cards required to make straight.
        - 2 (Medium): 2 more cards + board cards required to make straight.
        - 3 (High): 1 more card + board cards required to make straight.
        - 4 (Straight): Straight is already present in board cards.
        - NaN: Match did not reach that stage of the game so straight risk
        could not be calulated

    Added Columns:
    --------------
        - Flop Straight Risk: Risk quantification value at flop.
        - Turn Straight Risk: Risk quantification value at turn.
        - River Straight Risk: Risk quantification value at river.
    
    Args:
    --------------
        - poker_df_filepath: .pkl dataframe file formated in same way as poker_dataframe.

    Return:
    --------------
        None
    
    Export:
    --------------
        poker_df_straight_risk.pkl file with straight risk columns exported
        to current working directory.
    """
    st_df = pd.read_pickle(poker_df_filepath)

    #Add Columns to dataframe for Flop, Turn, and River straight risk.
    warnings.filterwarnings('ignore')
    st_df['Flop Straight Risk'] = np.nan
    st_df['Turn Straight Risk'] = np.nan
    st_df['River Straight Risk'] = np.nan

    # Calculate straight risk at flop.
    for loc in st_df.index:
        if st_df['Flop'][loc] is not None:
            # Create sorted list of integer rank of board cards ignoring
            # repeats.
            rank_char = [card[0] for card in st_df['Flop'][loc]]
            rank_char = list(set(rank_char))
            int_rank = [Card.CHAR_RANK_TO_INT_RANK[char] for char in rank_char]
            # Deal with aces being low and high.
            if 14 in int_rank:
                int_rank.append(1)
            int_rank = sorted(int_rank)
            # set initial risk
            risk = 1
            # Calculate differences between board cards
            diff = [int_rank[i + 1] - int_rank[i] \
                    for i in range(len(int_rank) - 1)]
            # If there are consecutive differences of 1 or 2 analyze further
            if '11' in ''.join(map(str, diff)) or '22' in ''.join(
                map(str, diff)) or '12' in ''.join(
                    map(str, diff)) or '21' in ''.join(map(str, diff)):

                # The number of consecutive 1's or 2's in difference list
                # will equal the risk value.
                count = 0
                max_count = 0
                for num in diff:
                    if num == 1 or num ==2:
                        count +=1
                        max_count = max(max_count,count)
                    else:
                        count = 0
                risk = max_count
            else:
                risk = 1
            st_df['Flop Straight Risk'][loc] = risk
        else:
            continue

    # Calc straight risk at turn.
    for loc in st_df.index:
        if st_df['Turn'][loc] is not None:
            rank_char = [card[0] for card in st_df['Flop'][loc]] + [
                st_df['Turn'][loc][0]]
            rank_char = list(set(rank_char))
            int_rank = [Card.CHAR_RANK_TO_INT_RANK[char] for char in rank_char]
            if 14 in int_rank:
                int_rank.append(1)
            int_rank = sorted(int_rank)

            diff = [int_rank[i + 1] - int_rank[i] \
                    for i in range(len(int_rank) - 1)]
            if '11' in ''.join(map(str, diff)) or '22' in ''.join(
                map(str, diff)) or '12' in ''.join(
                    map(str, diff)) or '21' in ''.join(map(str, diff)):
                count = 0
                max_count = 0
                for num in diff:
                    if num == 1 or num ==2:
                        count +=1
                        max_count = max(max_count,count)
                    else:
                        count = 0
                risk = max_count
            else:
                risk = 1
            st_df['Turn Straight Risk'][loc] = risk
        else:
            continue

    # Calc straight risk at river.
    for loc in st_df.index:
        if st_df['River'][loc] is not None:
            rank_char = [card[0] for card in st_df['Flop'][loc]] + [
                st_df['Turn'][loc][0]] + [st_df['River'][loc][0]]
            rank_char = list(set(rank_char))
            int_rank = [Card.CHAR_RANK_TO_INT_RANK[char] for char in rank_char]
            if 14 in int_rank:
                int_rank.append(1)
            int_rank = sorted(int_rank)

            diff = [int_rank[i + 1] - int_rank[i] \
                    for i in range(len(int_rank) - 1)]
            if '11' in ''.join(map(str, diff)) or '22' in ''.join(
                map(str, diff)) or '12' in ''.join(
                    map(str, diff)) or '21' in ''.join(map(str, diff)):
                count = 0
                max_count = 0
                for num in diff:
                    if num == 1 or num ==2:
                        count +=1
                        max_count = max(max_count,count)
                    else:
                        count = 0
                risk = max_count
            else:
                risk = 1
            st_df['River Straight Risk'][loc] = risk
        else:
            continue

    poker_df_straight_risk = os.path.join(os.getcwd(),
                                          "poker_df_straight_risk.pkl")
    st_df.to_pickle(poker_df_straight_risk)