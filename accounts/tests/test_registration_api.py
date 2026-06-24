from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from tests_helpers.users import user_registration_data

User = get_user_model()


class RegistrationAPITests(APITestCase):
    """Test cases for the user registration API endpoint."""

    def setUp(self):
        """Set up valid user data for testing."""
        self.valid_user_data = user_registration_data()
        self.url = reverse("registration")

    def test_user_can_be_created(self):
        """Test can user created with valid data and that the user is created correctly."""

        self.valid_user_data.pop("repeated_password")

        user = User.objects.create_user(**self.valid_user_data)

        self.assertEqual(user.username, "exampleUsername")
        self.assertEqual(user.email, "example@mail.de")
        self.assertEqual(user.type, "customer")

    def test_registration_with_valid_data_return_201(self):
        """Test registration with valid data returns 201"""

        response = self.client.post(self.url, self.valid_user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(email=self.valid_user_data["email"])
        token = Token.objects.get(user=user)

        expected_response = {
            "token": token.key,
            "username": user.username,
            "email": user.email,
            "user_id": user.id,
        }

        self.assertEqual(response.data, expected_response)

    def test_registration_with_invalid_password_returns_400(self):
        """Test registration with mismatching passwords returns 400."""

        userdata = self.valid_user_data.copy()
        userdata["repeated_password"] = "falsePassword"

        response = self.client.post(self.url, userdata, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_with_invalid_email_returns_400(self):
        """Test registration with invalid email returns 400."""

        userdata = self.valid_user_data.copy()
        userdata["email"] = "exampleUsername.mail.de"

        response = self.client.post(self.url, userdata, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_with_duplicate_userdata_returns_400(self):
        """Test registration with duplicate user data returns 400."""

        response_user_1 = self.client.post(
            self.url,
            self.valid_user_data,
            format="json",
        )
        self.assertEqual(response_user_1.status_code, status.HTTP_201_CREATED)

        response_user_2 = self.client.post(
            self.url,
            self.valid_user_data,
            format="json",
        )
        self.assertEqual(response_user_2.status_code, status.HTTP_400_BAD_REQUEST)
