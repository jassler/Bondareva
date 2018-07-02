from sympy import Symbol, Matrix, solve_linear_system

def find_balancing_weights(coalitions: list, var_name: str = 'x'):
    '''
    Parameter coalitions is a list of lists, each inner list representing a coalition of players.
    Number of players is inferred depending on who participates in the coalitions
    '''
    coefficients = []
    players = {}
    matrices = []
    for i, coalition in enumerate(coalitions):
        coalition_name = '{0}{{{1}}}'.format(var_name, ','.join([str(x) for x in coalition]))
        coefficients.append(Symbol(coalition_name))
        for player in coalition:
            if player not in players:
                players[player] = []
            players[player].append(i)
    
    for player, participating in players.items():
        tmp = [0]*len(coalitions)
        for coalition in participating:
            tmp[coalition] = 1

        tmp.append(1)
        matrices.append(tmp)
    
    system = Matrix(matrices)
    return solve_linear_system(system, *coefficients)
