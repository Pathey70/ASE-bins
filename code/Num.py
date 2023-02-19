import math
from Utils import rnd


class Num:
    """Summarize stream of numbers"""
    def __init__(self, at=0, txt=""):
        self.at = at
        self.txt = txt
        self.n = self.mu = self.m2 = 0
        self.lo = math.inf
        self.hi = -math.inf
        self.w = -1 if '-' in self.txt else 1

    def add(self, n):
        if n != '?':
            self.n += 1
            d = n - self.mu
            self.mu += d/self.n     # Might have to replace with integer division
            self.m2 += d * (n - self.mu)
            self.lo = min(n, self.lo)
            self.hi = max(n, self.hi)

    def mid(self):
        """Returns mean"""
        return self.mu

    def div(self):
        """Return standard deviation"""
        return 0 if self.m2 < 0 or self.n < 2 else pow(self.m2/(self.n - 1), 0.5)

    def rnd(self, x, n):
        return x if x == '?' else rnd(x, n)

    def norm(self, n):
        if n == '?':
            return n
        return (n - self.lo) / (self.hi - self.lo + 1e-32)

    def dist(self, n1, n2):
        if n1 == '?' and n2 == '?':
            return 1
        n1, n2 = self.norm(n1), self.norm(n2)
        if n1 == "?":
            n1 = 1 if n2 < 0.5 else 0
        if n2 == "?":
            n2 = 1 if n1 < 0.5 else 0
        return abs(n1 - n2)
