import unittest
from flask_validation_extended.exceptions import (
    InvalidAnnotation,
    InvalidDefault,
    InvalidOptional,
    InvalidHeaderName
)
from flask_validation_extended.types import All, List, Dict, FileObj
from flask_validation_extended.params import Header


class ParamHeaderTestCase(unittest.TestCase):

    def test_header_exists(self):
        self.assertTrue(Header('test') is not None)

    def test_invalid_header_name(self):
        for header_name in [1, 1.123, True, [1,2], {1:2}, {1,2}]:
            except_check = False
            try:
                Header(header_name)
            except InvalidHeaderName:
                except_check = True
            self.assertTrue(except_check)

    def test_annotation_valid(self):
        """Param Header annotation validation test"""

        # allowed types
        for type_i in [int, str, float, bool, All]:
            Header('test', type_i)

        # other types must exception!
        for type_i in [list, dict, List, Dict, List(), Dict(), FileObj, set]:
            exception_check = False
            try:
                Header('test', type_i)
            except InvalidAnnotation:
                exception_check = True
            self.assertTrue(exception_check)

    def test_default_valid(self):
        """Param Header default validation test"""
        types = [int, str, float, bool]
        defaults = [1, "1", 1.13, True]
        ex_defaults = [[1,2,3], {1,2,3}, {1:2}]

        # allowed default values
        for annotation, default in zip(types, defaults):
            Header('test', annotation, default)

        # other default values must exceptions!
        for t_idx, annotation in enumerate(types):
            for d_idx, default in enumerate(defaults + ex_defaults):
                if isinstance(default, annotation):
                    continue
                exception_check = False
                try:
                    Header('test', annotation, default)
                except InvalidDefault:
                    exception_check = True
                self.assertTrue(exception_check)

        # All allows everything
        for default in defaults + ex_defaults:
            Header('test', All, default)

    def test_optional_valid(self):
        """Param optional validation test"""
        for flag in [True, False]:
            Header('test', optional=flag)

        for flag in [1, "1", 1.21, {1,2,3}, [1,2,3], {1:3}]:
            exception_check = False
            try:
                Header('test', optional=flag)
            except InvalidOptional:
                exception_check = True
            self.assertTrue(exception_check)

if __name__ == '__main__':
    unittest.main()





