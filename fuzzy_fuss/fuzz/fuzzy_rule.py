import matplotlib.pyplot as plt
from collections import defaultdict

from typing import Tuple


class Atom(tuple):
    PATTERN = r"\s*(?P<variable>\w+) (?:is|will be) (?P<value>\w+)\s*"

    def __init__(self, vals):
        if len(vals) != 2:
            raise ValueError(f"Expected a length 2 argument, got length {len(vals)}: {vals}")

    def __repr__(self):
        return f"({self[0]} = {self[1]})"


class Rule(object):
    def __init__(self, name: str, prop_atoms: Tuple[Atom], prop_connectives, conclusion: Atom):
        la = len(prop_atoms)
        lc = len(prop_connectives)
        if not lc == la - 1:
            raise ValueError(f"Improper number of connectives for {la} atoms: expected {la - 1}, got {lc}")

        self.name = name
        self.prop_atoms = prop_atoms
        self.prop_connectives = prop_connectives
        self.conclusion = conclusion

    @property
    def all_atoms(self):
        return self.prop_atoms + (self.conclusion,)

    def __repr__(self):
        pc = self.prop_connectives
        pa = self.prop_atoms

        prop = str(pa[0])

        for i in range(len(self.prop_connectives)):
            prop += f" {pc[i].upper()}"
            prop += f" {str(pa[i+1])}"

        return f"{self.name}: {prop} => {str(self.conclusion)}"

    def plot(self, variables, measurements=None, axes=None, fig=None, title=None):
        if axes is None:
            fig, axes = plt.subplots(1, len(self.prop_atoms)+1, sharey='all', figsize=(8, 4))

        markers = defaultdict(lambda: None, measurements)

        for i, (a_name, a_value) in enumerate(self.all_atoms):
            variables[a_name][a_value].plot(ax=axes[i], title=f"{a_name}: {a_value}", marker=markers[a_name])

        for ax in axes:
            ax.grid(color='lightgray')
            ax.axhline(0, color='darkgray', zorder=1, lw=3)
            ax.axhline(1, color='dimgray', zorder=1, lw=1)
            ax.set_xlabel("x values")
        axes[0].set_ylabel("membership values")

        fig.suptitle(title or str(self))
        fig.subplots_adjust(top=0.8)

        plt.show()

