from .types import (
    All, List, Dict, FileObj, type_check,
    SINGLE_TYPES, BUILTIN_TYPES
)

from .rules import ValidationRule
from .exceptions import (
    InvalidOptional, InvalidDefault,
    InvalidAnnotation, InvalidRule,
    InvalidAnnotationJson , InvalidRuleAnnotation,
    InvalidHeaderName
)

CUSTOM_TYPES = {List, Dict, FileObj}


class Parameter:

    def __init__(
            self,
            annotation=All,
            default=None,
            rules=None,
            optional=False
    ):
        if not isinstance(annotation, (list, tuple)):
            annotation = [annotation]
        self.annotation = self._annotation_valid(annotation)

        self.default = self._default_valid(default)

        rules = [] if rules is None else rules
        if not isinstance(rules, (tuple, list)):
            rules = [rules]
        self.rules = self._rules_valid(rules)

        self.optional = self._optional_valid(optional)

    def _annotation_valid(self, annotations):
        for annotation in annotations:
            if annotation not in SINGLE_TYPES and annotation is not All:
                raise InvalidAnnotation(self.__class__.__name__)
        return annotations

    def _default_valid(self, default):
        if default is None:
            return default
        for annotation in self.annotation:
            if type_check(default, annotation):
                return default
        raise InvalidDefault()

    def _rules_valid(self, rules):

        if isinstance(self.annotation, tuple):
            origin_anns = list(self.annotation)
        else:
            origin_anns = self.annotation[:]

        for idx, origin_ann in enumerate(origin_anns):
            if hasattr(origin_ann, 'org_type'):
                origin_anns[idx] = origin_ann.org_type

        for origin_ann in origin_anns:
            for rule in rules:
                if rule.__class__.__bases__[0] is not ValidationRule:
                    raise InvalidRule(rule.__class__.__bases__[0])
                if isinstance(rule.types, (list, tuple)):
                    if All not in rule.types and origin_ann not in rule.types:
                        raise InvalidRuleAnnotation(
                            rule.__class__.__name__, rule.types
                        )
                else:
                    if rule.types is not All and  origin_ann is not rule.types:
                        raise InvalidRuleAnnotation(
                            rule.__class__.__name__, rule.types
                        )

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
    def __init__(self, header_name, *args, **kwargs):
        if not isinstance(header_name, str):
            raise InvalidHeaderName()
        self.header_name = header_name
        super().__init__(*args, **kwargs)


class Json(Parameter):

    def _annotation_valid(self, annotations):
        for annotation in annotations:
            if (
                annotation not in BUILTIN_TYPES and
                type(annotation) not in CUSTOM_TYPES and
                annotation is not All
            ):
                raise InvalidAnnotationJson(self.__class__.__name__)
        return annotations

class File(Parameter):

    def __init__(self, rules=None, optional=False):
        super().__init__(rules=rules, optional=optional)
        self.annotation = [FileObj]

    def _annotation_valid(self, annotation):
        return annotation

    def _rules_valid(self, rules):

        for rule in rules:
            if rule.__class__.__bases__[0] is not ValidationRule:
                raise InvalidRule(rule.__class__.__bases__[0])
            if isinstance(rule.types, (list, tuple)):
                if All not in rule.types and FileObj not in rule.types:
                    raise InvalidRuleAnnotation(
                        rule.__class__.__name__, rule.types
                    )
            else:
                if rule.types is not All and rule.types is not FileObj:
                    raise InvalidRuleAnnotation(
                        rule.__class__.__name__, rule.types
                    )

        return rules
