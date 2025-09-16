# finance/tests/test_users.py
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User

class UserRegistrationTest(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.user_data = {
            "username": "testuser",
            "password": "testpassword123",
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User"
        }

    def test_user_registration(self):
        """
        Test to create a new user via the registration endpoint.
        It only creates and verifies that it was saved in the database.
        """
        response = self.client.post(self.register_url, self.user_data, format='json')

        # Check status code 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the user was created in the database
        user_exists = User.objects.filter(username=self.user_data['username']).exists()
        self.assertTrue(user_exists)

        # Check that the response contains the username and email
        self.assertEqual(response.data["username"], self.user_data["username"])
        self.assertEqual(response.data["email"], self.user_data["email"])
