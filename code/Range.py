from Sym import Sym


class Range:
    def __init__(self, at, txt, lo, hi):
        self.at = at
        self.txt = txt
        self.lo = lo
        self.hi = lo or hi or lo
        self.y = Sym()
