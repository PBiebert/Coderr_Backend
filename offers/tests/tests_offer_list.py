from rest_framework.test import APITestCase
from tests_helpers.users import create_user
from tests_helpers.offers import offer_data, create_offer
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework import status


class OfferApiTests(APITestCase):
    def setUp(self):
        self.valid_business_user = create_user(type="business")
        self.token, created = Token.objects.get_or_create(user=self.valid_business_user)
        self.url = reverse("offer-list")
        self.offer_data = offer_data()

    def test_post_offer_return_201(self):
        """Test that a business user can create an offer and receives a 201 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        response = self.client.post(self.url, data=offer_data(), format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_offer_without_title_return_400(self):
        """Test that trying to create an offer without a title returns a 400 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        invalid_data = offer_data()
        invalid_data.pop("title")

        response = self.client.post(self.url, data=invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_offer_with_two_details_return_400(self):
        """Test that trying to create an offer with two details returns a 400 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        invalid_data = offer_data()
        invalid_data["details"].pop()
        response = self.client.post(self.url, data=invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_offer_with_duplicate_offer_types_return_400(self):
        """Test that trying to create an offer with duplicate offer types returns a 400 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        invalid_data = offer_data()
        invalid_data["details"][0]["offer_type"] = "standard"
        response = self.client.post(self.url, data=invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_offer_is_not_authenticated_return_401(self):
        """Test that trying to create an offer without authentication returns a 401 response"""

        response = self.client.post(self.url, data=offer_data(), format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_offer_is_not_business_user_return_403(self):
        """Test that trying to create an offer with a non-business user returns a 403 response"""

        customer = create_user(username="customer_user", type="customer")
        token, created = Token.objects.get_or_create(user=customer)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)

        response = self.client.post(self.url, data=offer_data(), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_offers_return_200(self):
        """Test that a business user can retrieve offers and receives a 200 response"""

        create_offer(self.valid_business_user, offer_data())
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_offers_returns_paginated_response(self):
        create_offer(self.valid_business_user, offer_data())
        response = self.client.get(self.url, format="json")

        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("results", response.data)

        self.assertIsInstance(response.data["results"], list)

    def test_get_offers_valid_response_structure(self):
        create_offer(self.valid_business_user, offer_data())
        response = self.client.get(self.url, format="json")

        offer = response.data["results"][0]
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
            "user_details",
        }

        expected_details_keys = {"id", "url"}
        expected_user_details_keys = {"first_name", "last_name", "username"}

        self.assertIn("details", offer)
        self.assertIn("user_details", offer)
        self.assertEqual(set(offer.keys()), expected_offer_keys)
        self.assertEqual(set(offer["details"][0].keys()), expected_details_keys)
        self.assertEqual(set(offer["user_details"].keys()), expected_user_details_keys)

    def test_get_offers_with_invalid_url_return_404(self):
        invalid_url = f"{self.url}?page=2"
        response = self.client.get(invalid_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_offers_with_query_param_creator_id_return_200(self):
        offer = create_offer(self.valid_business_user, offer_data())
        creator_id_url = f"{self.url}?creator_id={offer.user.id}"
        response = self.client.get(creator_id_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_offers_with_invalid_query_param_creator_id_return_400(self):
        invalid_creator_id_url = f"{self.url}?creator_id=invalid"
        response = self.client.get(invalid_creator_id_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_offers_with_query_param_min_price_return_200(self):
        create_offer(self.valid_business_user, offer_data())
        min_price_url = f"{self.url}?min_price=200"
        response = self.client.get(min_price_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_offers_with_invalid_query_param_min_price_return_400(self):
        invalid_min_price_url = f"{self.url}?min_price=invalid"
        response = self.client.get(invalid_min_price_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_offers_with_query_param_max_delivery_time_return_200(self):
        create_offer(self.valid_business_user, offer_data())
        max_delivery_time_url = f"{self.url}?max_delivery_time=5"
        response = self.client.get(max_delivery_time_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_offers_with_ordering_by_updated_at_return_200(self):
        create_offer(self.valid_business_user, offer_data())
        ordering_url = f"{self.url}?ordering=-updated_at"
        response = self.client.get(ordering_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_offers_with_ordering_by_min_price_return_200(self):
        create_offer(self.valid_business_user, offer_data())
        ordering_url = f"{self.url}?ordering=min_price"
        response = self.client.get(ordering_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_offers_with_search_by_title_return_200(self):
        create_offer(self.valid_business_user, offer_data(title="Grafikdesign-Paket"))
        search_url = f"{self.url}?search=Grafikdesign-Paket"
        response = self.client.get(search_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_offers_with_search_by_description_return_200(self):
        create_offer(self.valid_business_user, offer_data())
        search_url = f"{self.url}?search=umfassendes"
        response = self.client.get(search_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_offers_with_page_size_return_200(self):
        create_offer(self.valid_business_user, offer_data())
        page_size_url = f"{self.url}?page_size=5"
        response = self.client.get(page_size_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
