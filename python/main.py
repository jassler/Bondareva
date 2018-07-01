from balanced_collections import find_balancing_weights
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
            coalitions.append(coalition)
        else:
            print('Coalition is already in your list: {0}'.format(coalition))
    
    return coalitions



if __name__ == '__main__':
    print('\n\n\n\n\n\n\n') 
    print('Is your collection of coalitions balanced?')
    print(r'Find out by entering each coalition separately in form of "1, 2, 3", which turns it into a coalition {1, 2, 3}')
    print('(spaces are optional, numbers must be seperated by commas)\n')
    print('When you are done, leave the input empty')

    coalitions = prompt_coalition_input()


    result = find_balancing_weights(coalitions, '\u03b4')
    weakly_balanced = False
    if result is None:
        print('There are no solutions')
    else:
        for key, val in result.items():
            if val == 0:
                weakly_balanced = True
            print('{0} = {1}'.format(key, val))
    
    print('It is {0}'.format('weakly balanced' if weakly_balanced else 'balanced'))