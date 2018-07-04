from balanced_collections import find_balancing_weights
from itertools import chain, combinations
from sympy import N
from sympy.core.numbers import Float

def find_b(collection, players):
    # powerset generator: q\url{https://stackoverflow.com/a/18826666/7669319}q
    def powerset_generator(collection):
        for subset in chain.from_iterable(combinations(collection, r) for r in range(len(collection)+1)):
            yield set(subset)
    solutions = []
    powerset = powerset_generator(collection)
    players_in_collection = []

    for collection in powerset:
        # filter out collections with too many collections and
        # that don't have all players participating
        if len(collection) > len(players):
            continue
        players_in_collection.clear()
        for coalition in collection:
            for player in coalition:
                if player not in players_in_collection:
                    players_in_collection.append(player)

        if len(players_in_collection) == len(players):
            result = find_balancing_weights(collection)
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