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
        response1 = self.client.post('/api/auth/register', self.user1_data, format='json')
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response1.data['message'], 'User Registered Successfully')
        self.assertEqual(response1.data['status'], 200)

        response2 = self.client.post('/api/auth/login', self.user1_login_data, format='json')
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response2.data['message'], 'User Logged In Successfully')
        self.assertEqual(response2.data['status'], 200)

        user1_token = response2.data['data']['access']

        response = self.client.get('/api/chatbox/', headers={
            'Authorization': f'Bearer {user1_token}'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Chatboxes retrieved successfully')
        self.assertEqual(response.data['status'], 200)
        self.assertEqual(response.data['data'], [])

    def test_chatbox_can_be_created(self):
        response1 = self.client.post('/api/auth/register', self.user1_data, format='json')
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response1.data['message'], 'User Registered Successfully')
        self.assertEqual(response1.data['status'], 200)

        response2 = self.client.post('/api/auth/register', self.user2_data, format='json')
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response2.data['message'], 'User Registered Successfully')
        self.assertEqual(response2.data['status'], 200)

        response3 = self.client.post('/api/auth/login', self.user1_login_data, format='json')
        self.assertEqual(response3.status_code, 200)
        self.assertEqual(response3.data['message'], 'User Logged In Successfully')
        self.assertEqual(response3.data['status'], 200)

        user1_id = response1.data['data']['id']
        user2_id = response2.data['data']['id']

        user1_token = response3.data['data']['access']

        response4 = self.client.post('/api/chatbox/',
                                     {
                                         "participants": [user2_id]
                                     },
                                     headers={
                                         'Authorization': f'Bearer {user1_token}'
                                     })
        self.assertEqual(response4.status_code, 200)
        self.assertEqual(response4.data['message'], 'Chatbox created successfully')
        self.assertEqual(response4.data['status'], 200)

        response5 = self.client.get('/api/chatbox/',
                                    headers={
                                        'Authorization': f'Bearer {user1_token}'
                                    })
        self.assertEqual(response5.status_code, 200)
        self.assertEqual(response5.data['message'], 'Chatboxes retrieved successfully')
        self.assertEqual(response5.data['status'], 200)
        self.assertEqual(len(response5.data['data']), 1)

        response6 = self.client.get(f'/api/chatbox/{response4.data["data"]["id"]}',
                                    headers={
                                        'Authorization': f'Bearer {user1_token}'
                                    })
        self.assertEqual(response6.status_code, 200)
        self.assertEqual(response6.data['message'], 'Chatbox fetched successfully')
        self.assertEqual(response6.data['status'], 200)
        self.assertEqual(len(response6.data['data']['participants']), 2)
        self.assertEqual(response6.data['data']['participants'][0], user2_id)
        self.assertEqual(response6.data['data']['participants'][1], user1_id)
