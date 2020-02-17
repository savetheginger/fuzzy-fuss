import os

from fuzzy_fuss.fuzz.fuzzy_rule_base import RuleBase
from fuzzy_fuss.rbs.rule_base_parser import RuleBaseParser

rbp = RuleBaseParser()
rbp.parse(os.path.join(os.path.dirname(__file__), "tipping_rulebase.txt"))

# plot the parsed variables
for fv in rbp.variables.values():
    fv.plot_range(margin=10)

for fr in rbp.rules.values():
    fr.plot(rbp.variables, measurements=rbp.measurements, shade=0.1)

ruleset = RuleBase(rbp.variables)
for rule in rbp.rules.values():
    ruleset.add_rule(rule)

weights = ruleset.compute_weights(rbp.measurements)
ruleset.plot_eval(weights, method='max-min')
ruleset.plot_eval(weights, method='max-product')


