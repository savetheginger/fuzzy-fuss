from collections import namedtuple
import numpy as np
import matplotlib.pyplot as plt


class FuzzySetTuple(namedtuple('fuzzy4tuple', ['a', 'b', 'alpha', 'beta'])):
    def __init__(self, *args, **kwargs):
        super(FuzzySetTuple, self).__init__()

        self._bounds = (self.a - self.alpha,
                        self.a,
                        self.b,
                        self.b + self.beta)

        self._evaluators = (lambda x: 0,
                            lambda x: (x - self.a + self.alpha)/self.alpha,
                            lambda x: 1,
                            lambda x: (self.b + self.beta - x)/self.beta,
                            lambda x: 0)

    def get_evaluators(self, data):
        return np.array(self._evaluators)[np.searchsorted(self._bounds, data)]

    def get_values(self, data):
        evaluators = self.get_evaluators(data)
        return np.array(tuple(map(lambda x: x[0](x[1]), zip(evaluators, data))))

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

