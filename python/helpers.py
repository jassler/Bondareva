from itertools import combinations, chain

# powerset generator gotten from here: https://stackoverflow.com/a/18826666/7669319
def powerset_generator(collection):
    for subset in chain.from_iterable(combinations(collection, r) for r in range(len(collection)+1)):
        yield set(subset)

# powerset array gotten from here: https://gist.github.com/michaelkrisper/5595918
def powerset(collection):
    return [x for length in range(len(collection)+1) for x in combinations(collection, length)]