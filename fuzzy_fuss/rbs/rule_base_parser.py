import re

from fuzzy_fuss.rbs.rule import Rule, Atom


class RuleBaseParser(object):
    RULE_PATTERN = r"(?P<name>Rule\s*\d+):{0,1} if (?P<propositions>.+) then (?P<conclusion>.+)"
    ATOM_PATTERN = r"(?P<variable>\w+) (?:is|will be) (?P<value>\w+)"
    MEAS_PATTERN = r"\s*(?P<variable>\w+)\s*=\s*(?P<value>\d+(\.\d*){0,1})\s*"

    def __init__(self):
        self._rules = dict()
        self._variables = dict()
        self._measurements = dict()

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
    rl = r"Rule 1 If the driving is good and the journey_time is short then the tip will be big"
    match = RuleBaseParser.match_rule(rl)
    print(match or 'rule: no match')

    meas = "journey_time = 9"
    print(RuleBaseParser.match_measurement(meas) or "measurement: no match")
