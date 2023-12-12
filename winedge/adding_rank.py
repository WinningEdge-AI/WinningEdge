"""
adding_rank Module

The adding_rank module contains a function which creates a modified copy
of the poker_dataframe.pkl file containing historical poker data and generated
by the create_dataframe.py module. The function appends the hand rank (a string
classifying the type of hand a player has) and hand strength (the percentage
of possible poker hands that the player beats) for both the small blind
and big blind player to the dataframe and exports it to the current working
directory.
"""
import ast
import os
import warnings

import numpy as np
import pandas as pd

from . import Card, Evaluator

def add_rank_to_pkl_df(poker_dataframe_filepath):
    """
    This function saves a modified copy of the poker_dataframe.pkl file created
    by the create_dataframe.py module to the current working directory. The
    cleans the dataframe of all games that were not played to completion. Then
    the function calculates the handrank and hand strength for the small blind
    and big bind players for each game and appends this information into 
    four new columns in the dataframe (see metrics). The new dataframe is saved
    as poker_dataframe_w_rank.pkl in the current working directory.

    Metrics:
    --------------
        - SB Handrank (str): Represents the type of hand the small blind
        player has
            (Ex. sb hand = 2,3,4,5,6 -> SB Handrank = 'Flush')

        - BB Handrank (str): Represents the type of hand the big blind
        player has
            (Ex. bb hand = 5,5,8,8,10 -> SB Handrank = 'Two Pair')

        - SB Hand Strength (float): Represents the % of possible poker hands
        the small blind player beats with their current cards.
            (Ex. sb hand = royal flush -> SB Hand Strength = 0.9999)

        - BB Hand Strength (float): Represents the % of possible poker hands
        the sbig blind player beats with their current cards.

    Args:
    --------------
        filepath (str): Filepath to the poker_dataframe.pkl file containing
        historical poker data formated with the create_dataframe.py module.

    Returns:
    --------------
        None

    Exports:
    --------------
        Saves modified dataframe as poker_dataframe_w_rank.pkl to current
        working directory.
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
