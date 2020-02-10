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

    def __repr__(self):
        return f"Function {self.name}"

    def inversion(self):
        return Func(formula=(lambda *args: 1 - self(*args)), name=f"{self.name} (inversion)")

    def __neg__(self):
        return self.inversion()

    def __add__(self, other):
        return Func(formula=(lambda *args: np.maximum(self(*args), other(*args))),
                    name=f"{self.name} OR {other.name}")

    def __mul__(self, other):
        return Func(formula=(lambda *args: np.minimum(self(*args), other(*args))),
                    name=f"{self.name} AND {other.name}")

    @staticmethod
    def _to_float(x):
        if isinstance(x, np.ndarray):
            return x.astype(float)
        return float(x)


class Triangle(Func):
    DEFAULT_NAME = 'triangle'

    def __init__(self, a, b, c, **kwargs):
        super(Triangle, self).__init__(**kwargs)
        self.a = a
        self.b = b
        self.c = c

    def __call__(self, x):
            ba = self.b - self.a
            y1 = (x - self.a) / ba if ba else self._to_float(self.a <= x)

            cb = self.c - self.b
            y2 = (self.c - x) / cb if cb else self._to_float(x <= self.c)

            return np.maximum(np.minimum(y1, y2), 0)

    def __repr__(self):
        return f"{self.name.capitalize()} function with a={self.a}, b={self.b}, c={self.c}"


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
        y1 = (x - self.a) / ba if ba else self._to_float(self.a <= x)

        dc = self.d - self.c
        y2 = (self.d - x) / dc if dc else self._to_float(x <= self.d)

        return np.maximum(np.minimum(np.minimum(y1, y2), 1.), 0.)

    def __repr__(self):
        return f"{self.name.capitalize()} function with a={self.a}, b={self.b}, c={self.c}, d={self.d}"
