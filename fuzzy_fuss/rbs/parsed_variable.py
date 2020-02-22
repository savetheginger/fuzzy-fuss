import re

from fuzzy_fuss.fuzz.fuzzy4tuple import Fuzzy4Tuple
from fuzzy_fuss.fuzz.fuzzy_variable import FuzzyVariable
from fuzzy_fuss.rbs.parsed_object import ParsedObj, ParsedObjDict


class ParsedTuple(ParsedObj, Fuzzy4Tuple):
    PATTERN = r"\s*(?P<value>\w+)\s+(?P<numbers>[-\s\d.]+)\s*"

    @classmethod
    def process_match(cls, m, **kwargs) -> tuple:
        value = m.group('value')

        nums = re.split(r'\s+', m.group('numbers').strip(' '))

        if len(nums) != 4:
            raise ValueError(f"Matching a 4-tuple '{m.string}': expected 4 values, got {len(nums)}")

        try:
            num_nums = tuple(map(float, nums))
        except ValueError:
            raise ValueError(f"Invalid format for numerical values encountered in '{nums}'")

        return value, cls(*num_nums, value_name=value)


class ParsedVariable(ParsedObjDict, FuzzyVariable):
    def __init__(self, name, **kwargs):
        super(ParsedVariable, self).__init__(name=name, object_type=ParsedTuple, **kwargs)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
