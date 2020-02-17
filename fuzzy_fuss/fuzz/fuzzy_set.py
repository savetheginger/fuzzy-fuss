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

    @property
    def support(self):
        return self._mf.support

    def get_support(self, margin=0):
        return self.support[0] - margin, self.support[1] + margin

    def get_values(self, data, **kwargs):
        if isinstance(data, (abc.Sequence, abc.Iterable)):
            data = np.array(data)
        return self.membership_function(data)

    def plot_cut(self, cut, ax=None, show=False, method='max-min', **kwargs):
        if ax is None:
            fig, ax = plt.subplots()

        self.plot(ax=ax, **kwargs)
        self.cut(cut, method).plot(ax=ax, **kwargs)
        ax.axhline(cut, lw=1, color='k', linestyle=':', label=f"{cut:.2f}")
        ax.legend(fancybox=True, framealpha=0.5)

        if show:
            plt.show()

    def plot(self, data=None, ax=None, shade=0.2, margin=0, title=None, marker=None, show=False, **kwargs):
        if data is None:
            data = np.arange(*self.get_support(margin=margin))

        values = self.get_values(data)

        if ax is None:
            fig, ax = plt.subplots()

        border, = ax.plot(data, values, **kwargs)
        if shade:
            ax.fill_between(data, values, facecolor=border.get_color(), alpha=shade, zorder=1)

        if marker:
            marker_val = self.get_values(marker)
            ax.axvline(marker, lw=1, color='k', linestyle='-.', label="Meas.")
            ax.axhline(marker_val, lw=1, color='k', linestyle='--')
            ax.plot(marker, marker_val, '*', color='crimson', markersize=10)
            ax.legend(fancybox=True, framealpha=0.5)

        if title:
            ax.set_title(title)

        if show:
            plt.show()

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

    def __radd__(self, other):
        if other == 0:
            return self

        return self.__add__(other)

    def __add__(self, other):
        if isinstance(other, FuzzySet):
            return FuzzySet(self.membership_function + other.membership_function)

        else:
            raise TypeError(f"item not an instance of FuzzySet (got {type(other)})")

    def __mul__(self, other):
        if isinstance(other, FuzzySet):
            return FuzzySet(self.membership_function * other.membership_function)
        if isinstance(other, (int, float)):
            return FuzzySet(self.membership_function * other)
        else:
            raise TypeError(f"__mul__ undefined for {type(self)} and {type(other)}")

    def __neg__(self):
        return self.complement()

    def cut(self, cut: float, method='max-min'):
        if not isinstance(cut, float):
            raise TypeError(f"Cut level must be a float (got {type(cut)})")

        if not 0 <= cut <= 1:
            raise ValueError(f"Cut level must be between 0 and 1 (got {cut})")

        if method == 'max-min':
            func = self._mf.cut(cut)
        elif method == 'max-product':
            func = self.membership_function * cut
        else:
            raise ValueError(f"Unknown cut method: {method}")

        return FuzzySet(func)

