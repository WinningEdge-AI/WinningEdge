"""
This module raw accessed data and outputs a dataframe with all the relevant game info.
Original data came in ~30,000 raw txt files.

NOTES to Self
best solution as of 11/5
save this df in github so we can use it instead
Figure out how to use process_street_actions for preflop
"""

import os
#from tqdm import tqdm
#from IPython.core.interactiveshell import InteractiveShell # for all output
#InteractiveShell.ast_node_interactivity = "all"
files_path = [os.path.join(r,file) for r,d,f in os.walk(r"C:\Users\Peter\Desktop\Springboard\capstone1\Bought hands\unzipped") for file in f]

def get_hole_cards(sample_game, street_indices, small_blind_name):
    """
    This function captures hole cards if they are available and correctly assigns them to players
    """
    hole_cards1 = None
    hole_cards2 = None

    # Get hole cards
    if 'shows' in str(sample_game[street_indices[-1] + 1]):
        hole_cards1 = sample_game[street_indices[-1] + 1][-11:-1]
        hole_cards2 = sample_game[street_indices[-1] + 2][-11:-1]

    # Assign the hole cards correctly
    hole_cards1_player = sample_game[street_indices[-1] + 1][0:sample_game[street_indices[-1] + 1].index(' ') + 1]
    if hole_cards1_player == small_blind_name:
        small_bling_hole_cards = hole_cards1
        big_blind_hole_cards = hole_cards2
    else:
        small_bling_hole_cards = hole_cards2
        big_blind_hole_cards = hole_cards1

    return small_bling_hole_cards, big_blind_hole_cards

def left(sample_string, amount):
    """
    This is unnecessary but I am using it anyway.
    """
    return sample_string[:amount]

def process_street_actions(sample_game, start_index, end_index):
    """
    This function loops over the actions that players made during the game
    and stores them in a list of tuples
    """
    street_list = []
    for j in range(start_index, end_index):
        if 'folds' in sample_game[j]:
            thistuple = ('f', 0)
            street_list.append(thistuple)
        if ('calls' in sample_game[j] or 'bets' in sample_game[j] or 'raises' in sample_game[j]):
            dollar_sign = sample_game[j].index('$')
            amount = sample_game[j][dollar_sign + 1:-2]
            first_space = sample_game[j].index(' ')
            action = sample_game[j][first_space + 1:first_space + 5]
            tuple_to_add = (action[0], amount)
            street_list.append(tuple_to_add)
        if 'checks' in sample_game[j]:
            thistuple = ('k', 0)
            street_list.append(thistuple)
    return street_list

# pylint: disable=C0103
folded_pre=0
rows_list=[]

for f in files_path:
    with open(f, 'r') as file1:
        lines = file1.readlines()
    file_name = os.path.basename(f)

    # Find indices of lines starting with '#Game'
    game_indices = [i for i, line in enumerate(lines) if line.strip().startswith('#Game')]

    # Extract game data based on indices
    games = [lines[game_indices[i-1]:game_indices[i]] for i in range(1, len(game_indices))]

    # Now, process each game individually
    for index, game in enumerate(games):
        try:
            game_number = game[0].strip()[11:]
            small_blind_string_index = game[8].find('posts small blind')
            big_blind_string_index = game[9].find('posts big blind')
            small_blind_name = game[8][0:small_blind_string_index] #with a trailing space
            big_blind_name = game[9][0:big_blind_string_index]
            i = 10 #this is where line **Dealing down cards ** is
            preflop=[]
            flop=[]
            turn=[]
            river=[]
            preflop_counter = 0
            flop_counter=0
            stack_sb_index = game[6].find('$')
            stack_bb_index = game[7].find('$')
            stack_sb = game[6][stack_sb_index+1:-3]
            stack_bb = game[7][stack_bb_index+1:-3]
            flop_cards=None
            turn_card=None
            river_card=None

#find indeces of flop, turn , river and summary
            street_indeces = []
            for index_in_game, line in enumerate(game):
                if '** Dealing flop' in line or '** Dealing turn' in line or '** Dealing river' in line:
                    street_indeces.append(index_in_game)
                elif line.startswith('** Summary **'):
                    street_indeces.append(index_in_game)

#getting hole cards using the function
            sb_hole_cards, bb_hole_cards = get_hole_cards(game, street_indeces, small_blind_name)

#Getting preflop actions

#currently working on runnign this by calling process_street_actions
            while not ((game[i][:13] == ('** Summary **')) or (game[i][0:18] == ('** Dealing flop **'))):
                if 'folds' in game[i]:
                    thistuple= ('f',0)
                    preflop.append(thistuple)
                if ('calls' in game[i]) or ('bets' in game[i]) or ('raises' in game[i]):
                    dollar = game[i].index('$')
                    amount = game[i][dollar+1:-2]
                    first_space = game[i].index(' ')
                    action = game[i][first_space+1:first_space+5]
                    tuple_to_add = (action[0],amount)
                    preflop.append(tuple_to_add)
                if 'checks' in game[i]:
                    thistuple= ('k',0) #k for check
                    preflop.append(thistuple)
                i=i+1
                preflop_counter +=1

#Getting flop cards and actions
            if len(street_indeces)>1:
                flop_cards = [game[street_indeces[0]][-13:-11],game[street_indeces[0]][-9:-7],game[street_indeces[0]][-5:-3]]
                flop = process_street_actions(game, street_indeces[0], street_indeces[1])

#Getting turn cards and actions
            if len(street_indeces)>2:
                turn_card = game[street_indeces[1]][-5:-3]
                turn = process_street_actions(game, street_indeces[1], street_indeces[2])

#Getting river cards and actions
            if len(street_indeces)>3:
                river_card = game[street_indeces[2]][-5:-3]
                river=process_street_actions(game, street_indeces[2], street_indeces[3])

            remove_folded_pre =False  #this parameter identifies hands that were folded immediately
            if preflop[0][0][0]=='f':
                folded_pre+=1
                remove_folded_pre=True

#Create a dictionary with all the data per game
            river = river if river else None #if empty change to None to save space
            turn = turn if turn else None
            flop = flop if flop else None

            game_row  = {'Game ID':game_number,'File':file_name ,'Player SB':small_blind_name,
                         'Player BB':big_blind_name, 'Preflop actions':preflop,
                         'Flop actions':flop, 'Turn actions':turn,'River actions':river,
                         'Flop':flop_cards, 'Turn':turn_card, 'River':river_card, 'SB stack':stack_sb,
                         'BB stack': stack_bb, 'SB cards': sb_hole_cards,
                         'BB cards':bb_hole_cards,'Folded pre':remove_folded_pre}
            rows_list.append(game_row)

        except Exception as e:
            print(f"An error occurred: {e}")
