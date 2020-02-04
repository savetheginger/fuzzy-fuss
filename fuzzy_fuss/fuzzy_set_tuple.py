from collections import namedtuple
import numpy as np
import intervals as iv

from fuzzy_fuss.fuzz import Fuzz, FuzzDict


class FuzzySetTuple(Fuzz, namedtuple('fuzzy4tuple', ['a', 'b', 'alpha', 'beta'])):
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

    def get_values(self, data, **kwargs):
        return np.array(tuple(map(lambda x: self.get_value(x), data)))


if __name__ == '__main__':
    fsets = FuzzDict()
    fsets['small'] = FuzzySetTuple(2, 4, 2, 3)
    fsets['medium'] = FuzzySetTuple(7, 10, 2, 1)
    fsets['none'] = FuzzySetTuple(0, 0, 0, 0)
    fsets['strict'] = FuzzySetTuple(3, 3, 0, 0)

    fsets.plot_range(0, 10, 0.1, title="Fuzzy sets", shade=0, kwargs_by_name={'small': {'shade': 0.2}})

