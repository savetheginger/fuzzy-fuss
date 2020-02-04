from collections import namedtuple

from fuzzy_fuss.fuzz import Fuzz, FuzzDict
from fuzzy_fuss.func import Trapezoid


class FuzzySetTuple(Fuzz, namedtuple('fuzzy4tuple', ['a', 'b', 'alpha', 'beta'])):
    def __init__(self, *args, **kwargs):
        super(FuzzySetTuple, self).__init__()

        self._func = Trapezoid(self.a - self.alpha,
                               self.a,
                               self.b,
                               self.b + self.beta)

    @staticmethod
    def from_points(v1, v2, v3, v4):
        if not v1 <= v2 <= v3 <= v4:
            raise ValueError("Values are not in order")

        return FuzzySetTuple(v2, v3, v2-v1, v4-v3)


if __name__ == '__main__':
    fsets = FuzzDict()
    fsets['small'] = FuzzySetTuple(2, 4, 2, 3)
    fsets['medium'] = FuzzySetTuple(7, 10, 2, 1)
    fsets['none'] = FuzzySetTuple(0, 0, 0, 0)
    fsets['strict'] = FuzzySetTuple(3, 3, 0, 0)

    fsets.plot_range(0, 10, 0.1, title="Fuzzy sets", shade=0, kwargs_by_name={'small': {'shade': 0.2}})

    print(fsets.get_values([0, 2, 4, 10]))

