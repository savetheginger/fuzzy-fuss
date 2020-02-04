import numpy as np


class Func(object):
    DEFAULT_NAME = ''

    def __init__(self, *args, formula=None, name=None, **kwargs):
        self.name = name or self.DEFAULT_NAME
        self._func = formula

    def __call__(self, *args):
        if self._func is None:
            raise NotImplementedError("Function not implemented")

        return self._func(*args)

    def inversion(self):
        return Func(formula=(lambda *args: 1 - self(*args)), name=f"{self.name} (inversion)")

    def __neg__(self):
        return self.inversion()


class Triangle(Func):
    DEFAULT_NAME = 'triangle'

    def __init__(self, a, b, c, **kwargs):
        super(Triangle, self).__init__(**kwargs)
        self.a = a
        self.b = b
        self.c = c

    def __call__(self, x):
            ba = self.b - self.a
            y1 = (x - self.a) / ba if ba else self.a <= x

            cb = self.c - self.b
            y2 = (self.c - x) / cb if cb else x <= self.c

            if isinstance(x, np.ndarray):
                r1 = np.where(y1 < y2, y1, y2)
                r2 = np.where(r1 > 0, r1, 0)

                return r2

            return max((min(y1, y2)), 0)


class Trapezoid(Func):
    DEFAULT_NAME = 'trapezoid'

    def __init__(self, a, b, c, d, **kwargs):
        super(Trapezoid, self).__init__(**kwargs)
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def __call__(self, x):
        ba = self.b - self.a
        y1 = (x - self.a) / ba if ba else self.a <= x

        dc = self.d - self.c
        y2 = (self.d - x) / dc if dc else x <= self.d

        if isinstance(x, np.ndarray):
            r1 = np.where(y1 < y2, y1, y2)
            r2 = np.where(r1 < 1, r1, 1)
            r3 = np.where(r2 > 0, r2, 0)

            return r3

        return max((min(y1, 1, y2)), 0)

