import re


class ParsedObj(object):
    PATTERN = None

    @classmethod
    def match(cls, line, silent=True, **kwargs):
        if not cls.PATTERN:
            raise NotImplementedError(f"Pattern for class {cls.__name__} not specified")

        m = re.fullmatch(cls.PATTERN, line.replace('the ', ''), re.IGNORECASE)
        if not m:
            if silent:
                return
            raise RuntimeError(f"Failed to match '{line}' for class {cls.__name__} (pattern: {cls.PATTERN})")

        return cls.process_match(m, **kwargs)

    @classmethod
    def process_match(cls, m, **kwargs) -> tuple:
        raise NotImplementedError("Match processing method not implemented")


class ParsedObjDict(dict):
    def __init__(self, object_type: type(ParsedObj), item_type=None):
        super().__init__()
        self._object_type = object_type
        self._item_type = item_type or object_type

    def __setitem__(self, key, value):
        if not isinstance(value, self._item_type):
            raise TypeError(f"__setitem__: value not an instance of {self._item_type} "
                            f"(got {value} of type {type(value)})")

        super().__setitem__(key, value)

    def parse(self, line, **kwargs):
        match = self._object_type.match(line)

        if match:
            self[match[0]] = match[1]
            return True  # success
        return False     # fail
