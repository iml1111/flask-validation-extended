import unittest
from itertools import combinations
from flask_validation_extended.exceptions import (
    InvalidAnnotation,
    InvalidDefault,
    InvalidOptional
)
from flask_validation_extended.types import All, List, Dict, FileObj
from flask_validation_extended.params import Json, File
from flask_validation_extended.rules import (
    MinLen, MaxLen, Min, Max, In,
    Number, Strip, IsoDatetime, 
    Datetime, Email, Regex, Ext
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
        rule = Email()

        good_cases = [
            'asd@asd',
            'shin10256@gmail.com',
            '_asd_@asd.co.kr',
        ]
        for case in good_cases:
            self.assertTrue(rule.is_valid(case))
        bad_cases = [
            'asdasd',
            '1',
            'asd@@asd.com',
        ]
        for case in bad_cases:
            self.assertFalse(rule.is_valid(case))

    def test_regex(self):
        # Number Regex sample
        rule = Regex(r'^[0-9]*$')

        good_cases = ["1", "112346897", "010230123"]
        for case in good_cases:
            self.assertTrue(rule.is_valid(case))

        bad_cases = ['asd', '1111a', '56987_']
        for case in bad_cases:
            self.assertFalse(rule.is_valid(case))

    def _validate_ext(self, exts, good_cases, bad_cases):

        rule = Ext(exts)

        for case in good_cases:
            self.assertTrue(rule.is_valid(case))

        for case in bad_cases:
            self.assertFalse(rule.is_valid(case))

    def test_ext(self):

        # TestFile
        class TF:
            def __init__(self, filename):
                self.filename = filename

        self._validate_ext(
            exts='png',
            good_cases=[
                [TF('asd.png')],
                [TF('a.png'),TF('jpg.png'),TF('png.png')],
            ],
            bad_cases=[
                [TF('asd.peng')],
                [TF('a.exe'), TF('a.jpg'), TF('a.doc')],
                [TF('a.png'), TF('z.png'), TF('a.pptx')]
            ]
        )
        self._validate_ext(
            exts=['png', 'jpg', 'jpeg'],
            good_cases=[
                [TF('asd.png')],
                [TF('a.png'),TF('jpg.jpg'),TF('png.png')],
                [TF('a.png'),TF('jpg.jpg'),TF('a.jpeg')],
            ],
            bad_cases=[
                [TF('asd.peng')],
                [TF('a.exe'), TF('a.jpg'), TF('a.doc')],
                [TF('a.jpeg'), TF('z.jpg'), TF('a.pptx')]
            ]
        )

    def test_valid_rule_annotation(self):
        """Annotation / Rule validate test"""
        str_based_rules = [
            MinLen(5), MaxLen(5), In(["asd", "zxc"]),
            Number(), Strip(), IsoDatetime(),
            Datetime("yyyy"), Email(), Regex(r".*")    
        ]

        for i in range(1, len(str_based_rules) + 1):
            for comb in combinations(str_based_rules, i):
                Json(str, rules=comb)


if __name__ == '__main__':
    unittest.main()

