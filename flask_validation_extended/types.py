"""
Types
# Supported Types
    - Builtin Types: int, str, float, bool, list, dict
    - Custom Types: List, Dict, All
"""
from .exceptions import InvalidAnnotationJson


class All:
    pass


class FileObj:
    pass


class List:

    def __init__(self, item=All):
        self.item = item
        self._org_type = list
        self.__name__ = self.__str__()

    def __str__(self):
        try:
            if isinstance(self.item, (tuple, list)):
                return f"List({[i.__name__ for i in self.item]})"
            return f"List({self.item.__name__})"
        except AttributeError:
            raise InvalidAnnotationJson("Types in List")

    @property
    def org_type(self):
        return self._org_type


class Dict:

    def __init__(self, item=All):
        self.item = item
        self._org_type = dict
        self.__name__ = self.__str__()

    def __str__(self):
        try:
            if isinstance(self.item, (tuple, list)):
                return f"Dict({[i.__name__ for i in self.item]})"
            return f"Dict({self.item.__name__})"
        except AttributeError:
            raise InvalidAnnotationJson("Types in Dict")

    @property
    def org_type(self):
        return self._org_type


def type_check(data, annotation):
    if isinstance(annotation, Dict):
        if not isinstance(data, dict):
            return False
        for value in data.values():
            if not type_check(value, annotation.item):
                return False
        return True

    elif isinstance(annotation, List):
        if not isinstance(data, list):
            return False
        for item in data:
            if not type_check(item, annotation.item):
                return False
        return True

    elif isinstance(annotation, (tuple, list)):
        for ann_i in annotation:
            if type_check(data, ann_i):
                return True
        return False

    else:
        return annotation is All or \
               isinstance(data, annotation)