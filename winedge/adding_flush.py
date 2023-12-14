"""
This module contains a function to quantify the risk of a flush being present based on
the board card in our historical dataset at the river stage of the game.
"""
import os
import warnings

import numpy as np
import pandas as pd
from collections import Counter

def flush_eval_to_df(poker_df_filepath):
    """
    Function creates a modified version of the poker_dataframe from our historical data.
    The new dataframe only contains games that made it to the river stage of the game.
    The modified dataframe contains 3 new columns which adds the 'Board', created from
    combining the flop, turn, and river cards, adds 'Flush Count', the max count of a 
    singular suit on the board, and adds 'Flush', which is a conversion from 'Flush
    Count' to a likelihood that a flush is present.

    'Flush' Quantification:
    --------------
        - 0 (No possible flush): 'Flush Count' = 1 or 2, flush is not possible
        - 1 (Low possible flush): 'Flush Count' = 3, player needs two more of same suit
        - 2 (High possible flush): 'Flush Count' = 4, player needs one more of same suit
        - 3 (Flush on the board): 'Flush Count' = 5, flush is present on the board
        
        

    Added Columns:
    --------------
        - Board: combing cards from flop, turn, and river column per game
        - Flush Count: max count of same suit on the board
        - Flush: conversion from flush count using quantification above
    
    Args:
    --------------
        - poker_df_filepath: .pkl dataframe file formated in same way as poker_dataframe.

    Return:
    --------------
        None
    
    Export:
    --------------
        poker_dataframe_w_flush.pkl file exported to current working directory.
    """
    fl_df = pd.read_pickle(poker_df_filepath)

    #Creating new columns that are filled with NaN
    warnings.filterwarnings('ignore')
    fl_df['Board'] = np.nan
    fl_df['Flush Count'] = np.nan
    fl_df['Flush'] = np.nan

    #Resetting index of new dataframe
    fl_df = fl_df.reset_index()
    #Creating board by taking flop cards, and appending the turn and river card. 
    #then resetting the flop to its orignal form
    for loc in fl_df.index:
        fl_df['Board'][loc] = fl_df['Flop'][loc]
        fl_df['Board'][loc].append(fl_df['Turn'][loc])
        fl_df['Board'][loc].append(fl_df['River'][loc])
        fl_df['Flop'][loc] = fl_df['Flop'][loc][slice(3)]
    #Looking at board cards per game, per index of 'Board'. Counting the max instance 
    #of a single suit on the board. If max count is 1 or 2, 'Flush' = 0, max count = 3,
    #"Flush" = 1, max count = 4, 'Flush' = 2, max count = 5, 'Flush' = 3. These 'Flush' 
    #values signify likelihood of a player to get a flush on the board with 0 = impossible, 
    #and 3 = flush on board
    for games in fl_df.index:
        suits=[]
        for i in range(5):
            suits.append(fl_df['Board'][games][i][1])
        counts = Counter(suits)
        count = max(counts.values())
        if count == 1:
            flush = 0
        elif count ==2:
            flush = 0
        elif count == 3:
            flush = 1
        elif count == 4:
            flush = 2
        else:
            flush = 3
        fl_df['Flush Count'][games] = count
        fl_df['Flush'][games] = flush
    poker_dataframe_flush_risk = os.path.join(os.getcwd(), "poker_dataframe_flush_risk.pkl")
    fl_df.to_pickle(poker_dataframe_flush_risk)

    


