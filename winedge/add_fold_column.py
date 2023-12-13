"""
This is a module that adds 2 new columns to the dataframe:
- 'Fold_sb', which is True if the small blind folds during the game, and False otherwise
- 'Fold_bb', which is True if the big blind folds during the game, and False otherwise

The output is saved in a new dataframe
"""

import pandas as pd

def check_fold(preflop_actions, flop_actions, turn_actions, river_actions):
    """
    This function examines the actions throughout the course of the poker game, 
    and determines if the small blind or big blind player folded
    
    Args:
        preflop_actions (list of str): A list of action strings during the preflop phase
        flop_actions (list of str): A list of action strings during the flop phase
        turn_actions (list of str): A list of action strings during the turn phase
        river_actions (list of str): A list of actions strings during the river phase

    Returns:
        tuple of (bool, bool): A tuple containing two boolean values.
            The first boolean indicates if the small blind (SB) player folded.
            The second boolean indicates if the big blind (BB) player folded
    """
    fold_sb = False
    fold_bb = False
    
    if preflop_actions is not None:
        for index, action in enumerate(preflop_actions):
            if action[0] == 'f':
                if index % 2 == 0:
                    fold_sb = True
                else:
                    fold_bb = True
    
    if flop_actions is not None and fold_sb is False and fold_bb is False:
        for index, action in enumerate(flop_actions):
            if action[0] == 'f':
                if index % 2 == 0:
                    fold_sb = True
                else:
                    fold_bb = True
    
    if turn_actions is not None and fold_sb is False and fold_bb is False:
        for index, action in enumerate(turn_actions):
            if action[0] == 'f':
                if index % 2 == 0:
                    fold_sb = True
                else:
                    fold_bb = True
    
    if river_actions is not None and fold_sb is False and fold_bb is False:
        for index, action in enumerate(river_actions):
            if action[0] == 'f':
                if index % 2 == 0:
                    fold_sb = True
                else:
                    fold_bb = True
    
    return fold_sb, fold_bb

df = pd.read_pickle("../dataframe/poker_dataframe.pkl")
df['fold_sb'], df['fold_bb'] = zip(*df.apply(lambda row: check_fold(row['Preflop actions'], row['Flop actions'], row['Turn actions'], row['River actions']), axis=1))