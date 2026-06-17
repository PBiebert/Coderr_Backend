from rest_framework.test import APITestCase
from tests_helpers.users import create_user
from tests_helpers.offers import offer_data, create_offer
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework import status


class OfferSingleDetailApiTests(APITestCase):
    def setUp(self):
        self.valid_user = create_user()
        self.token, created = Token.objects.get_or_create(user=self.valid_user)
        self.offer = create_offer(self.valid_user, offer_data())
        self.detail = self.offer.details.get(offer_type="standard")
        self.valid_url = reverse("offers_single_detail", kwargs={"pk": self.detail.id})

    def test_get_offer_single_detail_return_200(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get(self.valid_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.detail.id)

    def test_get_offer_single_detail_validate_response_data(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get(self.valid_url)
        data = response.data

        expected_keys = {
            "id",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        }

        self.assertEqual(set(data.keys()), expected_keys)
        self.assertIsInstance(data["features"], list)

    def test_get_offer_single_detail_unauthenticated_user_return_401(self):
        response = self.client.get(self.valid_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_offer_single_detail_non_existent_detail_return_404(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        invalid_url = reverse("offers_single_detail", kwargs={"pk": 99})
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
