from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class RegistrationAPITestCase(APITestCase):

    def setUp(self):
        self.valid_user_data = {
            "username": "exampleUsername",
            "email": "exampleUsername@mail.de",
            "password": "examplePassword",
            "first_name": "Example",
            "last_name": "User",
            "type": "customer",
        }

    def test_user_can_be_created(self):

        user = User.objects.create_user(**self.valid_user_data)

        self.assertEqual(user.username, "exampleUsername")
        self.assertEqual(user.email, "exampleUsername@mail.de")
        self.assertEqual(user.first_name, "Example")
        self.assertEqual(user.last_name, "User")
        self.assertEqual(user.type, "customer")

    def test_user_can_registration(self):
        self.url = reverse("registration")

        response = self.client.post(self.url, self.valid_user_data, format="json")

        self.assertEqual(response.status_code, 201)
