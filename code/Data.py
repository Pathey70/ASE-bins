from Utils import csv, kap
from Utils import cosine, many, any
from Utils import mp as mp
from Row import Row
from Cols import Cols
import math


class Data:
    """Container for ROWs, summarized into NUM or SYM columns"""

    def __init__(self, src={}, the=None):
        self.rows = list()
        self.cols = None
        self.the = the
        if type(src) == str:
            csv(src, self.add)
        else:
            mp(src, self.add)

    def add(self, t):
        """Adds rows and columns"""
        if not self.cols:
            self.cols = Cols(self.the, t)
        else:
            if type(t) == list:
                t = Row(t)
            # print(t)
            self.cols.add(t)
            self.rows.append(t)

    def clone(self, t={}):
        """Creates clone"""
        data = Data([self.cols.names], self.the)
        mp(t, data.add)
        return data

    def stats(self, nPlaces, cols=None, what='mid'):
        if not cols:
            cols = self.cols.x

        def fun(k, col):
            return col.rnd(getattr(col, what)(), nPlaces), col.txt

        return kap(cols, fun)

    def dist(self, row1, row2, cols=None):
        n = 0
        d = 0
        if not cols:
            cols = self.cols.x
        for _, col in enumerate(cols):
            n = n + 1
            d = d + col.dist(row1.cells[col.at], row2.cells[col.at]) ** self.the['p']
        return (d / n) ** (1 / self.the['p'])

    def better(self, row1, row2, s1=0, s2=0, ys=None, x=0, y=0):
        if not ys:
            ys = self.cols.y
        for col in ys:
            x = col.norm(row1.cells[col.at])
            y = col.norm(row2.cells[col.at])
            s1 = s1 - math.exp(col.w * (x - y) / len(ys))
            s2 = s2 - math.exp(col.w * (y - x) / len(ys))
        return s1 / len(ys) < s2 / len(ys)

    def around(self, row1, rows=None, cols=None):
        if not rows:
            rows = self.rows
        if not cols:
            cols = self.cols.x

        def fun(row2):
            return {'row': row2, 'dist': self.dist(row1, row2, cols)}

        return sorted(list(map(fun, rows)), key=lambda x: x['dist'])

    def half(self, rows=None, cols=None, above=None):
        def gap(r1, r2):
            return self.dist(r1, r2, cols)

        if not rows:
            rows = self.rows

        some = many(rows, self.the["Halves"], self.the['seed'])
        if self.the['Reuse']:
            A = above
        if not above or not self.the['Reuse']:
            A = any(some, self.the['seed'])
        B = self.around(A, some)[int(self.the["Far"] * len(rows)) // 1]["row"]

        def dist(row1, row2):
            return self.dist(row1, row2, cols)

        c = dist(A, B)
        left = []
        right = []

        def project(row):
            return {"row": row, "dist": cosine(dist(row, A), dist(row, B), c)}

        for n, tmp in enumerate(sorted(list(map(project, rows)), key=lambda x: x["dist"])):
            if n <= len(rows) // 2:
                left.append(tmp["row"])
                mid = tmp["row"]
            else:
                right.append(tmp["row"])
        return left, right, A, B, mid, c

    def sway(self, cols=None):
        # if not rows:
        #     rows = self.rows
        # if not min:
        #     min = len(rows) ** self.the["min"]
        # if not cols:
        #     cols = self.cols.x
        # node = {"data": self.clone(rows)}
        # if len(rows) > 2 * min:
        #     left, right, node["A"], node["B"], node["mid"], _ = self.half(rows, cols, above)
        #     if self.better(node["B"], node["A"]):
        #         left, right, node["A"], node["B"] = right, left, node["B"], node["A"]
        #     node["left"] = self.sway(left, min, cols, node["A"])
        # return node
        def worker(rows, worse, above=None):
            if len(rows) <= len(self.rows) ** self.the["min"]:
                return rows, many(worse, self.the['rest'] * len(rows))
            l, r, A, B, m, c = self.half(rows, cols, above)
            if self.better(B, A):
                l, r, A, B = r, l, B, A
            for x in r:
                worse.append(x)
            return worker(l, worse, A)

        best, rest = worker(self.rows, [])
        return self.clone(best), self.clone(rest)

    def tree(self, rows=None, min=None, cols=None, above=None):
        if not rows:
            rows = self.rows
        if not min:
            min = len(rows) ** self.the["min"]
        if not cols:
            cols = self.cols.x

        node = {"data": self.clone(rows)}
        if len(rows) > 2 * min:
            left, right, node["A"], node["B"], node["mid"], _ = self.half(rows, cols, above)
            node['left'] = self.tree(left, min, cols, node['A'])
            node['right'] = self.tree(right, min, cols, node['B'])

        return node
