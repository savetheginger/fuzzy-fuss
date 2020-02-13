import re

from fuzzy_fuss.rbs.rule import Rule, Measurement
from fuzzy_fuss.fuzz.fuzzy4tuple import Fuzzy4Tuple
from fuzzy_fuss.rbs.parsed_object import ParsedObjDict
from fuzzy_fuss.rbs.variable import ParsedVariable


class RuleBase(object):
    TUPLE_PATTERN = r"(?P<value>\w+)\s*(?P<numbers>[\s\d.]+)"

    def __init__(self):
        self.rules = ParsedObjDict(Rule)
        self.variables = {}
        self.measurements = ParsedObjDict(Measurement, float)
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

    def parse_tuple(self, line):
        tup = self.match_tuple(line)
        if tup:
            if not self._current_name:
                raise RuntimeError(f"Encountered a 4-tuple for unspecified variable: {line}")
            self.variables[self._current_name][tup[0]] = Fuzzy4Tuple(*tup[1])
            return True
        return False

    @staticmethod
    def match_tuple(line):
        m = re.match(RuleBase.TUPLE_PATTERN, line)
        if not m:
            return
        value = m.group('value')

        nums = re.split(r'\s+', m.group('numbers'))

        if len(nums) != 4:
            raise ValueError(f"Matching a 4-tuple '{line}': expected 4 values, got {len(nums)}")

        try:
            num_nums = tuple(map(float, nums))
        except ValueError:
            raise ValueError(f"Invalid format for numerical values encountered in '{nums}'")

        return value, num_nums


if __name__ == '__main__':
    rb = RuleBase()
    rb.parse(r"C:\Users\anima\Documents\Aberdeen\MSc_AI\CS551J_KRR\code\fuzzy-fuss\examples\tipping_rulebase.txt")
