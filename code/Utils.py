import math
from Main import coerce
import os
import random

from Sym import Sym


def rnd(n, nPlaces=2):
    mult = pow(10, nPlaces)
    return math.floor(n * mult + 0.5) / mult


def rand(lo=0, hi=1, Seed=937162211):
    # Seed=937162211
    Seed = (16807 * Seed) % 2147483647
    return lo + (hi - lo) * Seed / 2147483647, Seed


def rint(lo, hi):
    x, seed = rand(lo, hi)
    return math.floor(0.5 + x)


def csv(src, fun):
    if not os.path.isfile(src):
        print("\nfile " + src + " doesn't exists!")
        sys.exit(2)
    with open(src, 'r') as file1:
        for line in file1:
            temp = []
            for j in line.strip().split(','):
                temp.append(coerce(j))
            fun(temp)


def mp(src, fun):
    for i in src:
        # print(i)
        fun(i)


def kap(t, fun, u={}):
    u = {}
    for k, v in enumerate(t):
        v, k = fun(k, v)
        if not k:
            u[len(u)] = v
        else:
            u[k] = v
    return u


def cosine(a, b, c):
    if c == 0:
        c = 0.5
    x1 = (a ** 2 + c ** 2 - b ** 2) / (2 * c)
    x2 = max(0, min(1, x1))
    y = math.sqrt(abs(a ** 2 - x2 ** 2))
    return x2, y


def many(t, n, seed=937162211):
    random.seed(seed)
    return random.choices(t, k=n)


def any(t, seed=937162211):
    random.seed(seed)
    return random.choices(t)[0]


def per(t, p=0.5):
    p = math.floor((p * len(t)) + .5)
    return t[max(1, min(len(t), p))]


def show(node, what, cols, nPlaces, lvl=0):
    if node:
        print("| " * lvl + str(len(node["data"].rows)) + " ", end='')
        # print(node)
        if "left" not in node or lvl == 0:
            print(node["data"].stats(nPlaces, node["data"].cols.y, "mid"))
        else:
            print("")
        show(None if "left" not in node else node["left"], what, cols, nPlaces, lvl + 1)
        show(None if "right" not in node else node["right"], what, cols, nPlaces, lvl + 1)


def cliffs_delta(ns1, ns2, the, seed=937162211):
    if len(ns1) > 256:
        ns1 = many(ns1, 256, seed)
    if len(ns2) > 256:
        ns2 = many(ns2, 256, seed)
    if len(ns1) > 10 * len(ns2):
        ns2 = many(ns1, 10 * len(ns2), seed)
    if len(ns2) > 10 * len(ns1):
        ns2 = many(ns2, 10 * len(ns1), seed)

    n, gt, lt = 0, 0, 0
    for x in ns1:
        for y in ns2:
            n = n + 1
            if x > y:
                gt = gt + 1

            elif x < y:
                lt = lt + 1
    return abs(lt - gt) / n > the['cliffs']


def diffs(nums1, nums2, the):
    def func(k, nums):
        return cliffs_delta(nums.has, nums2[k].has, the), nums.txt

    return kap(nums1, func)

def add(col, x, n=1, the):
    if x != '?':
        col.n += n
        if type(col) == Sym:
            col.has[x] += n
            if col.has[x] > col.most:
                col.most, col.mode = col.has[x], x
        else:
            col.lo, col.hi = min(col.lo, x), max(col.hi, x)
            all = len(col.has)
            pos = 0
            if all < the.Max:
                pos = all + 1
            elif rand() < the.Max/col.n:
                pos = rint(1, all)
            if pos:
                col.has[pos] = x
                col.ok = False

