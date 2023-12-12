"""
bluff_eval.py Module

This module contains a function to calculate a bluff metric for the small and
big blind players based on the poker_dataframe.
"""

import ast
import os
import numpy as np
import pandas as pd
import warnings
from . import Card, Evaluator

def bluff_eval(df_filepath):
    """
    the bluff_eval function creates a copy of the poker_dataframe.pkl and
    appends an normalized aggresiveness and bluffing metric columns for the
    small blind and big blind and returns the new dataframe to the current
    working directory.

    Metrics:
        -aggSB: Normalized aggressiveness for the small blind player
            = sum of bets 'b' and raises 'r' for specific game / average number
            of bets and raises for the small blind player
        
        -aggBB: Normalized aggressiveness for the big blind player
            = sum of bets 'b' and raises 'r' for specific game / average number
            of bets and raises for the big blind player

        -SB Bluff Metric: Metric quantifying the whether the small blind player
        was bluffing and how aggressively
            = (% of poker hands the sb player's hand loses to) * (aggSB)

        -BB Bluff Metric: Metric quantifying the whether the big blind player
        was bluffing and how aggressively
            = (% of poker hands the bb player's hand loses to) * (aggBB)

    Args:
        df_filepath(str): Filepath to poker_dataframe.pkl containing poker data.
    
    Returns:
        None

    Exports:
        poker_df_w_bluff.pkl to current working directory. poker_df_w_bluff.pkl
        is copy of input dataframe.pkl with all games not played to completion 
        removed and with added aggSB,aggBB, SB Bluff Metric, and BB Bluff Metric
        columns.

    """
    # Import and clean dataframe and add columns
    df = pd.read_pickle(df_filepath)
    blf_df = df[(~df['River'].isnull()) & (~df['SB cards'].isnull()) & \
                (~df['BB cards'].isnull()) & (~df['River actions'].isnull())]

    warnings.filterwarnings('ignore')
    blf_df['aggSB'] = np.nan
    blf_df['aggBB'] = np.nan
    blf_df['SB Bluff Metric'] = np.nan
    blf_df['BB Bluff Metric'] = np.nan
    blf_df = blf_df.reset_index()

    # Calculate Aggressiveness
    for loc in blf_df.index:
        sb_agg = 1
        bb_agg = 1
        for i, action in enumerate(blf_df['River actions'][loc]):
            if i %2==0:
                if action[0] == 'b' or action[0] == 'r':
                    sb_agg += 1
                else:
                    sb_agg += 0
            else:
                if action[0] == 'b' or action[0] == 'r':
                    bb_agg += 1
                else:
                    bb_agg += 0
        blf_df['aggBB'][loc] = bb_agg
        blf_df['aggSB'][loc] = sb_agg

    # Normalize aggressiveness to mean
    blf_df['aggSB'] = blf_df['aggSB']/blf_df['aggSB'].mean()
    blf_df['aggBB'] = blf_df['aggBB']/blf_df['aggBB'].mean()

    # Calculate handrank % and bluff metric
    for loc in blf_df.index:
        board_list = blf_df['Flop'][loc] + \
            [blf_df['Turn'][loc], blf_df['River'][loc]]
        hand_sb_list = ast.literal_eval(blf_df['SB cards'][loc].\
            replace("[ ", "['").replace(" ]", "']").replace(", ", "', '"))
        hand_bb_list = ast.literal_eval(blf_df['BB cards'][loc].\
            replace("[ ", "['").replace(" ]", "']").replace(", ", "', '"))

        handSB = [Card.new(card) for card in hand_sb_list]
        handBB = [Card.new(card) for card in hand_bb_list]
        board = [Card.new(card) for card in board_list]

        # Calc % of hands SB and BB player loses to
        sb_per = 1 - eval.get_rank_percentage(eval.evaluate(handSB, board))
        bb_per = 1 - eval.get_rank_percentage(eval.evaluate(handBB, board))

        # Calc bluff metric
        blf_df['SB Bluff Metric'][loc] = sb_per*blf_df['aggSB'][loc]
        blf_df['BB Bluff Metric'][loc] = bb_per*blf_df['aggBB'][loc]

    # Export new df with normalized aggressiveness and bluff metric
    poker_df_w_bluff = os.path.join(os.getcwd(), "poker_df_w_bluff.pkl")
    blf_df.to_pickle(poker_df_w_bluff)
