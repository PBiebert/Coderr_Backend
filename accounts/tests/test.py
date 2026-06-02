from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class RegistrationAPITestCaseHappy(APITestCase):

    def setUp(self):
        """
        Set up valid user data for testing
        """

        self.valid_user_data = {
            "username": "exampleUsername",
            "email": "exampleUsername@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "customer",
        }

    def test_user_can_be_created(self):
        """
        Test can user create
        """

        self.valid_user_data.pop("repeated_password")

        user = User.objects.create_user(**self.valid_user_data)

        self.assertEqual(user.username, "exampleUsername")
        self.assertEqual(user.email, "exampleUsername@mail.de")
        self.assertEqual(user.type, "customer")

    def test_registration_with_valid_data_returns_201(self):
        """
        Test registration with valid data returns 201
        """

        self.url = reverse("registration")
        response = self.client.post(self.url, self.valid_user_data, format="json")
        print(response.data)
        self.assertEqual(response.status_code, 201)

        user = User.objects.get(email=self.valid_user_data["email"])
        token = Token.objects.get(user=user)

        expected_response = {
            "token": token.key,
            "username": user.username,
            "email": user.email,
            "user_id": user.id,
        }

        self.assertEqual(response.data, expected_response)


class RegistrationAPITestCaseUnhappy(APITestCase):

    def setUp(self):
        pass

    def test_registration_with_invalid_password_returns_400(self):
        """
        Test registration with invalid password
        """

        userdata = {
            "username": "exampleUsername",
            "email": "exampleUsername@mail.de",
            "password": "examplePassword",
            "repeated_password": "falsePassword",
            "type": "customer",
        }

        self.url = reverse("registration")
        response = self.client.post(self.url, userdata, format="json")
        self.assertEqual(response.status_code, 400)

    def test_registration_with_invalid_email_returns_400(self):
        """
        Test registration with invalid email returns 400
        """

        userdata = {
            "username": "exampleUsername",
            "email": "exampleUsername.mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "customer",
        }

        self.url = reverse("registration")
        response = self.client.post(self.url, userdata, format="json")
        self.assertEqual(response.status_code, 400)

    def test_Register_2_users_with_the_same_userdata_returns_400(self):
        """
        Test if the same user can be registered twice
        """

        userdata = {
            "username": "exampleUsername",
            "email": "exampleUsername@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "customer",
        }

        self.url = reverse("registration")
        response_user_1 = self.client.post(self.url, userdata, format="json")
        self.assertEqual(response_user_1.status_code, 201)

        response_user_2 = self.client.post(self.url, userdata, format="json")
        self.assertEqual(response_user_2.status_code, 400)
