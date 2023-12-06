"""
This is a module that add 4 new columns that indicate aggression levels
4 possible output: 00,01,10,11
saves output in new df
"""

import pandas as pd

def check_aggression(action_list):
    """
    This function looks at the actions that happened and outputs a 2 digit number
    The number represents aggression show by either player

    Player counts as aggressive if they raised or bet

    Ex:
    00 - means both passive
    10 means SB aggressive BB passive
    01 means SB passive BB aggressive
    11 means both aggressive
    """
    agg_sb=0
    agg_bb =0

    if action_list==None:
        return None
    for index,action in enumerate(action_list):
        if action[0] in ('r','b'):
            if index %2==0:
                agg_sb=1
            else:
                agg_bb=1
    return agg_sb, agg_bb

df = pd.read_pickle("../dataframe/poker_dataframe.pkl")

df['Aggr preflop'] = df['Preflop actions'].apply(check_aggression)
df['Aggr flop'] = df['Flop actions'].apply(check_aggression)
df['Aggr turn'] = df['Turn actions'].apply(check_aggression)
df['Aggr river'] = df['River actions'].apply(check_aggression)

df.to_pickle('poker_dataframe_with_agg_columns.pkl')
