import numpy as np
import matplotlib.pyplot as plt


class Fuzz(object):
    def get_values(self, data, **kwargs):
        raise NotImplementedError(f"'get_values' function of {self.__class__.__name__} is not implemented")

    def plot(self, data, ax=None, **kwargs):
        values = self.get_values(data)
        if ax is None:
            fig, ax = plt.subplots()
        ax.plot(data, values, **kwargs)


class FuzzDict(dict):
    def plot(self, data, names=None, title=None):
        if names is None:
            names = self.keys()

        fig, ax = plt.subplots()

        for name in names:
            self[name].plot(data, ax=ax, label=name)

        if title:
            ax.set_title(title)

        ax.set_xlabel("x values")
        ax.set_ylabel("membership values")

        ax.legend(fancybox=True, framealpha=0.5)

        plt.show()

    def plot_range(self, start, stop, step, **kwargs):
        data = np.arange(start, stop, step)
        self.plot(data, **kwargs)

