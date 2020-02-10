import re

from fuzzy_fuss.rbs.rule import Rule


class RuleBaseReader(object):
    RULE_PATTERN = r"(?P<name>Rule\s*\d+):{0,1} (?P<body>.+)"

    def __init__(self):
        self._rules = dict()
        self._variables = dict()
        self._measurements = dict()

    @staticmethod
    def match_rule(line):
        m = re.fullmatch(RuleBaseReader.RULE_PATTERN, line, re.IGNORECASE)
        if not m:
            return

        md = m.groupdict()
        body = md['body']
        prop = re.findall(r"[the ]*(?P<variable>\w+) is (?P<value>\w+)", body, re.IGNORECASE)
        connectives = [s.strip(' ') for s in re.findall(r" and | or ", body)]

        return Rule(name=md['name'], prop_atoms=prop, prop_connectives=connectives, conclusion=(' ', ' '))


if __name__ == '__main__':
    rule = r"Rule 1 If the driving is good and the journey_time is short then the tip will be big"
    match = RuleBaseReader.match_rule(rule)
    print(match or 'no match')
