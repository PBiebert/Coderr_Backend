from rest_framework.test import APITestCase
from tests_helpers.users import create_user
from tests_helpers.offers import offer_data
from rest_framework.authtoken.models import Token
from django.urls import reverse


class OfferApiTests(APITestCase):
    def setUp(self):
        self.valid_business_user = create_user(type="business")
        self.token, created = Token.objects.get_or_create(user=self.valid_business_user)
        self.url = reverse("offers")
        self.offer_data = offer_data()

    def test_post_offer_return_201(self):
        """Test that a business user can create an offer and receives a 201 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        response = self.client.post(self.url, data=offer_data(), format="json")
        self.assertEqual(response.status_code, 201)

    def test_post_offer_without_title_return_400(self):
        """Test that trying to create an offer without a title returns a 400 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        invalid_data = offer_data()
        invalid_data.pop("title")

        response = self.client.post(self.url, data=invalid_data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_post_offer_with_two_details_return_400(self):
        """Test that trying to create an offer with two details returns a 400 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        invalid_data = offer_data()
        invalid_data["details"].pop()
        response = self.client.post(self.url, data=invalid_data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_post_offer_with_duplicate_offer_types_return_400(self):
        """Test that trying to create an offer with duplicate offer types returns a 400 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        invalid_data = offer_data()
        invalid_data["details"][0]["offer_type"] = "standard"
        response = self.client.post(self.url, data=invalid_data, format="json")
        self.assertEqual(response.status_code, 400)
