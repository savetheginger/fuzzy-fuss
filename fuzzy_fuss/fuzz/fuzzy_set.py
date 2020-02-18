import numpy as np
from copy import deepcopy
from collections import abc

from fuzzy_fuss.misc import plotting
from fuzzy_fuss.fuzz.func import Func
from fuzzy_fuss.fuzz.defuzzifier import Defuzzifier


class FuzzySet(object):
    def __init__(self, func: Func = None, variable_name=None, value_name=None):
        self._mf = func
        self.variable_name = variable_name
        self.value_name = value_name

    def _setup_dict(self):
        return dict(variable_name=self.variable_name,
                    value_name=self.value_name)

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

    @plotting.refine_plot()
    def plot_cut(self, cut_level, ax, method='max-min', **kwargs):
        self.plot(ax=ax, **kwargs)
        self.cut(cut_level, method).plot(ax=ax, **kwargs)
        ax.axhline(cut_level, lw=1, color='k', linestyle=':', label=f"{cut_level:.2f}")
        ax.legend()

    @plotting.refine_plot()
    def plot(self, ax, data=None, shade=0.2, margin=0, title=None, marker=None, **kwargs):
        if data is None:
            data = np.arange(*self.get_support(margin=margin))

        values = self.get_values(data)

        border, = ax.plot(data, values, **kwargs)
        if shade:
            ax.fill_between(data, values, facecolor=border.get_color(), alpha=shade, zorder=1)

        if marker:
            marker_val = self.get_values(marker)
            ax.axvline(marker, lw=1, color='k', linestyle='-.', label="Meas.")
            ax.axhline(marker_val, lw=1, color='k', linestyle=':')
            ax.plot(marker, marker_val, '*', color='crimson', markersize=10)
            ax.legend()

        if title:
            ax.set_title(title)

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
        comp.value_name = f"NOT ({self.value_name})"
        return comp

    def __radd__(self, other):
        if other == 0:
            return self

        return self.__add__(other)

    def _var_check(self, other):
        if self.variable_name and other.variable_name and self.variable_name != other.variable_name:
            raise ValueError(f"Unmatching variable names: {self.variable_name} and {other.variable_name}")

    def __add__(self, other):
        if isinstance(other, FuzzySet):
            self._var_check(other)
            return self._make(func=self.membership_function + other.membership_function,
                              value_name=f"({self.value_name}) OR ({other.value_name})")

        else:
            raise TypeError(f"item not an instance of FuzzySet (got {type(other)})")

    def __mul__(self, other):
        if isinstance(other, FuzzySet):
            self._var_check(other)
            return self._make(func=self.membership_function * other.membership_function,
                              value_name=f"({self.value_name}) AND ({other.value_name})")

        if isinstance(other, (int, float)):
            return self._make(func=self.membership_function * other,
                              value_name=f"{other} * {self.value_name}")

        else:
            raise TypeError(f"__mul__ undefined for {type(self)} and {type(other)}")

    def __neg__(self):
        return self.complement()

    def _make(self, **kwargs):
        params = {**self._setup_dict(), **kwargs}
        return FuzzySet(**params)

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

    def defuzzify(self, **kwargs):
        return Defuzzifier.defuzzify(self.membership_function, **kwargs)

    def rename(self, variable_name=None, value_name=None, inplace=True):
        if variable_name:
            self.variable_name = variable_name

        if value_name:
            self.value_name = value_name

        if not inplace:
            return self
