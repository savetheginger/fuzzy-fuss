import os

from fuzzy_fuss.rbs.rule_base_parser import RuleBaseParser


ruleset, measurements = RuleBaseParser().parse(os.path.join(os.path.dirname(__file__), "tipping_rulebase.txt"))

# plot the parsed variables
for fv in ruleset.variables.values():
    fv.plot_range(margin=10)

ruleset.plot_rules(measurements=measurements, shade=0.1)

weights = ruleset.compute_weights(measurements)
ruleset.plot_eval(weights, composition='max-min')
ruleset.plot_eval(weights, composition='max-product')


