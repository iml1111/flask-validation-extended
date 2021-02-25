import unittest
from flask_validation_extended.exceptions import (
    InvalidAnnotation,
    InvalidDefault,
    InvalidOptional
)
from flask_validation_extended.types import All, List, Dict, FileObj
from flask_validation_extended.params import Route, Query, Form, Header


class ParamTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.targets = [Route, Query, Form]

    def test_param_exists(self):
        for target in self.targets:
            self.assertTrue(target() is not None)

    def _annotation_valid(self, target):
        """Param annotation validation test"""

        # allowed types
        for type_i in [int, str, float, bool, All]:
            target(type_i)

        # other types must exception!
        for type_i in [list, dict, List, Dict, FileObj, set]:
            exception_check = False
            try:
                target(type_i)
            except InvalidAnnotation:
                exception_check = True
            self.assertTrue(exception_check)

    def test_annotation_valid(self):
        """Param annotation validation test"""
        for target in self.targets:
            self._annotation_valid(target)

    def _default_valid(self, target):
        """Route default validation test"""
        types = [int, str, float, bool]
        defaults = [1, "1", 1.13, True]
        ex_defaults = [[1,2,3], {1,2,3}, {1:2}]

        # allowed default values
        for annotation, default in zip(types, defaults):
            target(annotation, default)

        # other default values must exceptions!
        for t_idx, annotation in enumerate(types):
            for d_idx, default in enumerate(defaults + ex_defaults):
                if t_idx == d_idx:
                    continue
                exception_check = False
                try:
                    target(annotation, default)
                    # bool exceptions
                    if annotation is int and default in [True, False]:
                        exception_check = True
                except InvalidDefault:
                    exception_check = True
                self.assertTrue(exception_check)

        # All allows everything
        for default in defaults + ex_defaults:
            target(All, default)

    def test_default_valid(self):
        """Param default validation test"""
        for target in self.targets:
            self._default_valid(target)

    def test_optional_valid(self):
        """Param optional validation test"""
        for target in self.targets:

            for flag in [True, False]:
                target(optional=flag)

            for flag in [1, "1", 1.21, {1,2,3}, [1,2,3], {1:3}]:
                exception_check = False
                try:
                    target(optional=flag)
                except InvalidOptional:
                    exception_check = True
                self.assertTrue(exception_check)

if __name__ == '__main__':
    unittest.main()






