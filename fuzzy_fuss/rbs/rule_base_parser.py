import re
from collections import defaultdict

from fuzzy_fuss.rbs.rule import Rule, Atom


class RuleBaseParser(object):
    RULE_PATTERN = r"(?P<name>Rule\s*\d+):{0,1} if (?P<propositions>.+) then (?P<conclusion>.+)"
    ATOM_PATTERN = r"(?P<variable>\w+) (?:is|will be) (?P<value>\w+)"
    MEAS_PATTERN = r"\s*(?P<variable>\w+)\s*=\s*(?P<value>\d+(\.\d*){0,1})\s*"
    TUPLE_PATTERN = r"(?P<value>\w+)\s*(?P<numbers>[\s\d.]+)"

    def __init__(self):
        self._rules = dict()
        self._variables = defaultdict(lambda: dict())
        self._measurements = dict()
        self._rbs_name = None
        self._current_name = None

    def parse(self, filename):
        with open(filename) as f:
            for line in f:
                line = line.strip('\n')
                if not line:
                    continue

                if self.parse_rule(line) or self.parse_measurement(line) or self.parse_tuple(line):
                    continue

                if not self._rbs_name:
                    self._rbs_name = line
                else:
                    self._current_name = line

        self._current_name = None

    def parse_rule(self, line):
        rule = self.match_rule(line)
        if rule:
            self._rules[rule.name] = rule
            return True
        return False

    def parse_measurement(self, line):
        meas = self.match_measurement(line)
        if meas:
            self._measurements[meas[0]] = meas[1]
            return True
        return False

    def parse_tuple(self, line):
        tup = self.match_tuple(line)
        if tup:
            if not self._current_name:
                raise RuntimeError(f"Encountered a 4-tuple for unspecified variable: {line}")
            self._variables[self._current_name][tup[0]] = tup[1]
            return True
        return False

    @staticmethod
    def match_tuple(line):
        m = re.match(RuleBaseParser.TUPLE_PATTERN, line)
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

    @staticmethod
    def match_measurement(line):
        m = re.match(RuleBaseParser.MEAS_PATTERN, line)
        if not m:
            return
        md = m.groupdict()
        return Atom((md['variable'], float(md['value'])))

    @staticmethod
    def match_rule(line_raw):
        line = line_raw.replace('the ', '')

        m = re.fullmatch(RuleBaseParser.RULE_PATTERN, line, re.IGNORECASE)
        if not m:
            return

        md = m.groupdict()

        try:
            prop = re.findall(RuleBaseParser.ATOM_PATTERN, md['propositions'], re.IGNORECASE)
            connectives = [s.strip(' ') for s in re.findall(r" and | or ", md['propositions'])]
            conclusion = re.fullmatch(RuleBaseParser.ATOM_PATTERN, md['conclusion']).groups()
        except AttributeError:
            raise ValueError(f"Rule '{line_raw}' does not match the rule pattern")

        rule = Rule(name=md['name'], prop_atoms=prop, prop_connectives=connectives, conclusion=conclusion)
        return rule


if __name__ == '__main__':
    rbsp = RuleBaseParser()
    rbsp.parse(r"C:\Users\anima\Documents\Aberdeen\MSc_AI\CS551J_KRR\code\fuzzy-fuss\examples\tipping_rulebase.txt")
