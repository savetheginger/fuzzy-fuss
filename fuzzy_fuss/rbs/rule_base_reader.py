import re


class RuleBaseReader(object):
    RULE_PATTERN = r"(?P<name>Rule \d+):{0,1} (?P<body>.+)"

    def __init__(self):
        self._rules = dict()
        self._variables = dict()
        self._measurements = dict()


if __name__ == '__main__':
    rule = r"Rule 1 If the driving is good and the journey_time is short then the tip will be big"
    m = re.fullmatch(RuleBaseReader.RULE_PATTERN, rule)
    print(m.groups() if m else 'no match')
