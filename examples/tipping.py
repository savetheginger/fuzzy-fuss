import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

from fuzzy_fuss.rbs.rule_base_parser import RuleBaseParser

# parse the fuzzy rule base from the file
ruleset, measurements = RuleBaseParser().parse(os.path.join(os.path.dirname(__file__), "tipping_rulebase2.txt"))

r = 0.5
g = 0.05

meas_grid = {}
for variable, value in measurements.items():
    vr = r * value
    vg = g * value
    meas_grid[variable] = np.arange(value - vr, value + vr + vg, vg)


var1, var2 = tuple(meas_grid.keys())[:2]
vals1 = meas_grid[var1]
vals2 = meas_grid[var2]

results = np.zeros((vals1.size, vals2.size))

print(f"Performing exhaustive check for {results.size} values...")
for i1, val1 in enumerate(vals1):
    for i2, val2 in enumerate(vals2):
        results[i1, i2] = ruleset.evaluate(measurements={var1: val1, var2: val2})
print("Done")

x, y = np.meshgrid(vals1, vals2)

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(x, y, results, rstride=1, cstride=1, cmap='viridis')
ax.set_xlabel(var1)
ax.set_ylabel(var2)
ax.set_zlabel(ruleset.conclusion_names[0])
ax.set_title(f"Exhaustive rule base '{ruleset.name}' response analysis")
plt.show()
