from balanced_collections import find_balancing_weights
import helpers
from sympy import N
from sympy.core.numbers import Float
from itertools import chain, combinations
import re
import sys
import ast

def find_balanced_subcollections(collection):
    '''
    Find all minimal balanced collections of coalitions
    '''
    solutions = []
    powerset = helpers.powerset_generator(collection)
    players_in_item = {}


    for coalition in collection:
        for player in coalition:
            # if player appears in generated collection, switch to True
            # all players have to be in a collection for it to be minimal balanced
            players_in_item[player] = False
    player_amount = len(players_in_item.keys())

    
    for item in powerset:
        # filter out collections that don't have all players participating
        # and have too many items
        if len(item) > player_amount:
            continue
        for player in players_in_item.keys():
            players_in_item[player] = False
        for coalition in item:
            for player in coalition:
                players_in_item[player] = True
        
        if all(players_in_item.values()):
            result = find_balancing_weights(item)
            if is_result_minimal_balanced(result):
                solutions.append(result)

    return solutions

def is_result_minimal_balanced(result):
    
    # collection is not minimal balanced, if result isn't conclusive / not an absolute value
    if result is None:
        return False
    
    for _, val in result.items():
        if type(N(val)) is not Float:
            return False
        if val.is_zero or val.is_negative:
            return False
    return True

def is_minimal_balanced(collection, players) -> (bool, dict):
    # filter out collections that don't have all players participating
    # and have too many items
    if len(collection) > len(players):
        return False, None
    
    players_in_collection = []
    for coalition in collection:
        for player in coalition:
            if player not in players_in_collection:
                players_in_collection.append(player)
    
    if len(players) != len(players_in_collection):
        return False, None
    
    result = find_balancing_weights(collection)
    if not is_result_minimal_balanced(result):
        return False, None
    
    return True, result
    

if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        print('Usage:')
        print('Find subcollections to given collection:\npython {} [1] [2] [1,2] ...\n'.format(sys.argv[0]))
        print('Find subcollections to amount of players:\npython {} -p 4'.format(sys.argv[0]))
        print('Note that anything from 5 and above may take ages to compute')
        sys.exit()
    
    
    if sys.argv[1].lower() == '-p':
        if len(sys.argv) < 3:
            print('Expected number of players after -p')
            sys.exit()
        
        players = [i for i in range(1,int(sys.argv[2])+1)]
        collection = helpers.powerset(players)
        collection.remove(())
        collection.remove(tuple(players))
    else:
        arg = ','.join(sys.argv[1:])
        arg = re.sub('[^\[\]\d,]', '', arg)
        arg = re.sub(',+', ',', arg)
        arg.replace('][', '],[')

        collection = ast.literal_eval(''.join(sys.argv[1:]).replace('][', '],['))
        collection = [tuple(x) for x in collection]

    for item in find_balanced_subcollections(collection):
        keys = [str(x) for x in item.keys()]
        values = [str(x) for x in item.values()]
        print('{{{}}} => ({})'.format(', '.join(keys), ', '.join(values)))