import numpy as np
import pandas as pd
from collections import defaultdict

from fuzzy_fuss.misc import plotting
from fuzzy_fuss.fuzz.fuzzy_set import FuzzySet


class FuzzyVariable(dict):
    def __init__(self, name):
        super(FuzzyVariable, self).__init__()
        self.name = name

    def __setitem__(self, key, value):
        if not isinstance(value, FuzzySet):
            raise TypeError(f"'{key}': value must be a FuzzySet object (got {type(value)})")

        if value.variable_name and value.variable_name != self.name:
            raise ValueError(f"Unmatching variable names: '{self.name}' and '{value.variable_name}'")

        super(FuzzyVariable, self).__setitem__(key or value.value_name, value)
        if not value.value_name:
            value.value_name = key
        if not value.variable_name:
            value.variable_name = self.name

    def add_set(self, value):
        self.__setitem__(None, value)

    def __repr__(self):
        k = [f"'{key}'" for key in self.keys()]
        return f"Fuzzy variable with values: {', '.join(k) if k else '(none yet)'}"

    def get_support(self, margin=0):
        s_low = min(v.support[0] for v in self.values()) - margin
        s_high = max(v.support[1] for v in self.values()) + margin
        return s_low, s_high

    @plotting.refine_plot(show_default=True)
    def plot(self, data, ax, names=None, title=None, kwargs_by_name: dict = None, **kwargs,):
        if names is None:
            names = self.keys()

        kwargs_by_name = defaultdict(lambda: {}, **(kwargs_by_name or {}))

        for name in names:
            self[name].plot(ax=ax, data=data, label=name, **{**kwargs, **kwargs_by_name[name]})

        ax.set_title(title or f"Fuzzy variable '{self.name}'")

        ax.set_ylabel("membership values")

        ax.legend()

    def plot_range(self, *args, margin=10, **kwargs):
        args = args or self.get_support(margin=margin)
        data = np.arange(*args)
        self.plot(data, **kwargs)

    def get_values(self, data):
        return pd.DataFrame({name: self[name].get_values(data) for name in self.keys()},
                            index=data, columns=self.keys())
