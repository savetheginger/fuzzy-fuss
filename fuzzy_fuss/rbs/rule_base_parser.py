from fuzzy_fuss.fuzz.fuzzy_rule_base import RuleBase

from fuzzy_fuss.rbs.parsed_rule import ParsedRule, ParsedMeasurement
from fuzzy_fuss.rbs.parsed_object import ParsedObjDict
from fuzzy_fuss.rbs.variable import ParsedVariable


class RuleBaseParser(object):
    def __init__(self):
        self.rules = ParsedObjDict(ParsedRule)
        self.variables = {}
        self.measurements = ParsedObjDict(ParsedMeasurement, float)
        self.name = None
        self._current_name = None

    def parse(self, filename):
        self.name = None
        self.variables[None] = ParsedVariable(None)

        with open(filename) as f:
            for line in f:
                line = line.strip('\n')
                if not line:
                    continue

                if self.rules.parse(line) or self.measurements.parse(line) \
                        or self.variables[self._current_name].parse(line):
                    continue

                if not self.name:
                    self.name = line
                else:
                    self.variables[line] = ParsedVariable(line)
                    self._current_name = line

        if len(self.variables[None]):
            raise RuntimeError(f"Encountered 4-tuples for unspecified variables: {dict(self.variables[None].items())}")
        self.variables.pop(None)

        self._current_name = None

        return self.make_rule_base(), self.measurements

    def make_rule_base(self):
        rulebase = RuleBase(self.name, self.variables)
        for rule in self.rules.values():
            rulebase.add_rule(rule)

        return rulebase


