from balanced_collections import find_balancing_weights
from sympy import N
from sympy.core.numbers import Float
from itertools import chain, combinations
import re
import sys

file = open('b.tex', 'w')

def find_balanced_subcollections(collection, players):
    '''
    Find all minimal balanced collections of coalitions
    '''
    def powerset_generator(collection):
        for subset in chain.from_iterable(combinations(collection, r) for r in range(len(collection)+1)):
            yield set(subset)
    # powerset algorithm from here: https://gist.github.com/michaelkrisper/5595918
    # powerset = [x for length in range(len(collection)+1) for x in itertools.combinations(collection, length)]

    powerset = powerset_generator(collection)
    players_in_item = {}
    for player in players:
        players_in_item[player] = False
    total_amount = 2 ** len(collection)
    file.write('The powerset for {} players is {} items long.\n\n'.format(len(players), total_amount))
    # solutions = []
    possible_count = 0
    count = 0

    file.write('\\begin{longtable}{ | r l | c | }\n')
    file.write('\\multicolumn{2}{c}{Collection of coalitions} & \multicolumn{1}{c}{Coefficients}\\\\[2pt]\n')

    # filter out collections that don't have all players participating
    for item in powerset:
        if len(item) > len(players):
            continue
        for player in players_in_item.keys():
            players_in_item[player] = False
        for coalition in item:
            for player in coalition:
                players_in_item[player] = True
        
        if all(players_in_item.values()):
            possible_count += 1
            count = test_item(item, count)
        
    file.write('\\hline\n')
    file.write('\\end{longtable}\\vspace{10pt}\n')
    file.write('Program had to check {} possible solutions.\\vspace{{12pt}}\n\n'.format(possible_count))
    
    # return solutions
    return count

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

# filter out not minimal balanced items
def test_item(item, count):
    result = find_balancing_weights(item, var_name='')
    if is_minimal_balanced(result):
        if count % 10 == 0:
            file.write('\\hline & & \\\\[-8pt]\n')
        collection = [str(x) for x in result.keys()]
        coefficients = result.values()
        # $\mathcal{B}_2 =$ & $\{\{1, 2\}, \{3\}\}$ & $(1, 1)$\\[2pt]
        coll_string = '{{{0}}}'.format(', '.join([str(x) for x in collection]))
        coll_string = coll_string.replace(r'{', r'\{').replace(r'}', r'\}')
        coeff_string = '\\left({0}\\right)'.format(', '.join([str(x) for x in coefficients]))
        coeff_string = re.sub(r'(\d*)/(\d*)', r'\\frac{\1}{\2}', coeff_string)
        count += 1
        file.write('$\\mathcal{{B}}_{{{0}}} =$ & ${1}$ & ${2}$\\\\[2pt]\n'.format(count, coll_string, coeff_string))
    return count

if __name__ == '__main__':
    
    file.write('''\\documentclass[10pt,a4paper,titlepage]{article}
\\usepackage[utf8]{inputenc}
\\usepackage{amsmath}
\\usepackage{longtable}
\\usepackage{amsfonts}
\\usepackage{amssymb}
\\usepackage{amsthm}
\\setlength{\\parindent}{0pt}
\\author{Felix Fritz}
\\title{A list of balanced collections of coalitions}
\\begin{document}
\\maketitle
\\tableofcontents
\\pagebreak
''')
    for players in range (1,8):
        file.write('\\section{{Balanced collections of coalitions for $N = {0}$}}\n'.format(players))

        players = [i for i in range(1,players+1)]
        powerset = [x for length in range(len(players)+1) for x in combinations(players, length)]
        powerset.remove(())
        count = 0
        
        count = find_balanced_subcollections(powerset, players)

        file.write('For $N = \\{{{0}\\}}$, a total of {1} collections are balanced.\\vspace{{8pt}}\n\n'.format(', '.join([str(x) for x in players]), count))
        
    file.write('\\end{document}')
    file.close()
    #file.write(solutions)
    # for solution in solutions:
    #     collection = [str(x) for x in solution.keys()]
    #     collection.sort()
    #     file.write('{{{0}}}'.format(','.join(collection), end=''))