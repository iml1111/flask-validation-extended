import re
from datetime import datetime
from abc import ABCMeta, abstractmethod
from .exceptions import InvalidRuleParameter
from .types import All, FileObj


class ValidationRule(metaclass=ABCMeta):

    @staticmethod
    def _param_validate(param, param_type):
        if not isinstance(param, param_type):
            raise InvalidRuleParameter(param, param_type)
        return param

    @property
    def types(self):
        return All

    def invalid_str(self):
        return f"doesn't not match the {self.__class__.__name__} rule"

    @abstractmethod
    def is_valid(self, data) -> bool:
        pass


class MinLen(ValidationRule):

    def __init__(self, num):
        self._num = self._param_validate(num, int)

    @property
    def types(self):
        return (str, list, dict)

    def invalid_str(self):
        return f"must be at least {self._num} elements."

    def is_valid(self, data):
        return self._num <= len(data)


class MaxLen(ValidationRule):

    def __init__(self, num):
        self._num = self._param_validate(num, int)

    @property
    def types(self):
        return (str, list, dict)

    def invalid_str(self):
        return f"must be a maximum of {self._num} elements."

    def is_valid(self, data) -> bool:
        return len(data) <= self._num


class Min(ValidationRule):

    def __init__(self, num):
        self._num = self._param_validate(num, (int, float))

    @property
    def types(self):
        return (int, float)

    def invalid_str(self):
        return f"must be larger than {self._num}."

    def is_valid(self, data) -> bool:
        return self._num <= data


class Max(ValidationRule):

    def __init__(self, num):
        self._num = self._param_validate(num, (int, float))

    @property
    def types(self):
        return (int, float)

    def invalid_str(self):
        return f"must be smaller than {self._num}."

    def is_valid(self, data) -> bool:
        return data <= self._num


class In(ValidationRule):

    def __init__(self, enum):
        self._enum = self._param_validate(enum, (list, tuple))

    @property
    def types(self):
        return All

    def invalid_str(self):
        return f"must be one of these lists: {self._enum}."

    def is_valid(self, data) -> bool:
        return data in self._enum


class Number(ValidationRule):

    @property
    def types(self):
        return str

    def invalid_str(self):
        return f"must be a digitable(can convert int) string."

    def is_valid(self, data) -> bool:
        return data.isdecimal()


class Strip(ValidationRule):

    @property
    def types(self):
        return str

    def invalid_str(self):
        return f"must be a striped string."

    def is_valid(self, data) -> bool:
        return data == data.strip()


class IsoDatetime(ValidationRule):

    @property
    def types(self):
        return str

    def invalid_str(self):
        return f"must be a ISO Datetime Format."

    def is_valid(self, data) -> bool:
        try:
            datetime.fromisoformat(data)
        except ValueError:
            return False
        return True


class Datetime(ValidationRule):

    def __init__(self, dt_format):
        self._df_format = self._param_validate(dt_format, str)

    @property
    def types(self):
        return str

    def invalid_str(self):
        return f"must be a Datetime Format: {self._df_format}"

    def is_valid(self, data) -> bool:
        try:
            datetime.strptime(data, self._df_format)
            return True
        except ValueError:
            return False

REGEX_EMAIL = (
    r"^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@"
    r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
)

class Email(ValidationRule):

    @property
    def types(self):
        return str

    def invalid_str(self):
        return f"must be a Email Format."

    def is_valid(self, data) -> bool:
        return bool(re.fullmatch(pattern=REGEX_EMAIL, string=data))

REGEX_PHONE_NUM = r"^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3,4}[\s.-]\d{4}$"

class PhoneNum(ValidationRule):

    @property
    def types(self):
        return str

    def invalid_str(self):
        return f"must be a PhoneNumber Format."

    def is_valid(self, data) -> bool:
        return bool(re.fullmatch(pattern=REGEX_PHONE_NUM, string=data))


class Regex(ValidationRule):

    def __init__(self, pattern):
        self._p_str = self._param_validate(pattern, str)
        self._pattern = re.compile(self._param_validate(self._p_str, str))

    @property
    def types(self):
        return str

    def invalid_str(self):
        return f"pattern does not match: {self._p_str}"

    def is_valid(self, data) -> bool:
        return bool(self._pattern.search(data))


class Ext(ValidationRule):

    def __init__(self, extensions):
        if not isinstance(extensions, (list, tuple)):
            extensions = [extensions]
        for ext in extensions:
            self._param_validate(ext, str)
        self.extensions = extensions

    @property
    def types(self):
        return FileObj

    def invalid_str(self):
        return f'is not matched extension: {self.extensions}'

    def is_valid(self, file_list) -> bool:
        for file in file_list:
            check = False
            for ext in self.extensions:
                if file.filename.endswith(ext):
                    check = True
                    break
            if not check:
                return False
        return True


class MaxFileCount(ValidationRule):

    def __init__(self, max_num):
        self.max_num = self._param_validate(max_num, int)

    @property
    def types(self):
        return FileObj

    def invalid_str(self):
        return f'File Count must smaller than {self.max_num}.'

    def is_valid(self, file_list) -> bool:
        return len(file_list) <= self.max_num


class MinFileCount(ValidationRule):

    def __init__(self, min_num):
        self.min_num = self._param_validate(min_num, int)

    @property
    def types(self):
        return FileObj

    def invalid_str(self):
        return f'File Count must smaller than {self.min_num}.'

    def is_valid(self, file_list) -> bool:
        return len(file_list) >= self.min_num