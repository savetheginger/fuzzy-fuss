import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
from collections import abc

from fuzzy_fuss.fuzz.func import Func


class FuzzySet(object):
    def __init__(self, func: Func = None):
        self._mf = func

    @property
    def membership_function(self):
        if not self._mf:
            raise NotImplementedError("Function not defined")

        return self._mf

    def get_values(self, data, **kwargs):
        if isinstance(data, (abc.Sequence, abc.Iterable)):
            data = np.array(data)
        return self.membership_function(data)

    def plot(self, data, ax=None, shade=0.2, **kwargs):
        values = self.get_values(data)
        if ax is None:
            fig, ax = plt.subplots()

        border, = ax.plot(data, values, **kwargs)
        if shade:
            ax.fill_between(data, values, facecolor=border.get_color(), alpha=shade, zorder=1)

    def issubset(self, other, val_range=None, data=None):
        if data is None and val_range is None:
            raise ValueError("Either data or val_range must be provided")

        if data is None:
            data = np.arange(*val_range)

        return self.get_values(data) <= other.get_values(data)

    def invert(self):
        self._mf = - self._mf

    def complement(self):
        comp = deepcopy(self)
        comp.invert()
        return comp

    def __add__(self, other):
        return FuzzySet(self.membership_function + other.membership_function)

    def __mul__(self, other):
        return FuzzySet(self.membership_function * other.membership_function)

    def __neg__(self):
        return self.complement()

    def cut(self, cut: float, method='max-min'):
        if not isinstance(cut, float):
            raise TypeError(f"Cut level must be a float (got {type(cut)})")

        if not 0 <= cut <= 1:
            raise ValueError(f"Cut level must be between 0 and 1 (got {cut})")

        if method == 'max-min':
            func = self._min(cut)
        elif method == 'max-product':
            func = self._product(cut)
        else:
            raise ValueError(f"Unknown cut method: {method}")

        return FuzzySet(func)

    def _min(self, cut: float):
        """For max-min composition: perform an alpha-cut on the function"""

        return lambda x: np.minimum(self.membership_function(x), cut)

    def _product(self, cut):
        """For max-product composition: multiply the function by the max level"""

        return self.membership_function * cut

