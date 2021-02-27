"""
Types
# Supported Types
    - Builtin Types: int, str, float, bool, list, dict
    - Custom Types: List, Dict, All
"""
from .exceptions import InvalidCustomTypeArgument

SINGLE_TYPES = {int, str, float, bool}
BUILTIN_TYPES = {int, str, float, bool, list, dict}


class CustomType:

    @staticmethod
    def _type_valid(item):
        try:
            return (
                item in BUILTIN_TYPES or
                item is All or
                type(item) in {List, Dict}
            )
        except TypeError:
            return False

    def _item_valid(self, item):
        if isinstance(item, (list, tuple)):
            for item_i in item:
                if not self._type_valid(item_i):
                    return False
            return True
        return self._type_valid(item)


class All(CustomType):
    pass


class FileObj(CustomType):
    pass


class List(CustomType):

    def __init__(self, item=All):
        if self._item_valid(item):
            self.item = item
        else:
            raise InvalidCustomTypeArgument("Types in CustomType")
        self._org_type = list
        self.__name__ = self.__str__()

    def __str__(self):
        try:
            if isinstance(self.item, (tuple, list)):
                return f"List({[i.__name__ for i in self.item]})"
            return f"List({self.item.__name__})"
        except AttributeError:
            raise InvalidCustomTypeArgument("Types in CustomType")

    @property
    def org_type(self):
        return self._org_type


class Dict(List):

    def __str__(self):
        try:
            if isinstance(self.item, (tuple, list)):
                return f"Dict({[i.__name__ for i in self.item]})"
            return f"Dict({self.item.__name__})"
        except AttributeError:
            raise InvalidCustomTypeArgument("Types in CustomType")


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