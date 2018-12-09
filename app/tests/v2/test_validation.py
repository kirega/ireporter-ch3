from ...api.v2.validators import validate_string
from unittest import TestCase
from marshmallow import ValidationError

class ValidationTestCase(TestCase):
    def test_false_on_empty_string(self):
       
       with self.assertRaises( ValidationError): validate_string("")