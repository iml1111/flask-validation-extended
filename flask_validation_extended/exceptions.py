class InvalidAnnotation(Exception):

    def __init__(self, param):
        self.param = param

    def __str__(self):
        return (
            '"annotation" is invalid. '
            f'{self.param} must be one of '
            f'(int, float, str, bool types.All).'
        )

class InvalidAnnotationJson(InvalidAnnotation):

    def __str__(self):
        return (
            '"annotation" is invalid. '
            f'{self.param} must be one of '
            f'(int, float, str, bool, list, dict, '
            f'types.List, types.Dict, types.All).'
        )


class InvalidDefault(Exception):

    def __str__(self):
        return '"default" is not matched with "annotation"'

class InvalidRules(Exception):

    def __str__(self):
        # TODO: Rules 에러 기입하기
        return ''

class InvalidOptional(Exception):

    def __str__(self):
        return '"optional" must be one of (True, False).'

class InvalidRuleParameter(Exception):
    pass