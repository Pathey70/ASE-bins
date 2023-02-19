import sys

import TestEngine
from Sym import Sym
from Num import Num
from Data import Data
from Utils import rnd, csv, rand, show

tot = 0


def count(t):
    global tot
    tot = tot + len(t)


def eg_check_syms(the):
    """Tests Sym"""
    sym = Sym()
    for x in ["a", "a", "a", "a", "b", "b", "c"]:
        sym.add(x)
    assert 'a' == sym.mid() and 1.379 == rnd(sym.div())


def eg_check_nums(the):
    """Tests Num"""
    num = Num()
    for x in [1, 1, 1, 1, 2, 2, 3]:
        num.add(x)
    assert 11 / 7 == num.mid() and 0.787 == rnd(num.div())


def eg_the(the):
    print(the)
    pass


def eg_check_rands(the):
    num1 = Num()
    num2 = Num()
    Seed = the['seed']
    for i in (1, 1001):
        x, Seed = rand(0, 1, Seed)
        num1.add(x)
    Seed = the['seed']
    for i in (1, 1001):
        x, Seed = rand(0, 1, Seed)
        num2.add(x)
    m1 = rnd(num1.mid(), 10)
    m2 = rnd(num2.mid(), 10)
    assert m1 == m2 and .5 == rnd(m1, 1)


def eg_csv(the):
    csv(the['file'], count)
    assert tot == 8 * 399


def eg_data(the):
    """Tests Data"""
    data = Data(the['file'])
    assert len(data.rows) == 398 and \
           data.cols.y[0].w == -1 and \
           data.cols.x[0].at == 0 and \
           len(data.cols.x) == 4


def eg_stats(the):
    data = Data(the['file'])
    temp = {}
    temp.update({"y": data.cols.y, "x": data.cols.x})
    for k, cols in temp.items():
        print(k, "mid", data.stats(2, cols, "mid"))
        print("", "div", data.stats(2, cols, "div"))


def eg_around(the):
    data = Data(the['file'], the)
    print(0, 0, data.rows[1].cells)
    for n, t in enumerate(data.around(data.rows[1])):

        if n % 50 == 0:
            # print(t)
            print(n, rnd(t['dist'], 2), t['row'].cells)
    pass


def eg_half(the):
    data = Data(the["file"], the)
    left, right, A, B, mid, c = data.half()
    print(len(left), len(right), len(data.rows))
    print(A.cells, c)
    print(mid.cells)
    print(B.cells)


def eg_optimize(the):
    data = Data(the["file"], the)
    show(data.sway(), "mid", data.cols.y, 1)


def eg_clone(the):
    data1 = Data(the['file'], the)
    data2 = data1.clone(data1.rows)
    assert len(data1.rows) == len(data2.rows) and \
           data1.cols.y[1].w == data2.cols.y[1].w and \
           data1.cols.x[1].at == data2.cols.x[1].at and \
           len(data1.cols.x) == len(data2.cols.x)


def eg_cluster(the):
    data = Data(the["file"], the)
    show(data.cluster(), 'mid', data.cols.y, 1)