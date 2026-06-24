from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from tests_helpers.users import create_user, user_login_data

User = get_user_model()


class LoginAPIHappyPathTests(APITestCase):
    """Test cases for the login API endpoint, focusing on successful login scenarios."""

    def setUp(self):
        """Set up the test case with a valid user and login data."""

        self.url = reverse("login")
        self.valid_user = create_user()
        self.valid_login_data = user_login_data()

    def test_login_with_login_credentials_return_200(self):
        """
        Test login with valid credentials returns 200
        """
        response = self.client.post(self.url, self.valid_login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LoginAPIUnhappyPathTests(APITestCase):
    """Test cases for the login API endpoint, focusing on unsuccessful login scenarios."""

    def setUp(self):
        """Set up the test case with a valid user and login data."""

        self.url = reverse("login")
        self.valid_user = create_user()
        self.valid_login_data = user_login_data()

    def test_login_with_false_username_return_400(self):
        """Test login with an invalid username returns 400"""

        login_data = self.valid_login_data.copy()
        login_data["username"] = "falseUsername"

        response = self.client.post(self.url, login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_false_passwort_return_400(self):
        """Test login with an invalid password returns 400"""

        login_data = self.valid_login_data.copy()
        login_data["password"] = "falseExamplePassword"

        response = self.client.post(self.url, login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
