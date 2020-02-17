import os

from fuzzy_fuss.fuzz.fuzzy_rule import RuleSet
from fuzzy_fuss.rbs.rule_base_parser import RuleBase

rb = RuleBase()
rb.parse(os.path.join(os.path.dirname(__file__), "tipping_rulebase.txt"))

# plot the parsed variables
# for fv in rb.variables.values():
#     fv.plot_range(margin=10)
#
# for fr in rb.rules.values():
#     fr.plot(rb.variables, measurements=rb.measurements, shade=0.1)

ruleset = RuleSet()
for rule in rb.rules.values():
    ruleset.add_rule(rule)

ruleset.plot_eval(rb.variables, rb.measurements, method='max-min')
ruleset.plot_eval(rb.variables, rb.measurements, method='max-product')


