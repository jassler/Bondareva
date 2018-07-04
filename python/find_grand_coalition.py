from balanced_collections import find_balancing_weights
from balanced_subcollections import is_minimal_balanced
from sympy import N
import re
import helpers

def find_minval_for_grand_coalition(game: dict, players):
    '''
    Find the smallest value that the grand coalition has to produce
    in order for a grand coalition to be formed.

    For every missing coalition S in game, it assumes that v(S) = 0
    '''

    collections = helpers.powerset_generator(game.keys())
    min_payoff = 0

    # list of collections that result in the min_payoff
    max_result = []

    for coalition in helpers.powerset(players):
        if coalition not in game.keys():
            game[coalition] = 0

    for collection in collections:
        minimal, result = is_minimal_balanced(collection, players)
        if not minimal:
            continue
        
        sum = 0

        for key, val in result.items():
            coalition = tuple([int(x) for x in str(key).replace('{', '').replace('}', '').split(',')])
            sum += (N(val) * game[coalition])
        
        if sum > min_payoff:
            min_payoff = sum
            max_result.clear()
        if sum == min_payoff:
            max_result.append(result)
    return min_payoff, max_result


if __name__ == '__main__':
    player_amount = int(input('Number of players participating: '))
    players = range(1, player_amount + 1)
    powerset = helpers.powerset(players)
    
    powerset.remove(())
    grand_coalition = tuple(players)
    powerset.remove(grand_coalition)
    print('v() = 0')

    game = {}

    for coalition in powerset:
        while True:
            prompt = 'v({}) = '.format(', '.join([str(x) for x in coalition]))
            try:
                game[coalition] = float(input(prompt).replace(',', '.'))
                break
            except ValueError:
                continue
    
    if len(players) >= 4:
        print('Evaluating... (this might take some time...)')
    min_payoff, results = find_minval_for_grand_coalition(game, players)

    # remove trailing zeros when printing
    min_payoff_str = re.sub('(\.(?:[1-9]+|0))0+$', '\\1', str(min_payoff))

    # print results and calculations in a nice way
    print('\nv{} >= {}'.format(tuple(players), min_payoff_str))
    print('--- Due to the following {} ---'.format('calculation' if len(results) == 1 else 'calculations'))
    
    # first know what all calculations look like so we can use ljust later on
    calc_list = []
    longest = 0
    for result in results:
        tmp = ''
        print_plus = False
        for key, val in result.items():
            if print_plus:
                tmp += '+ '
            else:
                print_plus = True
            
            if str(val) != '1':
                tmp += '{}*'.format(val)
            tmp += 'v({}) '.format(str(key).replace('{', '').replace('}', '').replace(',', ', '))
        if longest < len(tmp):
            longest = len(tmp)
        calc_list.append(tmp)
    
    for calc in calc_list:
        print('{}= {}'.format(calc.ljust(longest), min_payoff_str))