import re

from fuzzy_fuss.fuzz.fuzzy_rule import Rule, Atom

from fuzzy_fuss.rbs.parsed_object import ParsedObj


class ParsedAtom(Atom, ParsedObj):
    PATTERN = r"\s*(?P<variable>\w+) (?:is|will be) (?P<value>\w+)\s*"

    @classmethod
    def process_match(cls, m, **kwargs):
        vals = tuple(m.groupdict().values())
        return cls(vals)

    @staticmethod
    def match_all(line, split_pattern=None):
        split_pattern = split_pattern or " and | or "
        props = re.split(split_pattern, line, re.IGNORECASE)
        return tuple(ParsedAtom.match(prop, silent=False) for prop in props)


class ParsedMeasurement(ParsedAtom):
    PATTERN = r"\s*(?P<variable>\w+)\s*=\s*(?P<value>\d+(\.\d*){0,1})\s*"

    def __new__(cls, vals):
        try:
            vals_new = (vals[0], float(vals[1]))
        except ValueError:
            raise ValueError(f"Cannot convert {vals[1]} to float")

        return super(ParsedMeasurement, cls).__new__(ParsedMeasurement, vals_new)


class ParsedRule(Rule, ParsedObj):
    PATTERN = r"(?P<name>Rule\s*\d+):{0,1} if (?P<propositions>.+) then (?P<conclusion>.+)"

    @classmethod
    def process_match(cls, m, **kwargs):
        md = m.groupdict()

        prop = ParsedAtom.match_all(md['propositions'])
        connectives = [s.strip(' ') for s in re.findall(r" and | or ", md['propositions'])]
        conclusion = ParsedAtom.match(md['conclusion'], silent=False)

        rule = cls(name=md['name'], prop_atoms=prop, prop_connectives=connectives, conclusion=conclusion)
        return rule.name, rule
