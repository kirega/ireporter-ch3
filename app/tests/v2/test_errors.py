from unittest import TestCase
from .basetest import BaseTestCase
from flask import json

class ErrorsTestCase(BaseTestCase):
    def test_page_404(self):
        result = self.app.get('/api/v2/dfjakdjlfkjadlfka')
        self.assertEqual(result.status_code, 404)
        data = json.loads(result.data)
        self.assertEqual(data['message'],"Page not found")

    def test_page_405(self):
        result = self.app.put('/api/v2/incidents')
        self.assertEqual(result.status_code, 405)
        data = json.loads(result.data)
        self.assertIn("method is not allowed", data['message'])