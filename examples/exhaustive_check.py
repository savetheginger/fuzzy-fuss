import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

from fuzzy_fuss.rbs.rule_base_parser import RuleBaseParser

from fuzzy_system import parser

parser.add_argument('--var-indices', nargs=2, default=(0, 1), type=int,
                    help="Indices of variables for the exhaustive check (in case there is more than 2)")
parser.add_argument('--var-grid-range', default=0.5, type=float,
                    help="Portion of variable value defining the grid range")
parser.add_argument('--var-grid-size', default=25, type=int,
                    help="Size of the grid (number of elements in the range)")
parsed_args = parser.parse_args()

# parse the fuzzy rule base from the file
ruleset, measurements = RuleBaseParser().parse(parsed_args.filename)

meas_grid = {}
for variable, value in measurements.items():
    vr = parsed_args.var_grid_range * value
    meas_grid[variable] = np.linspace(value - vr, value + vr, parsed_args.var_grid_size)


var_names = tuple(meas_grid.keys())
i = parsed_args.var_indices
var1 = var_names[i[0]]
var2 = var_names[i[1]]

results = np.zeros(2*(parsed_args.var_grid_size, ))

print(f"Performing exhaustive check for {results.size} values...")
for i1, val1 in enumerate(meas_grid[var1]):
    for i2, val2 in enumerate(meas_grid[var2]):
        results[i1, i2] = ruleset.evaluate(measurements={**measurements, var1: val1, var2: val2})
print("Done")

x, y = np.meshgrid(meas_grid[var1], meas_grid[var2])

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.plot_surface(x, y, results, rstride=1, cstride=1, cmap='viridis', vmax=np.nanmax(results), vmin=np.nanmin(results))
ax.set_xlabel(var1)
ax.set_ylabel(var2)
ax.set_zlabel(ruleset.conclusion_names[0])
ax.set_title(f"Exhaustive rule base '{ruleset.name}' response analysis")
plt.show()
