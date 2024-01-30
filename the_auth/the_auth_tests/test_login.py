from django.test import TestCase
from rest_framework.test import APIClient
from the_auth.models import User


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

    def register_user(self, user_data):
        response = self.client.post('/api/auth/register', user_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'User Registered Successfully')
        self.assertEqual(response.data['status'], 200)
        return response

    def login_user(self, user_login_data):
        response = self.client.post('/api/auth/login', user_login_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'User Logged In Successfully')
        self.assertEqual(response.data['status'], 200)
        return response

    def test_user_can_login(self):
        self.register_user(self.test_data)
        self.login_user(self.login_data)

    def test_user_can_login_with_email(self):
        new_login_data = self.login_data.copy()
        new_login_data['login'] = self.test_data['email']
        self.register_user(self.test_data)
        self.login_user(new_login_data)

    def test_user_cannot_login_with_invalid_login(self):
        new_login_data = self.login_data.copy()
        new_login_data['login'] = 'invalidlogin'

        self.register_user(self.test_data)

        response = self.client.post('/api/auth/login', new_login_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['login'], ['User with this username does not exist'])

    def test_user_cannot_login_with_invalid_password(self):
        new_login_data = self.login_data.copy()
        new_login_data['password'] = 'invalidpassword'

        self.register_user(self.test_data)
        self.assertEqual(User.objects.count(), 1)

        response = self.client.post('/api/auth/login', new_login_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['password'], ['Invalid password'])

    def test_user_cannot_login_with_blank_values(self):
        new_login_data = self.login_data.copy()
        new_login_data['login'] = ''
        new_login_data['password'] = ''

        self.register_user(self.test_data)

        response = self.client.post('/api/auth/login', new_login_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['login'], ['This field may not be blank.'])
        self.assertEqual(response.data['password'], ['This field may not be blank.'])

    def test_user_cannot_login_with_missing_values(self):
        new_login_data = self.login_data.copy()
        del new_login_data['login']
        del new_login_data['password']

        self.register_user(self.test_data)

        response = self.client.post('/api/auth/login', new_login_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['login'], ['This field is required.'])
        self.assertEqual(response.data['password'], ['This field is required.'])

    def test_user_cannot_login_with_invalid_login_and_password(self):
        new_login_data = self.login_data.copy()
        new_login_data['login'] = 'invalidlogin'
        new_login_data['password'] = 'invalidpassword'

        self.register_user(self.test_data)

        response = self.client.post('/api/auth/login', new_login_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['login'], ['User with this username does not exist'])