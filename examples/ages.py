from fuzzy_fuss.fuzz import FuzzDict
from fuzzy_fuss.fuzzy_set_tuple import FuzzySetTuple


fsets = FuzzDict()
fsets['young'] = FuzzySetTuple.from_points(0, 0, 20, 40)
fsets['middle-aged'] = FuzzySetTuple.from_points(35, 50, 60, 65)
fsets['old'] = FuzzySetTuple.from_points(60, 70, 100, 100)
fsets['not young'] = - fsets['young']

fsets.plot_range(0, 100, 1, title="Ages", shade=0)

print(fsets.get_values([20, 37, 55, 63, 85]))
