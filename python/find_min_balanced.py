from balanced_collections import find_balancing_weights
from balanced_subcollections import find_balanced_subcollections
from sympy import N
from sympy.core.numbers import Float
import re
import sys

def prompt_coalition_input():
    '''
    Ask user to type in every coalition inside the collection line by line
    '''
    coalitions = []

    while True:
        line: str = input('Coalition #{0}: '.format(len(coalitions) + 1))
        if line == '':
            break
        
        # remove everything except for numbers and commas
        line = re.sub('[^0-9,]', '', line)
        coalition = line.split(',')

        # some sanitization: remove empty strings, cast to int, sort, remove duplicates
        tmp = list(filter(None, coalition))
        tmp = [int(i) for i in tmp]
        tmp.sort()
        coalition.clear()
        for player in tmp:

            # add player to coalition
            if player not in coalition:
                coalition.append(player)
        
        # add coalition to collection of coalitions
        if coalition not in coalitions:
            coalitions.append(tuple(coalition))
        else:
            print('Coalition is already in your list: {0}'.format(coalition))
    
    return coalitions


if __name__ == '__main__':
    print('\nIs your collection of coalitions balanced?')
    print('Find out by entering each coalition separately in form of "1, 2, 3", which turns it into a coalition {1, 2, 3}')
    print('(spaces are optional, numbers must be seperated by commas)\n')
    print('When you are done, leave the input empty')

    # gather coalitions
    coalitions = prompt_coalition_input()

    # gather results
    result = find_balancing_weights(coalitions, var_name='\u03b4_')

    # evaluate results
    balanced = True
    weakly_balanced = False
    minimal_balanced = True

    # if function returns None, then the linear program doesn't have a solution
    if result is None:
        balanced = False
        print('There are no solutions -> it is not balanced')
    else:

        # minimal balanced collections have fixed values:
        # N(val) then should return a float, otherwise collection has infinitely many solutions and is not minimal
        # if balancing vector contains 0, then it's weakly balanced
        # in some cases such as {{1,2},{1,3},{2,3},{2,3,4}} there are negative solutions -> definitely not balanced
        for key, val in result.items():
            if type(N(val)) is not Float:
                minimal_balanced = False
            if val.is_zero:
                weakly_balanced = True
            elif val.is_negative:
                balanced = False
            
            print('{0} = {1}'.format(key, val))

        # tell user what order of balancedness he reached
        print('It is ', end='')
        if not balanced:
            print('not ', end='')
        elif minimal_balanced:
            print('minimal ', end='')
        elif weakly_balanced:
            print('weakly ', end='')

        print('balanced')

        # in case it's not minimal balanced, try to find all subsets that are
        if not minimal_balanced or weakly_balanced:
            print('Do you want to find all minimal balanced collections?')
            if len(coalitions) >= 10:
                print('Note that with {} coalitions, this program has to process {} possible outcomes'.format(len(coalitions), 2 ** coalitions))

            if input('Y/n: ').lower() == 'y':
                print('Trying to find all minimal balanced collections')
                players = []
                for coalition in coalitions:
                    for player in coalition:
                        if player not in players:
                            players.append(player)
                solutions = find_balanced_subcollections(coalitions)
                for solution in solutions:
                    keys = [str(x) for x in solution.keys()]
                    values = [str(x) for x in solution.values()]
                    print('{{{}}} => ({})'.format(', '.join(keys), ', '.join(values)))