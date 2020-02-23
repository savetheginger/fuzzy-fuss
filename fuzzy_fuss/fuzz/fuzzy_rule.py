import matplotlib.pyplot as plt
from collections import defaultdict
from typing import Tuple

from fuzzy_fuss.misc import plotting


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
    def prop_names(self):
        return tuple(a[0] for a in self.prop_atoms)

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

    @plotting.refine_multiplot
    def plot(self, variables, measurements=None, axes=None, fig=None, title=None, composition='coa', **kwargs):
        if axes is None:
            fig, axes = plt.subplots(1, len(self.prop_atoms)+1, sharey='all', figsize=(8, 4))

        markers = defaultdict(lambda: None, measurements)

        for i, (a_name, a_value) in enumerate(self.prop_atoms):
            variables[a_name][a_value].plot(ax=axes[i], marker=markers[a_name], **kwargs)

        conc = variables[self.conclusion[0]][self.conclusion[1]]
        if measurements:
            out_cut = self.compute_weight(variables, measurements)
            conc.plot_cut(out_cut, ax=axes[-1], composition=composition, **kwargs)
        else:
            conc.plot(ax=axes[-1], **kwargs)

        axes[0].set_ylabel("membership values")

        fig.suptitle(title or str(self))
        fig.subplots_adjust(top=0.8)

    def choose_weight(self, weights):
        statement = [weights[0]]
        for i, conn in enumerate(self.prop_connectives):
            statement.extend([conn, weights[i+1]])

        def pick(_stat):
            if len(_stat) < 2:
                return _stat[0]

            if 'or' in _stat:
                ix = _stat.index('or')
                return max(pick(_stat[:ix]), pick(_stat[ix+1:]))

            head = _stat[0]
            tail = pick(_stat[2:]) if len(_stat) > 3 else _stat[2]
            return min(head, tail)  # and

        return pick(statement)

    def compute_weight(self, variables: dict, measurements: dict):

        cuts = []
        for a_name, a_value in self.prop_atoms:
            try:
                cuts.append(variables[a_name][a_value].get_values(measurements[a_name]))
            except KeyError:
                raise ValueError(f"Missing data for variable {a_name} ({a_value})")

        return self.choose_weight(cuts)

    def evaluate(self, variables, measurements):
        weight = self.compute_weight(variables, measurements)
        return weight, self.get_conclusion(variables, weight)

    def get_conclusion(self, variables, weight=None, composition='max-min'):
        conc = variables[self.conclusion[0]][self.conclusion[1]]
        if weight is not None:
            conc = conc.cut(weight, composition=composition)

        return conc
