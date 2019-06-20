from itertools import chain, combinations


#lambda functions
def powerset(list):
    return chain.from_iterable(combinations(list , r) for r in range(len(list)+1))
