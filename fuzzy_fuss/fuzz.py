import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict
from copy import deepcopy
from collections import abc

from fuzzy_fuss.func import Func


class Fuzz(object):
    def __init__(self, func: Func = None):
        self._func = func

    @property
    def func(self):
        if not self._func:
            raise NotImplementedError("Function not defined")

        return self._func

    def get_values(self, data, **kwargs):
        if isinstance(data, (abc.Sequence, abc.Iterable)):
            data = np.array(data)
        return self.func(data)

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
        self._func = - self._func

    def complement(self):
        comp = deepcopy(self)
        comp.invert()
        return comp

    def __add__(self, other):
        return Fuzz(self.func + other.func)

    def __mul__(self, other):
        return Fuzz(self.func * other.func)

    def __neg__(self):
        return self.complement()


class FuzzDict(dict):
    def plot(self, data, names=None, title=None, kwargs_by_name: dict = None, **kwargs,):
        if names is None:
            names = self.keys()

        kwargs_by_name = defaultdict(lambda: {}, **(kwargs_by_name or {}))

        fig, ax = plt.subplots()

        for name in names:
            self[name].plot(data, ax=ax, label=name, **{**kwargs, **kwargs_by_name[name]})

        if title:
            ax.set_title(title)

        ax.set_xlabel("x values")
        ax.set_ylabel("membership values")

        ax.legend(fancybox=True, framealpha=0.5)

        plt.show()

    def plot_range(self, start, stop, step, **kwargs):
        data = np.arange(start, stop, step)
        self.plot(data, **kwargs)

    def get_values(self, data):
        return pd.DataFrame({name: self[name].get_values(data) for name in self.keys()},
                            index=data, columns=self.keys())
