from rest_framework.test import APITestCase
from django.urls import reverse
from tests_helpers.users import create_user, fill_database_with_users
from tests_helpers.profile import profile_update_data
from rest_framework import status
from rest_framework.authtoken.models import Token


class ProfileAPITests(APITestCase):
    def setUp(self):
        """Set up valid user and profile data for testing"""

        self.valid_business_user = create_user(type="business")
        self.token, created = Token.objects.get_or_create(user=self.valid_business_user)
        self.update_data = profile_update_data()
        self.url_with_valid_pk = reverse(
            "profile_details", kwargs={"pk": self.valid_business_user.id}
        )
        self.url_with_invalid_pk = reverse(
            "profile_details", kwargs={"pk": self.valid_business_user.id + 99}
        )
        self.url_business = reverse("business_profiles")
        self.url_customer = reverse("customer_profiles")

    def test_created_user_has_profile_with_default_values(self):
        """Test that a profile is automatically created for a new user and has default values"""

        self.assertTrue(hasattr(self.valid_business_user, "profile"))
        self.assertEqual(self.valid_business_user.first_name, "")
        self.assertEqual(self.valid_business_user.last_name, "")
        self.assertEqual(self.valid_business_user.profile.location, "")
        self.assertEqual(self.valid_business_user.profile.tel, "")
        self.assertEqual(self.valid_business_user.profile.description, "")
        self.assertEqual(self.valid_business_user.profile.working_hours, "")

    def test_get_profile_return_200(self):
        """Test that a user can retrieve their profile with a 200 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get(self.url_with_valid_pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_profile_unauthenticated_return_401(self):
        """Test that an unauthenticated user cannot retrieve a profile and receives a 401 response"""

        response = self.client.get(self.url_with_valid_pk)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_profile_user_not_found_return_404(self):
        """Test that trying to retrieve a non-existent profile returns a 404 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get(self.url_with_invalid_pk)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_profile_returns_expected_response(self):
        """Test that the profile retrieval returns the expected data structure and values"""

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
        }
        response.data.pop("created_at")
        self.assertEqual(response.data, valid_response)

    def test_patch_profile_update_fields_return_200(self):
        """Test that a user can update their profile fields and receives a 200 response"""
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        response = self.client.patch(
            self.url_with_valid_pk, self.update_data, format="multipart"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_profile_unauthenticated_return_401(self):
        """Test that an unauthenticated user cannot update a profile and receives a 401 response"""

        response = self.client.patch(
            self.url_with_valid_pk, self.update_data, format="multipart"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_profile_user_not_authorized_return_403(self):
        """Test that a user cannot update another user's profile and receives a 403 response"""

        other_user = create_user(username="otherUser")
        other_token, created = Token.objects.get_or_create(user=other_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + other_token.key)

        response = self.client.patch(
            self.url_with_valid_pk, self.update_data, format="multipart"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_profile_user_not_found_return_404(self):
        """Test that trying to update a non-existent profile returns a 404 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.patch(
            self.url_with_invalid_pk, self.update_data, format="multipart"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_only_business_users(self):
        """Test that the business profiles endpoint returns only profiles of users with type "business"""

        fill_database_with_users()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get(self.url_business, format="json")

        for profile in response.data:
            self.assertEqual(profile["type"], "business")

    def test_get_all_business_return_200(self):
        """Test that a user can retrieve a list of all customers with a 200 response"""

        fill_database_with_users()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get(self.url_business, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_business_return_401(self):
        """Test that an unauthenticated user cannot retrieve the list of customers and receives a 401 response"""

        response = self.client.get(self.url_business, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_only_customer_users(self):
        """Test that the customer profiles endpoint returns only profiles of users with type "customer"""

        fill_database_with_users()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get(self.url_customer, format="json")

        for profile in response.data:
            self.assertEqual(profile["type"], "customer")

    def test_get_all_customers_return_200(self):
        """Test that a user can retrieve a list of all customers with a 200 response"""
        fill_database_with_users()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get(self.url_customer, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_customers_return_401(self):
        """Test that an unauthenticated user cannot retrieve the list of customers and receives a 401 response"""

        response = self.client.get(self.url_customer, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
