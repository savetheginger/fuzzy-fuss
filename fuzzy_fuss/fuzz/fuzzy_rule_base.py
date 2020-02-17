import matplotlib.pyplot as plt
from collections import defaultdict

from fuzzy_fuss.misc import plotting
from fuzzy_fuss.fuzz.fuzzy_rule import Rule


class RuleBase(dict):
    def __init__(self, variables):
        self.variables = variables
        super(RuleBase, self).__init__()

    def __setitem__(self, key, value):
        self._check_rule_type(value)
        super(RuleBase, self).__setitem__(key, value)

    def __iter__(self):
        for key in sorted(self.keys()):  # sort by rule name
            yield self[key]

    @staticmethod
    def _check_rule_type(value):
        if not isinstance(value, Rule):
            raise TypeError(f"'value' must be of type Rule (got {type(value)})")

    def add_rule(self, rule: Rule):
        self._check_rule_type(rule)
        self[rule.name] = rule

    def get_partial_conclusions(self, weights=None, **kwargs):
        weights = weights or defaultdict(lambda: None)
        conclusions = [rule.get_conclusion(self.variables, weights[rule.name], **kwargs) for rule in self]
        return conclusions

    @property
    def conclusions(self):
        return self.get_partial_conclusions()

    def sum(self, weights, **kwargs):
        conclusions = self.get_partial_conclusions(weights, **kwargs)

        return sum(conclusions)

    def compute_weights(self, measurements):
        return {rule.name: rule.compute_weight(self.variables, measurements) for rule in self}

    def evaluate(self, measurements: dict, grid_size=1, **kwargs):
        # TODO: this assumes the conclusion of each rule is the same variable type
        weights = self.compute_weights(measurements)

        compound_conclusion = self.sum(weights, **kwargs)

        return compound_conclusion.defuzzify(grid_size=grid_size)

    @plotting.refine_multiplot
    def plot_eval(self, weights: dict, title=None, method='max-min', **kwargs):
        conclusions_cut = self.get_partial_conclusions(weights, method=method)

        rules = list(self)

        fig, axes = plt.subplots(1, len(self)+1, figsize=(15, 4), sharey='all', sharex='all')
        for i, conc in enumerate(self.conclusions):
            conc.plot_cut(ax=axes[i], cut_level=weights[rules[i].name], method=method,
                          title=f"{rules[i].name} {rules[i].conclusion}", **kwargs)

        for i, conc in enumerate(conclusions_cut):
            conc.plot(ax=axes[-1], label=rules[i].name, linewidth=1, linestyle='--')

        compound_conc = sum(conclusions_cut)
        compound_conc.plot(ax=axes[-1], shade=0, color='k', title="Aggregate conclusion", label="Aggregate")

        axes[-1].axvline(compound_conc.defuzzify(), color='k', linestyle='-.', lw=1, label="Crisp val.")

        axes[-1].legend()

        fig.subplots_adjust(left=0.05, right=0.95, top=0.85)
        fig.suptitle(title or f"Aggregation of rules with {method} method")
        plt.show()
