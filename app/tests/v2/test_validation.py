from ...api.v2.validators import validate_string, password_strength
from unittest import TestCase
from marshmallow import ValidationError

class ValidationTestCase(TestCase):
    def test_false_on_empty_string(self):
       
       with self.assertRaises( ValidationError): validate_string("")

    def test_password_strength(self):
        with self.assertRaises( ValidationError): password_strength("2323r3")