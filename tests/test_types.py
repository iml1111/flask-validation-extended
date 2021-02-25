import unittest
from itertools import combinations
from flask_validation_extended.types import List, Dict, All, type_check
from flask_validation_extended.exceptions import (
    InvalidCustomTypeArgument
)

class TypeTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.targets = [List, Dict]
        self.types = [
            int, str, float, bool,
            list, dict, List(), Dict(), All
        ]
        self.invalid_types = [
            1, "1", 1.2, True, False,
            [1,2,3], {1:2}, {1,2,3}
        ]

    def _test_type(self, target):
        """custom type List validation test"""

        # allowed cases
        target()
        for type_i in self.types:
            target(type_i)

        for i in range(1, len(self.types)):
            for comb in combinations(self.types, i):
                target(comb)

        # not allowed cases
        for type_i in self.invalid_types:
            except_check = False
            try:
                target(type_i)
            except InvalidCustomTypeArgument:
                except_check = True
            self.assertTrue(except_check)

        for i in range(1, len(self.invalid_types)):
            for comb in combinations(self.invalid_types, i):
                except_check = False
                try:
                    target(comb)
                except InvalidCustomTypeArgument:
                    except_check = True
                self.assertTrue(except_check)

        for valid_type in self.types:
            types = self.invalid_types + [valid_type]
            for i in range(2, len(types)):
                for comb in combinations(types, i):
                    except_check = False
                    try:
                        target(comb)
                    except InvalidCustomTypeArgument:
                        except_check = True
                    self.assertTrue(except_check)

        for i in range(1, len(self.types)):
            for comb in combinations(self.types, i):
                for invalid_type in self.invalid_types:
                    temp_comb = list(comb) + [invalid_type]
                    except_check = False
                    try:
                        target(temp_comb)
                    except InvalidCustomTypeArgument:
                        except_check = True
                    self.assertTrue(except_check)

    def test_types(self):
        """custom type validation test"""
        for target in self.targets:
            self._test_type(target)


if __name__ == '__main__':
    unittest.main()
