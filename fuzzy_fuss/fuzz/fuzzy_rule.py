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

    def plot(self, variables, measurements=None, axes=None, fig=None, title=None, **kwargs):
        if axes is None:
            fig, axes = plt.subplots(1, len(self.prop_atoms)+1, sharey='all', figsize=(8, 4))

        markers = defaultdict(lambda: None, measurements)

        for i, (a_name, a_value) in enumerate(self.prop_atoms):
            variables[a_name][a_value].plot(ax=axes[i], title=f"{a_name}: {a_value}", marker=markers[a_name], **kwargs)

        conc = variables[self.conclusion[0]][self.conclusion[1]]
        if measurements:
            out_cut = self.compute_weight(variables, measurements)
            conc.plot_cut(out_cut, ax=axes[-1], **kwargs)
        else:
            conc.plot(ax=axes[-1], **kwargs)

        for ax in axes:
            ax.grid(color='lightgray')
            ax.axhline(0, color='darkgray', zorder=1, lw=3)
            ax.axhline(1, color='dimgray', zorder=1, lw=1)
            ax.set_xlabel("x values")
        axes[0].set_ylabel("membership values")

        fig.suptitle(title or str(self))
        fig.subplots_adjust(top=0.8)

        plt.show()

    def compute_weight(self, variables: dict, measurements: dict):
        conn = set(self.prop_connectives)
        if len(conn) > 1:
            raise RuntimeError("Rule evaluation for multiple connectives types is not implemented")  # TODO

        conn = tuple(conn)[0]

        cuts = []
        for a_name, a_value in self.prop_atoms:
            try:
                cuts.append(variables[a_name][a_value].get_values(measurements[a_name]))
            except KeyError:
                raise ValueError(f"Missing data for variable {a_name}")

        output_cut = min(cuts) if conn.lower() == 'and' else max(cuts)

        return output_cut

    def evaluate(self, variables, measurements):
        weight = self.compute_weight(variables, measurements)
        return weight, self.get_conclusion(variables, weight)

    def get_conclusion(self, variables, weight=None):
        conc = variables[self.conclusion[0]][self.conclusion[1]]
        if weight:
            conc = conc * weight

        return conc


class RuleSet(dict):
    def __init__(self):
        super(RuleSet, self).__init__()

    def __setitem__(self, key, value):
        self._check_rule_type(value)
        super(RuleSet, self).__setitem__(key, value)

    def __iter__(self):
        yield from set(self.values())

    @staticmethod
    def _check_rule_type(value):
        if not isinstance(value, Rule):
            raise TypeError(f"'value' must be of type Rule (got {type(value)})")

    def add_rule(self, rule: Rule):
        self._check_rule_type(rule)
        self[rule.name] = rule

    def get_partial_conclusions(self, variables, weights=None):
        weights = weights or defaultdict(lambda: None)
        conclusions = [rule.get_conclusion(variables, weights[rule.name]) for rule in self]
        return conclusions

    def sum(self, variables, weights):
        conclusions = self.get_partial_conclusions(variables, weights)

        conc_sum = conclusions[0]
        for conc in conclusions:
            conc_sum += conc

        return conc_sum

    def compute_weights(self, variables, measurements):
        return {rule.name: rule.compute_weight(variables, measurements) for rule in self}

    def evaluate(self, variables: dict, measurements: dict):
        # TODO: this assumes the conclusion of each rule is the same variable type
        weights = self.compute_weights(variables, measurements)

        compound_conclusion = self.sum(variables, weights)

        return compound_conclusion

    def plot_eval(self, variables: dict, measurements: dict):
        weights = self.compute_weights(variables, measurements)
        conclusions = self.get_partial_conclusions(variables)
        conclusions_cut = self.get_partial_conclusions(variables, weights)

        rules = list(self)

        fig, axes = plt.subplots(1, len(self)+1, figsize=(15, 4), sharey='all', sharex='all')
        for i, conc in enumerate(conclusions):
            conc.plot_cut(ax=axes[i], cut=weights[rules[i].name], title=f"{rules[i].name}: {rules[i].conclusion}")
            axes[i].grid(color='lightgray')

        for i, conc in enumerate(conclusions_cut):
            conc.plot(ax=axes[-1], shade=0.1, label=rules[i].name)
        self.sum(variables, weights).plot(ax=axes[-1], shade=0, zorder=1,
                                          title="Aggregate conclusion", label="Aggregate")
        axes[-1].grid(color='lightgray')

        axes[-1].legend(fancybox=True, framealpha=0.5)
        plt.show()
