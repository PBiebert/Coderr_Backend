from rest_framework.test import APITestCase
from django.urls import reverse
from tests_helpers.users import create_business_user
from rest_framework import status
from rest_framework.authtoken.models import Token


class ProfileAPITests(APITestCase):
    def setUp(self):
        self.valid_business_user = create_business_user()
        self.token, created = Token.objects.get_or_create(user=self.valid_business_user)
        self.url_with_valid_pk = reverse(
            "profile_details", kwargs={"pk": self.valid_business_user.id}
        )
        self.url_with_invalid_pk = reverse(
            "profile_details", kwargs={"pk": self.valid_business_user.id + 99}
        )

    def test_created_user_has_profile_with_default_values(self):
        self.assertTrue(hasattr(self.valid_business_user, "profile"))
        self.assertEqual(self.valid_business_user.first_name, "")
        self.assertEqual(self.valid_business_user.last_name, "")
        self.assertEqual(self.valid_business_user.profile.location, "")
        self.assertEqual(self.valid_business_user.profile.tel, "")
        self.assertEqual(self.valid_business_user.profile.description, "")
        self.assertEqual(self.valid_business_user.profile.working_hours, "")

    def test_get_profile_return_200(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get(self.url_with_valid_pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_profile_unauthenticated_return_401(self):
        response = self.client.get(self.url_with_valid_pk)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profile_user_not_found_return_404(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get(self.url_with_invalid_pk)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_profile_returns_expected_response(self):

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get(self.url_with_valid_pk)

        valid_response = {
            "user": self.valid_business_user.id,
            "username": self.valid_business_user.username,
            "first_name": self.valid_business_user.first_name,
            "last_name": self.valid_business_user.last_name,
            "file": self.valid_business_user.profile.file or None,
            "location": self.valid_business_user.profile.location,
            "tel": self.valid_business_user.profile.tel,
            "description": self.valid_business_user.profile.description,
            "working_hours": self.valid_business_user.profile.working_hours,
            "type": self.valid_business_user.type,
            "email": self.valid_business_user.email,
            "created_at": response.data,
        }

        print(f"valid_response{valid_response}")
        print(f"")
        print(f"response{response.data}")
        self.assertEqual(response.data, valid_response)
