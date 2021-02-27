
class InvalidHeaderName(Exception):

    def __str__(self):
        return '"header_name" must be a str.'


class InvalidAnnotation(Exception):

    def __init__(self, param):
        self.param = param

    def __str__(self):
        return (
            '"annotation" is invalid. '
            f'{self.param} must be one of '
            f'(int, float, str, bool types.All) or tuple.'
        )

class InvalidAnnotationJson(InvalidAnnotation):

    def __str__(self):
        return (
            '"annotation" is invalid. '
            f'{self.param} must be one of '
            f'(int, float, str, bool, list, dict, '
            f'types.List(), types.Dict(), types.All) or tuple.'
        )


class InvalidCustomTypeArgument(InvalidAnnotation):

    def __str__(self):
        return (
            '"annotation" is invalid. '
            f'{self.param} must be one of '
            f'(int, float, str, bool, list, dict, '
            f'types.List(), types.Dict(), types.All) or tuple.'
        )


class InvalidDefault(Exception):

    def __str__(self):
        return '"default" is not matched with "annotation"'

class InvalidRule(Exception):

    def __init__(self, rule):
        self.rule = rule

    def __str__(self):
        return f"{self.rule} is not Validation Rule."


class InvalidRuleAnnotation(Exception):

    def __init__(self, rule, rule_types):
        self.rule = rule
        self.rule_types = rule_types

    def __str__(self):
        return (
            f'Rule "{self.rule}" is Invalid. '
            f"This rule's Annotation must be in {self.rule_types}, "
        )


class InvalidOptional(Exception):

    def __str__(self):
        return '"optional" must be one of (True, False).'


class InvalidRuleParameter(Exception):

    def __init__(self, param, valid_type):
        self.param = param
        self.valid_type = valid_type

    def __str__(self):
        return f'"{self.param}" is not {self.valid_type}'


class EmptyTupleException(Exception):

    def __str__(self):
        return "args must be in filled."