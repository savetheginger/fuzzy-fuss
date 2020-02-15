import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict

from fuzzy_fuss.fuzz.fuzzy_set import FuzzySet


class FuzzyVariable(dict):
    def __init__(self, name):
        super(FuzzyVariable, self).__init__()
        self.name = name

    def __setitem__(self, key, value):
        if not isinstance(value, FuzzySet):
            raise TypeError(f"'{key}': value must be a FuzzySet object (got {type(value)})")

        super(FuzzyVariable, self).__setitem__(key, value)

    def __repr__(self):
        k = [f"'{key}'" for key in self.keys()]
        return f"Fuzzy variable with values: {', '.join(k) if k else '(none yet)'}"

    def get_support(self, margin=0):
        s_low = min(v.support[0] for v in self.values()) - margin
        s_high = max(v.support[1] for v in self.values()) + margin
        return s_low, s_high

    def plot(self, data, names=None, title=None, kwargs_by_name: dict = None, **kwargs,):
        if names is None:
            names = self.keys()

        kwargs_by_name = defaultdict(lambda: {}, **(kwargs_by_name or {}))

        fig, ax = plt.subplots()

        for name in names:
            self[name].plot(data, ax=ax, label=name, **{**kwargs, **kwargs_by_name[name]})

        ax.grid(color='lightgray')
        ax.axhline(0, color='darkgray', zorder=1, lw=3)
        ax.axhline(1, color='dimgray', zorder=1, lw=1)

        ax.set_title(title or f"Fuzzy variable '{self.name}'")

        ax.set_xlabel("x values")
        ax.set_ylabel("membership values")

        ax.legend(fancybox=True, framealpha=0.5)

        plt.show()

    def plot_range(self, *args, margin=10, **kwargs):
        args = args or self.get_support(margin=margin)
        data = np.arange(*args)
        self.plot(data, **kwargs)

    def get_values(self, data):
        return pd.DataFrame({name: self[name].get_values(data) for name in self.keys()},
                            index=data, columns=self.keys())
