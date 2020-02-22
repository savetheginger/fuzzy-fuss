import numpy as np

from fuzzy_fuss.fuzz.func import Func


class Defuzzifier(object):
    METHODS = ('coa', 'som', 'lom', 'mom')

    @staticmethod
    def defuzzify(func: Func, grid_size=1, method='coa'):
        if not isinstance(func, Func):
            raise TypeError(f"Argument is not a Func object (got {type(func)})")

        method = method.lower()

        if method in Defuzzifier.METHODS:
            return getattr(Defuzzifier, f'_defuzzify_{method}')(*Defuzzifier.generate_data(func, grid_size))
        else:
            raise ValueError(f"Unknown defuzzification method code: {method}")

    @staticmethod
    def _defuzzify_coa(xdata, ydata):
        """Calculate centroid of area"""

        return np.average(xdata, weights=ydata)

    @staticmethod
    def _defuzzify_som(xdata, ydata):
        """Smallest of maximum"""

        return Defuzzifier._get_max_range(xdata, ydata).min()

    @staticmethod
    def _defuzzify_lom(xdata, ydata):
        """Largest of maximum"""

        return Defuzzifier._get_max_range(xdata, ydata).max()

    @staticmethod
    def _defuzzify_mom(xdata, ydata):
        """Largest of maximum"""

        return Defuzzifier._get_max_range(xdata, ydata).mean()

    @staticmethod
    def generate_data(func, grid_size):
        xdata = np.arange(*func.support, grid_size)
        ydata = func(xdata)
        return xdata, ydata

    @staticmethod
    def _get_max_range(xdata, ydata):
        return xdata[np.where(ydata == ydata.max())]