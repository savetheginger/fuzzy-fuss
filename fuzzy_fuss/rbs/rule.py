import re
from typing import Tuple

from fuzzy_fuss.rbs.parsed_object import ParsedObj


class Atom(tuple, ParsedObj):
    PATTERN = r"\s*(?P<variable>\w+) (?:is|will be) (?P<value>\w+)\s*"

    def __init__(self, vals):
        if len(vals) != 2:
            raise ValueError(f"Expected a length 2 argument, got length {len(vals)}: {vals}")

    def __repr__(self):
        return f"({self[0]} = {self[1]})"

    @classmethod
    def process_match(cls, m, **kwargs):
        vals = tuple(m.groupdict().values())
        return cls(vals)

    @staticmethod
    def match_all(line, split_pattern=None):
        split_pattern = split_pattern or " and | or "
        props = re.split(split_pattern, line, re.IGNORECASE)
        return tuple(Atom.match(prop, silent=False) for prop in props)


class Measurement(Atom):
    PATTERN = r"\s*(?P<variable>\w+)\s*=\s*(?P<value>\d+(\.\d*){0,1})\s*"

    def __new__(self, vals):
        try:
            vals_new = (vals[0], float(vals[1]))
        except ValueError:
            raise ValueError(f"Cannot convert {vals[1]} to float")

        return super(Measurement, self).__new__(Measurement, vals_new)


class Rule(ParsedObj):
    PATTERN = r"(?P<name>Rule\s*\d+):{0,1} if (?P<propositions>.+) then (?P<conclusion>.+)"

    def __init__(self, name: str, prop_atoms: Tuple[Atom], prop_connectives, conclusion: Atom):
        la = len(prop_atoms)
        lc = len(prop_connectives)
        if not lc == la - 1:
            raise ValueError(f"Improper number of connectives for {la} atoms: expected {la - 1}, got {lc}")

        self.name = name
        self.prop_atoms = prop_atoms
        self.prop_connectives = prop_connectives
        self.conclusion = conclusion

    def __repr__(self):
        pc = self.prop_connectives
        pa = self.prop_atoms

        prop = str(pa[0])

        for i in range(len(self.prop_connectives)):
            prop += f" {pc[i].upper()}"
            prop += f" {str(pa[i+1])}"

        return f"{self.name}: {prop} => {str(self.conclusion)}"

    @classmethod
    def process_match(cls, m, **kwargs):
        md = m.groupdict()

        prop = Atom.match_all(md['propositions'])
        connectives = [s.strip(' ') for s in re.findall(r" and | or ", md['propositions'])]
        conclusion = Atom.match(md['conclusion'], silent=False)

        rule = cls(name=md['name'], prop_atoms=prop, prop_connectives=connectives, conclusion=conclusion)
        return rule.name, rule
