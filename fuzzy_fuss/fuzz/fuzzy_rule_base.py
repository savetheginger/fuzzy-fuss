import matplotlib.pyplot as plt
from collections import defaultdict

from fuzzy_fuss.misc import plotting
from fuzzy_fuss.fuzz.fuzzy_rule import Rule


class RuleBase(dict):
    def __init__(self, name, variables):
        self.name = name
        self.variables = variables
        super(RuleBase, self).__init__()

    def __setitem__(self, key, value):
        self._check_rule_type(value)
        super(RuleBase, self).__setitem__(key, value)

    def __iter__(self):
        for key in sorted(self.keys()):  # sort by rule name
            yield self[key]

    def __repr__(self):
        v = self.variables
        return f"Rule base '{self.name}' with {len(v)} variables ({', '.join(v.keys())}) and {len(self)} rules"

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

    @property
    def conclusion_names(self):
        return list(set([rule.conclusion[0] for rule in self]))

    def sum(self, weights, **kwargs):
        conclusions = self.get_partial_conclusions(weights, **kwargs)

        return sum(conclusions)

    def compute_weights(self, measurements):
        return {rule.name: rule.compute_weight(self.variables, measurements) for rule in self}

    def evaluate(self, measurements: dict, grid_size=1, defuzz_method='coa', **kwargs):
        conc_names = self.conclusion_names
        if len(conc_names) > 1:
            raise RuntimeError(f"More than on target variable (rule conclusion) in the rule base: {conc_names}")

        weights = self.compute_weights(measurements)

        compound_conclusion = self.sum(weights, **kwargs)

        return compound_conclusion.defuzzify(grid_size=grid_size, method=defuzz_method)

    def plot_rules(self, **kwargs):
        for fr in self:
            fr.plot(self.variables, **kwargs)

    @plotting.refine_multiplot
    def plot_eval(self, weights: dict, title=None, composition='max-min', crisp_conclusion=None, **kwargs):
        conclusions_cut = self.get_partial_conclusions(weights, composition=composition)

        rules = list(self)

        fig, axes = plt.subplots(1, len(self)+1, figsize=(15, 4), sharey='all', sharex='all')
        for i, conc in enumerate(self.conclusions):
            conc.plot_cut(ax=axes[i], cut_level=weights[rules[i].name], composition=composition,
                          title=f"{rules[i].name} {rules[i].conclusion}", **kwargs)

        for i, conc in enumerate(conclusions_cut):
            conc.plot(ax=axes[-1], label=rules[i].name, linewidth=1, linestyle='--')

        compound_conc = sum(conclusions_cut)
        compound_conc.plot(ax=axes[-1], shade=0, color='k', label="Aggregate",
                           title=f"{compound_conc.variable_name}: composition")

        if crisp_conclusion is not None:
            axes[-1].axvline(crisp_conclusion, color='k', linestyle='-.', lw=1, label="Crisp val.")

        axes[-1].legend()
        axes[0].set_ylabel(f"membership values")
        fig.subplots_adjust(left=0.05, right=0.95, top=0.85)
        fig.suptitle(title or f"Aggregation of rules with {composition} method")
        plt.show()
