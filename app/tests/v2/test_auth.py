from flask import json
from .basetest import BaseTestCase
import unittest


class FlaskUserTest(BaseTestCase):
    """
        This class will cover all API endpoints for authentication
        The tests are ordered in the order of execution to enable for simple and easy of
        temporary test structures during the test.
    """

    def setUp(self):
        self.user_signup_data = json.dumps({
            "first_name": "Joseph",
            "last_name": "Mutiga",
            "other_names": "Kirega",
            "phonenumber": "0716570355",
            "email": "joseph.mutiga934@gmail.com",
            "username": "kirega",
            "password": "mtumkubwa"
        })
        self.login_data = json.dumps(
            {"username": "kirega", "password": "mtumkubwa"})
        self.wrong_login_data_format = json.dumps(
            {"username_ndfsame": "kirega", "password": "mtumkubwa"})
        self.nonexisting_user = json.dumps(
            {"username": "Tyron", "password": "mtumkubwa"})
        self.wrong_pwd = json.dumps(
            {"username": "kirega", "password": "4dfsjkdskfjsk"})

    def test_1_user_can_signup(self):
        "Test that by posting user data to the endpoint, it gets created"

        result = self.app.post('/api/v2/signup', data=self.user_signup_data)
        self.assertEqual(result.status_code, 201)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Sign Up successful. Welcome!")

    def test_2_user_sign_up_existing_username(self):
        "Test that by posting user data to the endpoint, it gets created"

        result = self.app.post('/api/v2/signup', data=self.user_signup_data)
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertEqual(data['message'],  "Username/Email already exists")

    def test_3_user_signup_with_empty_body(self):
        """Test that sign up fails for empty payloads"""

        result = self.app.post('/api/v2/signup', data=json.dumps({}))
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Missing or invalid field members")

    def test_4_login_with_right_credentials(self):
        """Test that a user/admin providing correct credentials in able to login"""
        result = self.app.post('/api/v2/login', data=self.login_data)
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Login Success!")

    def test_5_user_login_with_empty_body(self):
        """Test that a user providing empty payload fails"""
        result = self.app.post('/api/v2/login', data=json.dumps({}))
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Missing or invalid field members")

    def test_6_login_with_wrong_format(self):
        """Test that a user providing correct credentials in able to login"""
        result = self.app.post(
            '/api/v2/login', data=self.wrong_login_data_format)
        self.assertEqual(result.status_code, 400)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Missing or invalid field members")

    def test_7_login_with_nonexisting_user(self):
        """Test that a user providing correct credentials in is unable to login
         if user does not exist"""
        result = self.app.post(
            '/api/v2/login', data=self.nonexisting_user)
        self.assertEqual(result.status_code, 401)
        data = json.loads(result.data)
        self.assertEqual(
            data['message'], "Login Failed, Incorrect Username/Password!")

    def test_8_login_with_wrong_pwd(self):
        """Test that a user providing correct credentials in is unable to login
         if user does not exist"""
        result = self.app.post(
            '/api/v2/login', data=self.wrong_pwd)
        self.assertEqual(result.status_code, 401)
        data = json.loads(result.data)
        self.assertEqual(
            data['message'], "Login Failed, Incorrect Username/Password!")

    def test_9_logout(self):
        """Tests that the user can logout successfuly"""
        r = self.app.post('/api/v2/login', data=self.login_data)
        token = json.loads(r.data)['access_token']
        result = self.app.post('/api/v2/logout',
                               headers=dict(Authorization='Bearer ' + token))
        self.assertEqual(result.status_code, 200)
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Successfully logged out!")
        result = self.app.post('/api/v2/logout',
                               headers=dict(Authorization='Bearer ' + token))
        data = json.loads(result.data)
        self.assertEqual(data['message'], "Token has been revoked")


if __name__ == '__main__':
    unittest.main()
