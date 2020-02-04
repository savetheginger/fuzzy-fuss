import numpy as np


class Func(object):
    DEFAULT_NAME = ''

    def __init__(self, *args, name=None, **kwargs):
        self.name = name or self.DEFAULT_NAME

    def __call__(self, *args):
        raise NotImplementedError("Function not implemented")

    def inversion(self):
        return self.__class__.__new__(lambda *args: 1 - self(*args))

    def __neg__(self):
        return self.inversion()


class AnyFunc(Func):
    def __init__(self, formula, **kwargs):
        super(AnyFunc, self).__init__(**kwargs)
        self._func = formula

    def __call__(self, *args):
        return self._func(*args)


class Triangle(Func):
    DEFAULT_NAME = 'triangle'

    def __init__(self, a, b, c, **kwargs):
        super(Triangle, self).__init__(**kwargs)
        self.a = a
        self.b = b
        self.c = c

    def __call__(self, x):
            y1 = (x - self.a) / (self.b - self.a)
            y2 = (self.c - x) / (self.c - self.b)

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
        y1 = (x - self.a) / (self.b - self.a)
        y2 = (self.d - x) / (self.d - self.c)

        if isinstance(x, np.ndarray):
            r1 = np.where(y1 < y2, y1, y2)
            r2 = np.where(r1 < 1, r1, 1)
            r3 = np.where(r2 > 0, r2, 0)

            return r3

        return max((min(y1, 1, y2)), 0)

