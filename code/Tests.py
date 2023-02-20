import sys

import TestEngine
from Sym import Sym
from Num import Num
from Data import Data
from Utils import rnd, csv, rand, show, rint

tot = 0


def count(t):
    global tot
    tot = tot + len(t)


def eg_syms(the):
    """Tests Sym"""
    sym = Sym()
    for x in ["a", "a", "a", "a", "b", "b", "c"]:
        sym.add(x)
    print(sym.mid(),rnd(sym.div()))
    assert 'a' == sym.mid() and 1.379 == rnd(sym.div())


def eg_nums(the):
    """Tests Num"""
    num1 = Num()
    num2 = Num()
    Seed = the['seed']
    for i in range(1, 1001):
        x, Seed = rand(0, 1, Seed)
        num1.add(x)
    Seed = the['seed']
    for i in range(1, 1001):
        x, Seed = rand(0, 1, Seed)
        num2.add(x**2)
    m1 = rnd(num1.mid(), 1)
    m2 = rnd(num2.mid(), 1)
    d1 = rnd(num1.mid(), 1)
    d2 = rnd(num2.mid(), 1)
    print(1,m1,d1)
    print(2,m2,d2)
    assert num1.mid() == num1.mid() and .5 == m1


def eg_the(the):
    print(the)
    pass


def eg_rand(the):
    t=[]
    u=[]
    Seed = the['seed']
    for i in range(1, 1001):
        t.append(rint(0,100))
    Seed = the['seed']
    for i in range(1, 1001):
        u.append(rint(0,100))
    for i in range(1, 1000):
        assert t[i] == u[i]



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


def eg_half(the):
    data = Data(the["file"], the)
    left, right, A, B, mid, c = data.half()
    print(len(left), len(right), len(data.rows))
    print(A.cells, c)
    print(mid.cells)
    print(B.cells)


def eg_clone(the):
    data1 = Data(the['file'], the)
    data2 = data1.clone(data1.rows)
    assert len(data1.rows) == len(data2.rows) and \
           data1.cols.y[1].w == data2.cols.y[1].w and \
           data1.cols.x[1].at == data2.cols.x[1].at and \
           len(data1.cols.x) == len(data2.cols.x)
