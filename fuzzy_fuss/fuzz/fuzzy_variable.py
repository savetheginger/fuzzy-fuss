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

    def plot(self, data, names=None, title=None, kwargs_by_name: dict = None, **kwargs,):
        if names is None:
            names = self.keys()

        kwargs_by_name = defaultdict(lambda: {}, **(kwargs_by_name or {}))

        fig, ax = plt.subplots()

        for name in names:
            self[name].plot(data, ax=ax, label=name, **{**kwargs, **kwargs_by_name[name]})

        ax.set_title(title or self.name)

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
