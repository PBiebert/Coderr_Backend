from rest_framework.test import APITestCase
from tests_helpers.users import create_user
from tests_helpers.offers import offer_data, create_offer
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework import status


class OfferDetailsApiTests(APITestCase):
    def setUp(self):
        self.valid_user = create_user()
        self.token, created = Token.objects.get_or_create(user=self.valid_user)
        self.offer = create_offer(self.valid_user, offer_data())
        self.valid_url = reverse("offers-details", kwargs={"pk": self.offer.id})

    def test_get_offer_details_return_200(self):
        """Test that a user can retrieve offer details with a 200 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get(self.valid_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_offer_details_validate_response_data(self):
        """Test that the response data from a GET request to retrieve offer details contains the expected fields"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get(self.valid_url)
        data = response.data

        expected_offer_keys = {
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
            "min_price",
            "min_delivery_time",
        }

        expected_offer_detail_keys = {
            "id",
            "url",
        }

        self.assertEqual(set(data.keys()), expected_offer_keys)
        for detail in data["details"]:
            self.assertEqual(set(detail.keys()), expected_offer_detail_keys)

    def test_get_offer_details_unauthenticated_user_return_401(self):
        """Test that an unauthenticated user cannot retrieve offer details and receives a 401 response"""

        response = self.client.get(self.valid_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_offer_details_non_existent_offer_return_404(self):
        """Test that retrieving details of a non-existent offer returns a 404 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        invalid_url = reverse("offers-details", kwargs={"pk": 9999})
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_offer_details_return_204(self):
        """Test that a user can delete an offer and receives a 204 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.delete(self.valid_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_offer_details_unauthenticated_user_return_401(self):
        """Test that an unauthenticated user cannot delete an offer and receives a 401 response"""

        response = self.client.delete(self.valid_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_offer_details_is_not_owner_return_403(self):
        """Test that a user cannot delete an offer they do not own and receives a 403 response"""

        other_user = create_user(username="otheruser", email="otheruser@mail.de")
        other_token, created = Token.objects.get_or_create(user=other_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + other_token.key)
        response = self.client.delete(self.valid_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_offer_details_non_existent_offer_return_404(self):
        """Test that deleting a non-existent offer returns a 404 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        invalid_url = reverse("offers-details", kwargs={"pk": 99})
        response = self.client.delete(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_offer_details_return_200(self):
        """Test that a user can update an offer and receives a 200 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        updated_data = offer_data(title="Updated Grafikdesign-Paket")
        updated_data["details"][0]["title"] = "Basic Design Updated"
        updated_data["details"][0]["delivery_time_in_days"] = 6

        response = self.client.patch(self.valid_url, updated_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Grafikdesign-Paket")
        self.assertEqual(response.data["details"][0]["title"], "Basic Design Updated")
        self.assertEqual(response.data["details"][0]["delivery_time_in_days"], 6)

    def test_update_offer_details_with_invalid_data_return_400(self):
        """Test that updating an offer with invalid data returns a 400 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        invalid_data = offer_data(title="")  # Title cannot be empty

        response = self.client.patch(self.valid_url, invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_offer_details_unauthenticated_user_return_401(self):
        """Test that an unauthenticated user cannot update an offer and receives a 401 response"""

        updated_data = offer_data(title="Updated Grafikdesign-Paket")
        response = self.client.patch(self.valid_url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_offer_details_is_not_owner_return_403(self):
        """Test that a user cannot update an offer they do not own and receives a 403 response"""

        other_user = create_user(username="otheruser", email="otheruser@mail.de")
        other_token, created = Token.objects.get_or_create(user=other_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + other_token.key)
        updated_data = offer_data(title="Updated Grafikdesign-Paket")
        response = self.client.patch(self.valid_url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_offer_details_non_existent_offer_return_404(self):
        """Test that updating a non-existent offer returns a 404 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        invalid_url = reverse("offers-details", kwargs={"pk": 99})
        updated_data = offer_data(title="Updated Grafikdesign-Paket")
        response = self.client.patch(invalid_url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
