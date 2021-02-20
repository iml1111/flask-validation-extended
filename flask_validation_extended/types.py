from typing import Any


class List:

    def __init__(self, item):
        self.item = item
        self.__origin__ = list
        self.__name__ = self.__str__()

    def __str__(self):
        if isinstance(self.item, tuple):
            return f"List({[i.__name__ for i in self.item]})"
        return f"List({self.item.__name__})"


class Dict:
    def __init__(self, key, value):
        self.key = key

        self.value = value
        self.__origin__ = dict
        self.__name__ = self.__str__()

    def __str__(self):
        return "Dict({%s:%s})" % (self.key.__name__, self.value.__name__)

All = "All"

TYPES = {int, str, float, bool, List, Dict, All}