import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict
from copy import deepcopy


class Fuzz(object):
    def __init__(self):
        self._inverted = False
        self._func = None

    @property
    def func(self):
        if not self._func:
            raise NotImplementedError("Function not defined")

        if self._inverted:
            return lambda x: 1 - self._func(x)

        return self._func


    def get_values(self, data, **kwargs):
        raise NotImplementedError(f"'get_values' function of {self.__class__.__name__} is not implemented")

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
        self._inverted = not self._inverted

    def complement(self):
        comp = deepcopy(self)
        comp.invert()
        return comp


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
