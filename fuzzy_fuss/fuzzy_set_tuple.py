from collections import namedtuple
import numpy as np
import matplotlib.pyplot as plt
import intervals as iv


class FuzzySetTuple(namedtuple('fuzzy4tuple', ['a', 'b', 'alpha', 'beta'])):
    def __init__(self, *args, **kwargs):
        super(FuzzySetTuple, self).__init__()

        bounds = (self.a - self.alpha,
                  self.a,
                  self.b,
                  self.b + self.beta)

        self._intervals = iv.IntervalDict()
        self._intervals[iv.open(-iv.inf, bounds[0])] = lambda x: 0
        self._intervals[iv.closedopen(bounds[0], bounds[1])] = lambda x: (x - self.a + self.alpha)/self.alpha
        self._intervals[iv.closed(bounds[1], bounds[2])] = lambda x: 1
        self._intervals[iv.openclosed(bounds[2], bounds[3])] = lambda x: (self.b + self.beta - x)/self.beta
        self._intervals[iv.open(bounds[3], iv.inf)] = lambda x: 0

    @property
    def intervals(self):
        return self._intervals

    def get_value(self, x):
        return self._intervals[x](x)

    def get_values(self, data):
        return np.array(tuple(map(lambda x: self.get_value(x), data)))

    def plot(self, data, ax=None, **kwargs):
        values = self.get_values(data)
        if ax is None:
            fig, ax = plt.subplots()
        ax.plot(data, values, **kwargs)


if __name__ == '__main__':
    small = FuzzySetTuple(2, 4, 2, 3)
    medium = FuzzySetTuple(7, 10, 2, 1)
    none = FuzzySetTuple(0, 0, 0, 0)
    strict = FuzzySetTuple(3, 3, 0, 0)

    xdata = np.arange(0, 10, 0.1)
    fig, ax = plt.subplots()
    small.plot(xdata, ax=ax, label='small')
    medium.plot(xdata, ax=ax, label='medium')
    none.plot(xdata, ax=ax, label='none')
    strict.plot(xdata, ax=ax, label='strict')
    ax.legend(fancybox=True, framealpha=0.5)
    plt.show()

