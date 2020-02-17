import numpy as np


class Func(object):
    DEFAULT_NAME = ''

    def __init__(self, *args, formula=None, name=None, support=None, **kwargs):
        self.name = name or self.DEFAULT_NAME
        self._func = formula
        self._support = support

    def __call__(self, *args):
        if self._func is None:
            raise NotImplementedError("Function not implemented")

        return self._func(*args)

    def __repr__(self):
        return f"Function {self.name}"

    @property
    def support(self):
        if not self._support:
            raise NotImplementedError(f"Support of a fuzzy membership function {type(self)} is not defined")
        return self._support

    def inversion(self):
        return Func(formula=(lambda *args: 1 - self(*args)), name=f"{self.name} (inversion)",
                    support=self.support)  # TODO: correct support - add core

    def __neg__(self):
        return self.inversion()

    def __add__(self, other):
        if isinstance(other, Func):
            s_low = min(self.support[0], other.support[0])
            s_high = max(self.support[1], other.support[1])

            return Func(formula=(lambda *args: np.maximum(self(*args), other(*args))),
                        name=f"{self.name} OR {other.name}",
                        support=(s_low, s_high))

        raise TypeError(f"Expected type Func, got {type(other)}")

    def __mul__(self, other):
        if isinstance(other, Func):
            s_low = max(self.support[0], other.support[0]),
            s_high = min(self.support[1], other.support[1])

            return Func(formula=(lambda *args: np.minimum(self(*args), other(*args))),
                        name=f"{self.name} AND {other.name}",
                        support=tuple(sorted((s_low, s_high))))

        if isinstance(other, (int, float)):
            return Func(formula=lambda *args: other * self(*args),
                        name=f"{other} * {self.name}",
                        support=self.support)

        raise TypeError(f"Expected type Func, got {type(other)}")

    @staticmethod
    def _to_float(x):
        if isinstance(x, np.ndarray):
            return x.astype(float)
        return float(x)

    def make(self, **kwargs):
        defaults = dict(name=self.name, support=self.support, formula=self.__call__)
        kwargs = {**defaults, **kwargs}
        return Func(**kwargs)

    def cut(self, level):
        if not isinstance(level, float):
            raise TypeError(f"Cut level should be a float (got {type(level)})")

        return Func(formula=(lambda x: np.minimum(self(x), level)),
                    support=self.support,
                    name=f"{self.name} cut at {level}")


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

    @property
    def support(self):
        return self.a, self.c


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

    @property
    def support(self):
        return self.a, self.d
