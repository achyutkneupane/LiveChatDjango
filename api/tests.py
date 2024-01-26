from django.test import TestCase

# Create your tests here.
# The registration test

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import User


class RegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration_success(self):
        test_data = {
            'firstName': 'Test',
            'middleName': 'Middle',
            'lastName': 'User',
            'email': 'testuser@example.com',
            'username': 'testuser',
            'password': 'testpassword123'
        }
        response = self.client.post('/api/register', test_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().firstName, 'Test')
        self.assertEqual(User.objects.get().middleName, 'Middle')
        self.assertEqual(User.objects.get().lastName, 'User')
        self.assertEqual(User.objects.get().email, 'testuser@example.com')
        self.assertEqual(User.objects.get().username, 'testuser')
        self.assertEqual(User.objects.get().password, 'testpassword123')