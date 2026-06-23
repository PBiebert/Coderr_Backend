from rest_framework.test import APITestCase
from tests_helpers.users import create_user
from tests_helpers.reviews import review_data, create_review
from tests_helpers.offers import offer_data, create_offer
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework import status as http_status


class PlatformBaseInfoViewTestCase(APITestCase):
    def setUp(self):
        self.customer_user = create_user()
        self.customer_token = Token.objects.create(user=self.customer_user)

        self.business_users = []
        for i in range(3):
            business_user = create_user(username=f"exampleBusiness{i}", type="business")
            self.business_users.append(business_user)

        self.offers = []
        for business_user in self.business_users:
            self.offers.append(create_offer(business_user, offer_data()))
            self.offers.append(create_offer(business_user, offer_data()))

        self.ratings = [5, 4, 5]
        for i in range(len(self.business_users)):
            create_review(
                review_data(
                    self.customer_user, self.business_users[i], rating=self.ratings[i]
                )
            )

        self.url = reverse("platform-base-info")

    def test_get_platform_base_info(self):
        """Test the GET request to retrieve platform base information."""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.customer_token.key)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, http_status.HTTP_200_OK)

    def test_get_platform_base_info_response_structure(self):
        """Test the structure of the response returned by the GET request to retrieve platform base information."""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.customer_token.key)
        response = self.client.get(self.url)

        expected_fields = {
            "review_count",
            "average_rating",
            "business_profile_count",
            "offer_count",
        }

        self.assertEqual(set(response.data.keys()), expected_fields)

    def test_get_platform_base_info_values(self):
        """Test the values returned by the GET request to retrieve platform base information."""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.customer_token.key)
        response = self.client.get(self.url)

        expected_review_count = len(self.business_users)
        expected_average_rating = round(sum(self.ratings) / len(self.ratings), 1)
        expected_business_profile_count = len(self.business_users)
        expected_offer_count = len(self.offers)

        self.assertEqual(response.data["review_count"], expected_review_count)
        self.assertEqual(response.data["average_rating"], expected_average_rating)
        self.assertEqual(
            response.data["business_profile_count"], expected_business_profile_count
        )
        self.assertEqual(response.data["offer_count"], expected_offer_count)
