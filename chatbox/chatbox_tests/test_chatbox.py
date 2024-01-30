from django.test import TestCase
from rest_framework.test import APIClient
from the_auth.the_auth_tests.test_login import LoginTestCase


class ChatboxTestCase(TestCase):
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

        self.user2_data = {
            "firstName": "Test",
            "middleName": "User",
            "lastName": "Two",
            "email": "testuser2@example.com",
            "username": "testuser2",
            "password": "testpassword123"
        }

        self.user3_data = {
            "firstName": "Test",
            "middleName": "User",
            "lastName": "Three",
            "email": "testuser3@example.com",
            "username": "testuser3",
            "password": "testpassword123"
        }

        self.user1_login_data = {
            "login": self.user1_data['username'],
            "password": self.user1_data['password']
        }

        self.user2_login_data = {
            "login": self.user2_data['username'],
            "password": self.user2_data['password']
        }

    login_user = LoginTestCase.login_user
    register_user = LoginTestCase.register_user

    def create_chatbox(self, participants, token):
        response = self.client.post('/api/chatbox/',
                                    {
                                        "participants": participants
                                    },
                                    headers={
                                        'Authorization': f'Bearer {token}'
                                    })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Chatbox created successfully')
        self.assertEqual(response.data['status'], 200)
        return response

    def get_chatboxes(self, token):
        response = self.client.get('/api/chatbox/',
                                   headers={
                                       'Authorization': f'Bearer {token}'
                                   })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Chatboxes retrieved successfully')
        self.assertEqual(response.data['status'], 200)
        return response

    def get_chatbox(self, chatbox_id, token):
        response = self.client.get(f'/api/chatbox/{chatbox_id}',
                                   headers={
                                       'Authorization': f'Bearer {token}'
                                   })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Chatbox fetched successfully')
        self.assertEqual(response.data['status'], 200)
        return response

    def send_message(self, chatbox_id, content, token):
        response = self.client.post(f'/api/chatbox/{chatbox_id}/message',
                                    {
                                        "content": content
                                    },
                                    headers={
                                        'Authorization': f'Bearer {token}'
                                    })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Message sent successfully')
        self.assertEqual(response.data['status'], 200)
        return response

    def test_chatbox_can_be_fetched(self):
        self.register_user(self.user1_data)
        response2 = self.login_user(self.user1_login_data)
        user1_token = response2.data['data']['access']
        response = self.get_chatboxes(user1_token)
        self.assertEqual(response.data['data'], [])

    def test_chatbox_can_be_created(self):
        response1 = self.register_user(self.user1_data)
        response2 = self.register_user(self.user2_data)
        response3 = self.login_user(self.user1_login_data)

        user1_id = response1.data['data']['id']
        user2_id = response2.data['data']['id']

        user1_token = response3.data['data']['access']

        response4 = self.create_chatbox([user2_id], user1_token)

        response5 = self.get_chatboxes(user1_token)
        self.assertEqual(len(response5.data['data']), 1)

        response6 = self.get_chatbox(response4.data["data"]["id"], user1_token)
        self.assertEqual(len(response6.data['data']['participants']), 2)
        self.assertEqual(response6.data['data']['participants'][0], user2_id)
        self.assertEqual(response6.data['data']['participants'][1], user1_id)

    def test_groupchat_can_be_created(self):
        response1 = self.register_user(self.user1_data)
        response2 = self.register_user(self.user2_data)
        response3 = self.register_user(self.user3_data)
        response4 = self.login_user(self.user1_login_data)

        user1_id = response1.data['data']['id']
        user2_id = response2.data['data']['id']
        user3_id = response3.data['data']['id']

        user1_token = response4.data['data']['access']

        response5 = self.create_chatbox([user2_id, user3_id], user1_token)

        response6 = self.get_chatboxes(user1_token)
        self.assertEqual(len(response6.data['data']), 1)

        response7 = self.get_chatbox(response5.data["data"]["id"], user1_token)
        self.assertEqual(len(response7.data['data']['participants']), 3)
        self.assertEqual(response7.data['data']['participants'][0], user3_id)
        self.assertEqual(response7.data['data']['participants'][1], user2_id)
        self.assertEqual(response7.data['data']['participants'][2], user1_id)

    def test_message_can_sent_in_private_chat(self):
        self.register_user(self.user1_data)
        response2 = self.register_user(self.user2_data)

        response3 = self.login_user(self.user1_login_data)
        response4 = self.login_user(self.user2_login_data)

        user2_id = response2.data['data']['id']

        user1_token = response3.data['data']['access']
        user2_token = response4.data['data']['access']

        response5 = self.create_chatbox([user2_id], user1_token)

        self.send_message(response5.data["data"]["id"], "Hello from user1", user1_token)
        self.send_message(response5.data["data"]["id"], "Hello from user2", user2_token)
