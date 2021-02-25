import unittest
from flask_validation_extended import Validator

class BasicsTestCase(unittest.TestCase):

    def setUp(self):
        self.validator = Validator()

    def tearDown(self):
        pass

    def test_module_exists(self):
        """Run Module Exists"""
        self.assertFalse(self.validator is None)

if __name__ == '__main__':
    unittest.main()