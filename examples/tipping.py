import os

from fuzzy_fuss.rbs.rule_base_parser import RuleBase

rb = RuleBase()
rb.parse(os.path.join(os.path.dirname(__file__), "tipping_rulebase.txt"))

# plot the parsed variables
for fv in rb.variables.values():
    maxx = max(s.b + s.beta for s in fv.values())
    minx = min(s.a - s.alpha for s in fv.values())
    fv.plot_range(minx-10, maxx+10, 1)
