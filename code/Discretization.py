from copy import deepcopy
from Sym import Sym


def merge(col1, col2):
    new = deepcopy(col1)
    if type(col1) == Sym:
        for x, n in col2.has.items():
            add(new, x, n)
    else:
        for n in col2.has.values():
            add(new, n)
    new.lo = min(col1.lo, col2.lo)
    new.hi = max(col1.hi, col2.hi)
    return new


def merge2(col1, col2):
    new = merge(col1, col2)
    if new.div() <= (col1.div() * col1.n + col2.div() * col2.n) / new.n:
        return new
