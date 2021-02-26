import unittest
from flask_validation_extended.exceptions import (
    InvalidAnnotation,
    InvalidDefault,
    InvalidOptional
)
from flask_validation_extended.types import All, List, Dict, FileObj
from flask_validation_extended.params import Route, Query, Form
from flask_validation_extended.rules import (
    MinLen, MaxLen, Min, Max, In,
    Number, Strip, IsoDatetime, Datetime
)


class RuleTestCase(unittest.TestCase):

    def test_min_len(self):
        rule = MinLen(5)
        test_cases = ["A" * 10, [1] * 10]

        for test_case in test_cases:
            for idx in range(5):
                valid = rule.is_valid(test_case[:idx])
                self.assertFalse(valid)

            for idx in range(6, 11):
                valid = rule.is_valid(test_case[:idx])
                self.assertTrue(valid)

    def test_max_len(self):
        rule = MaxLen(5)
        test_cases = ["A" * 10, [1] * 10]

        for test_case in test_cases:
            for idx in range(5):
                valid = rule.is_valid(test_case[:idx])
                self.assertTrue(valid)

            for idx in range(6, 11):
                valid = rule.is_valid(test_case[:idx])
                self.assertFalse(valid)

    def test_min(self):
        rule = Min(5)
        for i in range(5):
            self.assertFalse(rule.is_valid(i))
        for i in range(6, 11):
            self.assertTrue(rule.is_valid(i))

    def test_max(self):
        rule = Max(5)
        for i in range(5):
            self.assertTrue(rule.is_valid(i))
        for i in range(6, 11):
            self.assertFalse(rule.is_valid(i))

    def test_in(self):
        rule = In([1,2,3])

        for i in range(1, 4):
            self.assertTrue(rule.is_valid(i))

        for i in range(4, 10):
            self.assertFalse(rule.is_valid(i))

        for i in [{1:2}, [1,2,3], {1,2,3}]:
            self.assertFalse(rule.is_valid(i))

    def test_number(self):
        rule = Number()

        for i in map(str, range(10)):
            self.assertTrue(rule.is_valid(i))

        bad_cases = [
            "asd", "1a", "1.2",
            "1233213132.1", "a1"
        ]
        for i in map(str, bad_cases):
            self.assertFalse(rule.is_valid(i))

    def test_strip(self):
        rule = Strip()

        good_cases = [
            "asdasdasdasd",
            "IM IML!",
            "Goooo   oood!"
        ]
        for case in good_cases:
            self.assertTrue(rule.is_valid(case))

        bad_cases = ["\t", "\n", "\r", " "]
        for case in good_cases:
            for prefix in bad_cases:
                self.assertFalse(rule.is_valid(prefix + case))
                self.assertFalse(rule.is_valid(case + prefix))
                self.assertFalse(rule.is_valid(prefix + case + prefix))

    def test_isodatetime(self):
        rule = IsoDatetime()

        good_cases = [
            "2000-10-31T01:30:00.000-05:00",
            "2017-03-16T17:40:00+09:00",
            "2017-03-16",
            "2017-03-16 19:55:28.084217",
            "2017-03-16 10:55:28.084274",
            "2017-03-16 10:55:28"
        ]
        for case in good_cases:
            self.assertTrue(rule.is_valid(case))
        bad_cases = [
            "2000-10-3101:30:00.000-05:00",
            "2017-03-1617:40:00+09:00",
            "2017-3-16",
            "2017-03-1 19:55:28084217",
            "2017-03-16  10:55:28"
        ]
        for case in bad_cases:
            self.assertFalse(rule.is_valid(case))

    def test_email(self):
        pass

    def test_regex(self):
        pass

    def test_ext(self):
        pass

    def test_valid_rule_annotation(self):
        pass
