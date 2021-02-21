from abc import ABCMeta, abstractmethod


class ValidationRule(metaclass=ABCMeta):

    @abstractmethod
    def valid(self, data):
        pass


class MinLen(ValidationRule):

    def __init__(self, num):
        if isinstance(num, int):
            self.num = num
            self.types = {str, list, dict}
        else:
            # TODO: 모든 Rule 인자에 대한 예외처리 진행
            pass

    def valid(self, data):
        return len(data) >= self.num


class MaxLen(ValidationRule):

    def __init__(self, num):
        self.num = num
        self.types = {str, list, dict}

    def valid(self, data):
        return len(data) <= self.num


class Min(ValidationRule):

    def __init__(self, num):
        self.num = num
        self.types = {int, float}

    def valid(self, data):
        return data >= self.num


class Max(ValidationRule):

    def __init__(self, num):
        self.num = num
        self.types = {int, float}

    def valid(self, data):
        return data <= self.num


class StrFilter(ValidationRule):

    def __init__(self, string):
        self.string = string
        # TODO: 룰 작성 진행하기