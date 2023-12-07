"""
adding_rank Module

The adding_rank Module contains a function which converts the poker_dataframe pickle data file
into a pandas dataframe. The function uses the evaluator.py and card.py modules to
calculate the hand strength and hand rank for the small blind and big blind player
for each game in the poker_dataframe that was played to completion (river stage - all player
cards revealed) and appends the hand strength and hand rank for each player to the pandas dataframe.

The adding_rank module contains the add_rank_to_pkl_df function which converts the 

Dependancies:
--------------
- card.py
- evaluator.py
- poker_dataframe.pkl

Functions:
--------------
- add_rank_to_pkl_df(filepath):
    This function creates a pandas dataframe from the poker_dataframe.pkl file.
    The function then removes games which have not been played to completion (games where all
    player cards are not revealed). Then it uses the evaluator.py, card.py, and look.py modules
    to calculate the hand rank and hand strength for each player for each game in the dataframe.
    The hand rank and hand strength for each player are then appended into the pandas
    poker_dataframe in the following columns:
        - SB Handrank (str): Phrase describing the type of hand the small blind player has.
            (e.g. Two Pair)
        - BB Handrank (str): Phrase describing the type of hand the big blind player has.
            (e.g. Two Pair)
        - SB Hand Strength (str): A normalized rank for the small blind hand ranging from 0-1.
            The normalization is based on how strong the hand is relative to the 7462 possible
            poker hands. (e.g. 1 = Royal Flush, 7642 = 7,5,4,3,2 unsuited)
        - BB Hand Strength (str): A normalized rank for the big blind hand ranging from 0-1.
            The normalization is based on how strong the hand is relative to the 7462 possible
            poker hands. (e.g. 1 = Royal Flush, 7642 = 7,5,4,3,2 unsuited)
    The function converts the dataframe back into a pkl file titled "poker_dataframe_w_rank.pkl"
    and saves the file in the current working directory where the function was run.

    Args:
        filepath (str): Filepath to the poker_dataframe.pkl file.
    Returns:
        None (saves pkl version of dataframe to current working directory)
Exports:
--------------
- poker_dataframe_w_rank.pkl is saved in current working directory which is a copy of the
poker_dataframe.pkl file input appended with the SB and BB handrank and normalized hand strength.
"""
import ast
import os
import warnings

import numpy as np
import pandas as pd

from . import Card, Evaluator

def add_rank_to_pkl_df(poker_dataframe_filepath):
    """
    This function saves a modified copy of the poker_dataframe.pkl file to the current working
    directory. The original file is modified to only contain games where the player cards are
    revealed and is appended with columns for both players hand strength and hand rank as
    calculated by the evaluator.py module.

    Args:
        filepath (str): Filepath to the poker_dataframe.pkl file or a file which is formatted 
        the same contain heads up poker player data.
    Returns:
        None
    Exports:
        Saves modified poker_dataframe.pkl file containing only completed games appended
        with player hand strength and hand rank data to the current working directory
        in a pickle file poker_dataframe_w_rank.pkl.
    """
    # Create pandas df from pickle dataframe
    pk = pd.read_pickle(poker_dataframe_filepath)
    # Remove all entries where player cards are not revealed (game did not go to
    # river stage).
    pk_rvr = pk[(~pk['River'].isnull()) & (~pk['SB cards'].isnull()) & \
                (~pk['BB cards'].isnull())]

    #Add Columns to dataframe for SB & BB Handrank and Handstrength
    warnings.filterwarnings('ignore')
    pk_rvr['SB Handrank'] = np.nan
    pk_rvr['BB Handrank'] = np.nan
    pk_rvr['SB Hand Strength'] = np.nan
    pk_rvr['BB Hand Strength'] = np.nan

    # Definal evaluator
    pkeval = Evaluator()

    for loc in pk_rvr.index:
        # Extract the board and player cards from the dataframe and format them
        # for use in the Card.py module.
        board_list = [pk_rvr['Turn'][loc], pk_rvr['River'][loc]] + \
            pk_rvr['Flop'][loc]
        hand_sb_list = ast.literal_eval(pk_rvr['SB cards'][loc].\
            replace("[ ", "['").replace(" ]", "']").replace(", ", "', '"))
        hand_bb_list = ast.literal_eval(pk_rvr['BB cards'][loc].\
            replace("[ ", "['").replace(" ]", "']").replace(", ", "', '"))

        # Replace the original df elements with the cleaned ones
        pk_rvr['SB cards'][loc] = hand_sb_list
        pk_rvr['BB cards'][loc] = hand_bb_list

        # Create unique cards formatted for the evaluator using the Card.py
        # module based on the player and board coards extracted from the
        # dataframe.
        hand_sb = [Card.new(card) for card in hand_sb_list]
        hand_bb = [Card.new(card) for card in hand_bb_list]
        board = [Card.new(card) for card in board_list]

        pk_rvr['SB Handrank'][loc] = pkeval.class_to_string(
            pkeval.get_rank_class(pkeval.evaluate(hand_sb, board)))
        pk_rvr['SB Hand Strength'][loc] = pkeval.get_rank_percentage(
            pkeval.evaluate(hand_sb, board))

        pk_rvr['BB Handrank'][loc] = pkeval.class_to_string(
            pkeval.get_rank_class(pkeval.evaluate(hand_bb, board)))
        pk_rvr['BB Hand Strength'][loc] = pkeval.get_rank_percentage(
            pkeval.evaluate(hand_bb, board))

    # Reset the index of the pandas poker_dataframec
    pk_rvr = pk_rvr.reset_index()

    # Convert the poker_dataframe pk_rvr to a pkl datafile and save it in the
    # current working directory.
    poker_dataframe_w_rank = os.path.join(os.getcwd(),
                                          "poker_dataframe_w_rank.pkl")
    pk_rvr.to_pickle(poker_dataframe_w_rank)
