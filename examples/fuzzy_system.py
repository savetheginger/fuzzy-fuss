from argparse import ArgumentParser

from fuzzy_fuss.rbs.rule_base_parser import RuleBaseParser

parser = ArgumentParser("Fuzzy rule-based reasoning system")
parser.add_argument('filename', type=str, help="Name of the file containing the rule base")
parser.add_argument('--composition', choices=['max-min', 'max-product'], default='max-min',
                    help="Type of composition to be used when evaluating a fuzzy rule")
parser.add_argument('--grid-size', type=float, default=0.1,
                    help="Size of grid used for defuzzification (the finer the grid, the more accurate the results)")
parser.add_argument('--plot', action='store_true', dest='plot', default=False,
                    help="Display plots of the parsed variables, rules, and the reasoning")

parsed_args = parser.parse_args()
kwargs = dict(composition=parsed_args.composition,
              grid_size=parsed_args.grid_size)


# parse the fuzzy rule base from the file
ruleset, measurements = RuleBaseParser().parse(parsed_args.filename)

if parsed_args.plot:
    # plot parsed fuzzy variables
    for fv in ruleset.variables.values():
        fv.plot_range(margin=10)

    # plot parsed rules
    ruleset.plot_rules(measurements=measurements, shade=0.1)

    weights = ruleset.compute_weights(measurements)
    ruleset.plot_eval(weights, **kwargs)

print(f"Result: {ruleset.evaluate(measurements, **kwargs):g}")
