from django.test import TestCase
from rest_framework.test import APIClient
from .models import User


class RegistrationTestCase(TestCase):
    test_data = dict()

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

    def test_user_registration_success(self):
        response = self.client.post('/api/register', self.test_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)
        for key, value in self.test_data.items():
            user = User.objects.get()
            self.assertEqual(getattr(user, key), value)

    def test_user_registration_failure(self):
        test_data_copy = self.test_data.copy()
        test_data_copy["email"] = "invalidemail"
        response = self.client.post('/api/register', test_data_copy, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(response.data['email'], ['Enter a valid email address.'])

    def test_user_registration_duplicate(self):
        response = self.client.post('/api/register', self.test_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.data['message'], 'User Registered Successfully')

        response = self.client.post('/api/register', self.test_data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.data["username"], ["User with this username already exists."])
        self.assertEqual(response.data["email"], ["User with this email already exists."])

    def test_user_registration_blank(self):
        test_data_copy = self.test_data.copy()
        test_data_copy["firstName"] = ""
        test_data_copy["lastName"] = ""
        test_data_copy["email"] = ""
        test_data_copy["username"] = ""
        test_data_copy["password"] = ""
        response = self.client.post('/api/register', test_data_copy, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(response.data["firstName"], ["This field may not be blank."])
        self.assertEqual(response.data["lastName"], ["This field may not be blank."])
        self.assertEqual(response.data["email"], ["This field may not be blank."])
        self.assertEqual(response.data["username"], ["This field may not be blank."])
        self.assertEqual(response.data["password"], ["This field may not be blank."])

    def test_user_registration_missing(self):
        test_data_copy = self.test_data.copy()
        del test_data_copy["firstName"]
        del test_data_copy["lastName"]
        del test_data_copy["email"]
        del test_data_copy["username"]
        del test_data_copy["password"]
        response = self.client.post('/api/register', test_data_copy, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(response.data["firstName"], ["This field is required."])
        self.assertEqual(response.data["lastName"], ["This field is required."])
        self.assertEqual(response.data["email"], ["This field is required."])
        self.assertEqual(response.data["username"], ["This field is required."])
        self.assertEqual(response.data["password"], ["This field is required."])
