import math
from copy import deepcopy
from Sym import Sym
from Range import Range
from Utils import itself


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


def mergeAny(ranges0):
    def noGaps(t):
        for i in range(1, len(t)):
            t[i].lo = t[i - 1].hi
        t[0].lo = -math.inf
        t[-1].hi = math.inf
        return t

    j = 0
    ranges1 = []
    while j < len(ranges0):
        left, right = ranges0[j], ranges0[j + 1]
        if right:
            y = merge2(left.y, right.y)
            if y:
                j += 1
                left.hi, left.y = right.hi, y
        ranges1.append(left)
        j += 1

    return noGaps(ranges0) if len(ranges0) == len(ranges1) else mergeAny(ranges1)


def bin(col, x, the):
    if x == '?' or type(col) == Sym:
        return x
    tmp = (col.hi - col.lo) / (the.bins - 1)
    return 1 if col.hi == col.lo else math.floor(x / tmp + 0.5) * tmp


def bins(cols, rowss, the):
    out = {}
    for col in cols:
        ranges = {}
        for y, rows in enumerate(rowss):
            for row in rows:
                x, k = row[col.at]
            if x != '?':
                k = bin(col, x, the)
                if k not in ranges:
                    ranges[k] = Range(col.at, col.txt, x)
                extend(ranges[k], x, y)
        ranges = sorted(ranges, key=lambda r: ranges[r].lo)
        out[1 + len(out)] = ranges if type(col) == Sym else mergeAny(ranges)
    return out
