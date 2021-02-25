import unittest
from flask_validation_extended.params import Json
from flask_validation_extended.exceptions import (
    InvalidAnnotation,
    InvalidDefault,
    InvalidOptional
)
from flask_validation_extended.types import All, List, Dict, FileObj


class ParamJsonTestCase(unittest.TestCase):

    def test_json_exists(self):
        self.assertTrue(Json() is not None)

    def test_annotation_valid(self):
        """Param Json annotation validation test"""
        types = [
            int, str, float, bool,
            list, dict, List(), Dict(), All
        ]
        # allowed types
        for type_i in types:
            Json(type_i)

        # other types must exception!
        for type_i in [FileObj, set]:
            exception_check = False
            try:
                Json(type_i)
            except InvalidAnnotation:
                exception_check = True
            self.assertTrue(exception_check)

    def test_default_valid(self):
        """Param Json default validation test"""
        types = [
            int, str, float, bool,
            list, dict,
            List(), Dict()
        ]
        defaults = [
            1, "1", 1.123, True,
            [1,2,3], {1:2},
            [1, 2, 7], {}
        ]
        ex_defaults = [{1,2,3}, List, List(), Dict, List(), All]

        # allowed default values
        for annotation, default in zip(types, defaults):
            Json(annotation, default)

        # other default values must exceptions!
        for annotation in types:
            for default in ex_defaults:
                exception_check = False
                try:
                    Json(annotation, default)
                except InvalidDefault:
                    exception_check = True
                self.assertTrue(exception_check)

    def test_optional_valid(self):
        """Param Json optional validation test"""
        for flag in [True, False]:
            Json(optional=flag)

        for flag in [1, "1", 1.21, {1,2,3}, [1,2,3], {1:3}]:
            exception_check = False
            try:
                Json(optional=flag)
            except InvalidOptional:
                exception_check = True
            self.assertTrue(exception_check)


if __name__ == '__main__':
    unittest.main()
