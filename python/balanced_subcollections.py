from balanced_collections import find_balancing_weights
from sympy import N
from sympy.core.numbers import Float
import itertools
from multiprocessing.pool import Pool
from multiprocessing import Lock
from multiprocessing.managers import Array
import re

def find_balanced_subcollections(collection, players):
    '''
    Find all minimal balanced collections of coalitions
    '''
    # powerset algorithm from here: https://gist.github.com/michaelkrisper/5595918
    powerset = [x for length in range(len(collection)+1) for x in itertools.combinations(collection, length)]
    print('The powerset for {} players is {} long. '.format(len(players), len(powerset)))

    possible_collections = []
    solutions = []
    # filter out collections that don't have all players participating
    for item in powerset:
        if len(item) > len(players):
            continue
        players_in_item = []
        for coalition in item:
            for player in coalition:
                if player not in players_in_item:
                    players_in_item.append(player)
        
        if len(players) == len(players_in_item):
            possible_collections.append(item)
    
    def chunks(l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]
    # pool = Pool(10)

    # pool.map(test_item, possible_collections, chunksize=100)
    
    # pool.close()
    # pool.join()
    print('Program had to check {} possible solutions.\n'.format(len(possible_collections)))
    for collection in possible_collections:
        test_item(collection)
    
    return solutions

def is_minimal_balanced(result):
    # collection is minimal balanced, if result isn't conclusive / not an absolute value
    if result is None:
        return False
    
    for _, val in result.items():
        if type(N(val)) is not Float:
            return False
        if val.is_zero or val.is_negative:
            return False
    return True


solutions = []

# filter out not minimal balanced items
def test_item(item):
    result = find_balancing_weights(item, var_name='')
    if is_minimal_balanced(result):
        collection = [str(x) for x in result.keys()]

        #coefficients = [x for _,x in sorted(zip(collection, result.values()))]
        #collection.sort()
        coefficients = result.values()
        # $\mathcal{B}_2 =$ & $\{\{1, 2\}, \{3\}\}$ & $(1, 1)$\\[2pt]
        coll_string = '{{{0}}}'.format(', '.join([str(x) for x in collection]))
        coll_string = coll_string.replace(r'{', r'\{').replace(r'}', r'\}')
        coeff_string = '\\left({0}\\right)'.format(', '.join([str(x) for x in coefficients]))
        coeff_string = re.sub(r'(\d*)/(\d*)', r'\\frac{\1}{\2}', coeff_string)

        solutions.append('${0}$ & ${1}$'.format(coll_string, coeff_string))

        # with lock:
        #     count = counter.get()
        #     counter.set(count + 1)
        #     if count % 15 == 0:
        #         print('\\hline & &\\\\[-8pt]')
            
        #     print('$\\mathcal{{B}}_{{{0}}} =$ & ${1}$ & ${2}$\\\\[2pt]'.format(count, coll_string, coeff_string))
            
    

if __name__ == '__main__':
    print(r'\documentclass[10pt,a4paper,titlepage]{article}')
    print(r'\usepackage[utf8]{inputenc}')
    print(r'\usepackage{amsmath}')
    print(r'\usepackage{amsfonts}')
    print(r'\usepackage{amssymb}')
    print(r'\usepackage{amsthm}')
    print(r'\author{Felix Fritz}')
    print(r'\title{A list of balanced collections of coalitions}')
    print(r'\begin{document}')
    print(r'\maketitle')
    print(r'\tableofcontents')
    print(r'\pagebreak')

    for players in range (1, 6):
        solutions.clear()
        print('\\section{{Balanced collections of coalitions for $N = {0}$}}'.format(players))

        players = [i for i in range(1,players+1)]
        powerset = [x for length in range(len(players)+1) for x in itertools.combinations(players, length)]
        powerset.remove(())
        find_balanced_subcollections(powerset, players)

        print('For $N = \\{{{0}\\}}$, a total of {1} collections are balanced.\\vspace{{8pt}}\n'.format(', '.join([str(x) for x in players]), len(solutions)))
        
        print(r'\begin{tabular}{ | r l | c | }')
        print(r'\multicolumn{2}{c}{Collection of coalitions} & \multicolumn{1}{c}{Coefficients}\\[2pt]')
        print(r'\hline & & \\[-8pt]')
        
        for i, solution in enumerate(solutions):
            print('$\\mathcal{{B}}_{{{0}}} =$ & {1}\\\\[2pt]'.format(i+1, solution))

        print(r'\hline')
        print(r'\end{tabular}')
    print(r'\end{document}')
    #print(solutions)
    # for solution in solutions:
    #     collection = [str(x) for x in solution.keys()]
    #     collection.sort()
    #     print('{{{0}}}'.format(','.join(collection), end=''))