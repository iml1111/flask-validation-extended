"""
Types
# Supported Types
    - Builtin Types: int, str, float, bool, list, dict
    - Custom Types: List, Dict, All
"""
class All:
    pass


class List:

    def __init__(self, item=All):
        self.item = item
        self.__origin__ = list
        self.__name__ = self.__str__()

    def __str__(self):
        if isinstance(self.item, tuple):
            return f"List({[i.__name__ for i in self.item]})"
        return f"List({self.item.__name__})"


class Dict:

    def __init__(self, key=All, value=All):
        self.key = key
        self.value = value
        self.__origin__ = dict
        self.__name__ = self.__str__()

    def __str__(self):
        return "Dict({%s:%s})" % (self.key.__name__, self.value.__name__)


def type_check(data, annotation):
    if isinstance(annotation, Dict):
        if not isinstance(data, dict):
            return False
        for key, value in data.items():
            if not isinstance(key, annotation.key):
                return False
            if not type_check(value, annotation.value):
                return False
        return True

    elif isinstance(annotation, List):
        if not isinstance(data, list):
            return False
        for item in data:
            if not type_check(item, annotation.item):
                return False
        return True

    elif isinstance(annotation, tuple):
        for ann_i in annotation:
            if type_check(data, ann_i):
                return True
        return False

    else:
        return annotation is All or \
               isinstance(data, annotation)