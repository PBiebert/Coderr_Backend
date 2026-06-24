from rest_framework.test import APITestCase
from tests_helpers.users import create_user
from tests_helpers.reviews import review_data, create_review
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework import status as http_status


class ReviewListCreateAPITestCase(APITestCase):
    """Test case for the ReviewListCreateAPIView API endpoint."""

    def setUp(self):
        """
        Set up the test case with a customer user, business user, and
        authentication tokens.
        """

        self.custom_user = create_user()
        self.custom_token = Token.objects.create(user=self.custom_user)

        self.business_user = create_user(username="exampleBusiness", type="business")
        self.business_token = Token.objects.create(user=self.business_user)

        self.url = reverse("reviews-list")

    def test_create_review_return_201(self):
        """Test that a customer can create a review and receives a 201 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.custom_token.key)
        response = self.client.post(
            self.url,
            review_data(self.custom_user.id, self.business_user.id),
            format="json",
        )
        self.assertEqual(response.status_code, http_status.HTTP_201_CREATED)

    def test_create_review_valid_response_structure(self):
        """
        Test that the response data structure when creating a review contains
        the expected fields
        """

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.custom_token.key)
        response = self.client.post(
            self.url,
            review_data(self.custom_user.id, self.business_user.id),
            format="json",
        )

        expected_fields = {
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at",
        }

        self.assertEqual(set(response.data.keys()), expected_fields)

    def test_create_review_with_invalid_rating_returns_400(self):
        """Test that creating a review with an invalid rating value returns a 400 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.custom_token.key)
        response = self.client.post(
            self.url,
            review_data(self.custom_user.id, self.business_user.id, rating=6),
            format="json",
        )
        self.assertEqual(response.status_code, http_status.HTTP_400_BAD_REQUEST)

    def test_create_review_user_has_already_reviewed_returns_400(self):
        """
        Test that creating a review for the same business user by the same
        customer returns a 400 response
        """

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.custom_token.key)
        review_data_instance = review_data(self.custom_user.id, self.business_user.id)

        self.client.post(self.url, review_data_instance, format="json")

        response = self.client.post(self.url, review_data_instance, format="json")
        self.assertEqual(response.status_code, http_status.HTTP_400_BAD_REQUEST)

    def test_create_review__is_not_authenticated_returns_401(self):
        """Test that creating a review without authentication returns a 401 response"""

        response = self.client.post(
            self.url,
            review_data(self.custom_user.id, self.business_user.id),
            format="json",
        )
        self.assertEqual(response.status_code, http_status.HTTP_401_UNAUTHORIZED)

    def test_create_review_as_business_user_returns_403(self):
        """Test that a business user cannot create a review and receives a 403 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.business_token.key)
        response = self.client.post(
            self.url,
            review_data(self.custom_user.id, self.business_user.id),
            format="json",
        )
        self.assertEqual(response.status_code, http_status.HTTP_403_FORBIDDEN)


class ReviewListAPITestCase(APITestCase):
    def setUp(self):
        self.custom_user = create_user()
        self.custom_token = Token.objects.create(user=self.custom_user)
        self.custom_user_2 = create_user(username="exampleCustomer2")

        self.business_user = create_user(username="exampleBusiness", type="business")
        self.business_user_2 = create_user(username="exampleBusiness2", type="business")

        self.url = reverse("reviews-list")

        create_review(review_data(self.custom_user, self.business_user))
        create_review(review_data(self.custom_user, self.business_user_2))
        create_review(review_data(self.custom_user_2, self.business_user))

    def test_get_reviews_returns_200(self):
        """Test that a GET request to the reviews endpoint returns a 200 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.custom_token.key)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, http_status.HTTP_200_OK)

    def test_get_reviews_as_unauthenticated_user_returns_401(self):
        """
        Test that a GET request to the reviews endpoint without authentication
        returns a 401 response
        """

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, http_status.HTTP_401_UNAUTHORIZED)

    def test_get_reviews_with_business_user_filter_returns_200(self):
        """
        Test that filtering reviews by business user returns a 200 response
        and the correct number of reviews
        """

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.custom_token.key)
        filter_url = f"{self.url}?business_user_id={self.business_user.id}"
        response = self.client.get(filter_url)

        self.assertEqual(response.status_code, http_status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_reviews_with_reviewer_filter_returns_200(self):
        """
        Test that filtering reviews by reviewer returns a 200 response and
        the correct number of reviews
        """

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.custom_token.key)
        filter_url = f"{self.url}?reviewer_id={self.custom_user.id}"
        response = self.client.get(filter_url)

        self.assertEqual(response.status_code, http_status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_reviews_with_ordering_to_updated_at_returns_200(self):
        """
        Test that ordering reviews by updated_at returns a 200 response and
        the correct number of reviews
        """

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.custom_token.key)
        filter_url = f"{self.url}?ordering=updated_at"
        response = self.client.get(filter_url)

        self.assertEqual(response.status_code, http_status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_reviews_with_ordering_to_rating_returns_200(self):
        """
        Test that ordering reviews by rating returns a 200 response and the
        correct number of reviews
        """

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.custom_token.key)
        filter_url = f"{self.url}?ordering=rating"
        response = self.client.get(filter_url)

        self.assertEqual(response.status_code, http_status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
