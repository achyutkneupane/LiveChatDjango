from django.test import TestCase
from rest_framework.test import APIClient
from api.models import User
import bcrypt


class RegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_data = {
            "firstName": "Test",
            "middleName": "Middle",
            "lastName": "User",
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "testpassword123"
        }
        self.login_data = {
            "login": self.test_data['username'],
            "password": self.test_data['password']
        }

    def test_user_can_login(self):
        response = self.client.post('/api/auth/register', self.test_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.data['message'], 'User Registered Successfully')

        response = self.client.post('/api/auth/login', self.login_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'User Logged In Successfully')

    def test_user_can_login_with_email(self):
        new_login_data = self.login_data.copy()
        new_login_data['login'] = self.test_data['email']

        response = self.client.post('/api/auth/register', self.test_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.data['message'], 'User Registered Successfully')

        response = self.client.post('/api/auth/login', new_login_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'User Logged In Successfully')

    def test_user_cannot_login_with_invalid_login(self):
        new_login_data = self.login_data.copy()
        new_login_data['login'] = 'invalidlogin'

        response = self.client.post('/api/auth/register', self.test_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.data['message'], 'User Registered Successfully')

        response = self.client.post('/api/auth/login', new_login_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['login'], ['User with this username does not exist'])