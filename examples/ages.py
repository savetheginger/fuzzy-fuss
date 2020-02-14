from fuzzy_fuss.fuzz.fuzzy_variable import FuzzyVariable
from fuzzy_fuss.fuzz.fuzzy4tuple import Fuzzy4Tuple


fsets = FuzzyVariable('Ages')
fsets['young'] = Fuzzy4Tuple.from_points(0, 0, 20, 40)
fsets['middle-aged'] = Fuzzy4Tuple.from_points(35, 50, 60, 65)
fsets['old'] = Fuzzy4Tuple.from_points(60, 70, 100, 100)
fsets['not young'] = - fsets['young']
fsets['young OR middle-aged'] = fsets['young'] + fsets['middle-aged']
fsets['old AND middle-aged'] = fsets['old'] * fsets['middle-aged']

fsets.plot_range(0, 100, 1, shade=0,
                 kwargs_by_name={'young OR middle-aged': {'shade': 0.3},
                                 'old AND middle-aged': {'shade': 0.5}})

print(fsets.get_values([20, 37, 55, 63, 85]))

cf = FuzzyVariable("Compositions")
m = fsets['middle-aged']
cf['original'] = m
cf['max-min'] = m.cut(0.5)
cf['max-product'] = m.cut(0.5, 'max-product')
cf.plot_range(0, 100, 1)
