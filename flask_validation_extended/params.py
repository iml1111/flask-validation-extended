from .types import All, List, Dict, type_check
from .exceptions import (
    InvalidOptional, InvalidDefault,
    InvalidAnnotation, InvalidRules,
    InvalidAnnotationJson
)


SINGLE_TYPES = {int, str, float, bool}
BUILTIN_TYPES = {int, str, float, bool, list, dict}
CUSTOM_TYPES = {List, Dict}


class Parameter:

    def __init__(
            self,
            annotation=All,
            default=None,
            rules=None,
            optional=False
    ):
        self.annotation = self._annotation_valid(annotation)
        self.default = self._default_valid(default, annotation)
        self.rules = self._rules_valid(rules)
        self.optional = self._optional_valid(optional)

    def _annotation_valid(self, annotation):
        if annotation in SINGLE_TYPES or annotation is All:
            return annotation
        raise InvalidAnnotation(self.__class__.__name__)

    @staticmethod
    def _default_valid(default, annotation):
        if default is None or type_check(default, annotation):
            return default
        raise InvalidDefault()

    @staticmethod
    def _rules_valid(rules):
        rules = rules if rules else []
        return rules

    @staticmethod
    def _optional_valid(optional):
        if isinstance(optional, bool):
            return optional
        raise InvalidOptional()


class Route(Parameter):
    pass


class Header(Parameter):
    def __init__(self, headername_or_annotation=All, *args, **kwargs):
        if isinstance(headername_or_annotation, str):
            self.header_name = headername_or_annotation
            super().__init__(*args, **kwargs)
        else:
            self.header_name = None
            super().__init__(headername_or_annotation, *args, **kwargs)


class Query(Parameter):
    pass


class Form(Parameter):
    pass


class Json(Parameter):

    def _annotation_valid(self, annotation):
        if annotation in BUILTIN_TYPES or \
                type(annotation) in CUSTOM_TYPES or \
                annotation is All:
            return annotation
        raise InvalidAnnotationJson(self.__class__.__name__)


class File:
    pass
