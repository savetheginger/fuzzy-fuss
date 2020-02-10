from collections import namedtuple

from fuzzy_fuss.fuzz.fuzz import FuzzySet, FuzzyVariable
from fuzzy_fuss.fuzz.func import Trapezoid


class Fuzzy4Tuple(FuzzySet, namedtuple('fuzzy4tuple', ['a', 'b', 'alpha', 'beta'])):
    def __init__(self, *args, **kwargs):
        super(Fuzzy4Tuple, self).__init__()

        self._mf = Trapezoid(self.a - self.alpha,
                             self.a,
                             self.b,
                             self.b + self.beta)

    @staticmethod
    def from_points(v1, v2, v3, v4):
        if not v1 <= v2 <= v3 <= v4:
            raise ValueError("Values are not in order")

        return Fuzzy4Tuple(v2, v3, v2 - v1, v4 - v3)


if __name__ == '__main__':
    fsets = FuzzyVariable()
    fsets['small'] = Fuzzy4Tuple(2, 4, 2, 3)
    fsets['medium'] = Fuzzy4Tuple(7, 10, 2, 1)
    fsets['none'] = Fuzzy4Tuple(0, 0, 0, 0)
    fsets['strict'] = Fuzzy4Tuple(3, 3, 0, 0)

    fsets.plot_range(0, 10, 0.1, title="Fuzzy sets", shade=0, kwargs_by_name={'small': {'shade': 0.2}})

    print(fsets.get_values([0, 2, 4, 10]))

