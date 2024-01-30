from django.test import TestCase
from rest_framework.test import APIClient


class RegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1_data = {
            "firstName": "Test",
            "middleName": "User",
            "lastName": "One",
            "email": "testuser@example.com",
            "username": "testuser",
            "password": "testpassword123"
        }
        self.user1_login_data = {
            "login": self.user1_data['username'],
            "password": self.user1_data['password']
        }

        self.user2_data = {
            "firstName": "Test",
            "middleName": "User",
            "lastName": "Two",
            "email": "testuser2@example.com",
            "username": "testuser2",
            "password": "testpassword123"
        }

        self.user2_login_data = {
            "login": self.user2_data['username'],
            "password": self.user2_data['password']
        }

    def test_chatbox_can_be_fetched(self):
        response = self.client.get('/api/chatbox/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Chatboxes retrieved successfully')
        self.assertEqual(response.data['status'], 200)
        self.assertEqual(response.data['data'], [])

    def test_chatbox_can_be_created(self):
        response1 = self.client.post('/api/auth/register', self.user1_data, format='json')
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response1.data['message'], 'User Registered Successfully')
        print(response1.data)

        response2 = self.client.post('/api/auth/register', self.user2_data, format='json')
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response2.data['message'], 'User Registered Successfully')

        response3 = self.client.post('/api/auth/login', self.user1_login_data, format='json')
        self.assertEqual(response3.status_code, 200)
        self.assertEqual(response3.data['message'], 'User Logged In Successfully')

        user1_id = response1.data['data']['id']
        user2_id = response2.data['data']['id']

        response4 = self.client.post('/api/chatbox/',
                                     {
                                         "participants": [user1_id, user2_id]
                                     })
        self.assertEqual(response4.status_code, 200)
        self.assertEqual(response4.data['message'], 'Chatbox created successfully')
