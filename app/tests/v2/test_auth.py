from flask import json
from .basetest import BaseTestCase
import unittest


class FlaskUserTest(BaseTestCase):
    """
        This class will cover all API endpoints for authentication
    """
    def setUp(self):
        self.user_signup_data = json.dumps({
            "first_name": "Joseph",
            "last_name": "Mutiga",
            "other_names": "Kirega",
            "phonenumber": "0716570355",
            "email": "joseph.mutiga934@gmail.com",
            "username": "joedfs",
            "password": "1234"
        })

        
    def test_user_can_signup(self):
        "Test that by posting user data to the endpoint, it gets created"

        result = self.app.post('/api/v2/signup', data=self.user_signup_data)
        self.assertEqual(result.status_code, 201)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Sign Up successful. Welcome!")

    def test_user_sign_up_existing_username(self):
        "Test that by posting user data to the endpoint, it gets created"
        
        result = self.app.post('/api/v2/signup', data=self.user_signup_data)
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertEqual(data['message'],  "Username/Email already exists")

    def test_user_signup_with_empty_body(self):
        """Test that sign up fails for empty payloads"""

        result = self.app.post('/api/v2/signup', data=json.dumps({}))
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Missing or invalid field members")





if __name__ == '__main__':
    unittest.main()
