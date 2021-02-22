from .types import All, List, Dict, type_check
from .rules import ValidationRule
from .exceptions import (
    InvalidOptional, InvalidDefault,
    InvalidAnnotation, InvalidRule,
    InvalidAnnotationJson , InvalidRuleAnnotation
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
        elif isinstance(annotation, (tuple, list)):
            for ann_i in annotation:
                self._annotation_valid(ann_i)
            return annotation
        raise InvalidAnnotation(self.__class__.__name__)

    @staticmethod
    def _default_valid(default, annotation):
        if default is None or type_check(default, annotation):
            return default
        raise InvalidDefault()

    def _rules_valid(self, rules):

        rules = [] if rules is None else rules
        if not isinstance(rules, (tuple, list)):
            rules = [rules]

        origin_ann = self.annotation
        if hasattr(self.annotation, 'org_type'):
            origin_ann = self.annotation.org_type

        for rule in rules:
            if rule.__class__.__bases__[0] is not ValidationRule:
                raise InvalidRule(rule.__class__.__bases__[0])
            if rule.types is not All and origin_ann not in rule.types:
               raise InvalidRuleAnnotation(rule.__class__.__name__, rule.types, origin_ann)
        return rules

    @staticmethod
    def _optional_valid(optional):
        if isinstance(optional, bool):
            return optional
        raise InvalidOptional()


class Route(Parameter):
    pass


class Query(Parameter):
    pass


class Form(Parameter):
    pass


class Header(Parameter):
    def __init__(self, headername_or_annotation=All, *args, **kwargs):
        if isinstance(headername_or_annotation, str):
            self.header_name = headername_or_annotation
            super().__init__(*args, **kwargs)
        else:
            self.header_name = None
            super().__init__(headername_or_annotation, *args, **kwargs)


class Json(Parameter):

    def _annotation_valid(self, annotation):
        if (
            annotation in BUILTIN_TYPES or
            type(annotation) in CUSTOM_TYPES or
            annotation is All
        ):
            return annotation
        elif isinstance(annotation, (tuple, list)):
            for ann_i in annotation:
                self._annotation_valid(ann_i)
            return annotation
        raise InvalidAnnotationJson(self.__class__.__name__)


class File:
    pass
