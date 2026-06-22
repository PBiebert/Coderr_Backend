from rest_framework.test import APITestCase
from tests_helpers.users import create_user
from tests_helpers.reviews import review_data, create_review
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework import status as http_status


class ReviewPatchDeleteAPITestCase(APITestCase):
    def setUp(self):
        self.custom_user = create_user()
        self.custom_token = Token.objects.create(user=self.custom_user)

        self.business_user = create_user(username="exampleBusiness", type="business")
        self.business_token = Token.objects.create(user=self.business_user)

        self.review = create_review(review_data(self.custom_user, self.business_user))

        self.url = reverse("reviews-detail", kwargs={"pk": self.review.id})

    def test_patch_review_return_200(self):
        """Test that a customer can update their review and receives a 200 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.custom_token.key)
        response = self.client.patch(
            self.url, {"rating": 4, "description": "Good work!"}, format="json"
        )
        self.assertEqual(response.status_code, http_status.HTTP_200_OK)

    def test_patch_review_with_invalid_fields_return_400(self):
        """Test that updating a review with invalid fields returns a 400 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.custom_token.key)
        response = self.client.patch(self.url, {"business_user": 3}, format="json")
        self.assertEqual(response.status_code, http_status.HTTP_400_BAD_REQUEST)

    def test_patch_reviewis_not_authenticated_returns_401(self):
        """Test that updating a review without authentication returns a 401 response"""

        response = self.client.patch(
            self.url, {"rating": 4, "description": "Good work!"}, format="json"
        )
        self.assertEqual(response.status_code, http_status.HTTP_401_UNAUTHORIZED)

    def test_patch_review_as_different_user_returns_403(self):
        """Test that a user cannot update another user's review and receives a 403 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.business_token.key)
        response = self.client.patch(
            self.url, {"rating": 4, "description": "Good work!"}, format="json"
        )
        self.assertEqual(response.status_code, http_status.HTTP_403_FORBIDDEN)

    def test_patch_review_with_invalid_id_returns_404(self):
        """Test that updating a review with an invalid ID returns a 404 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.custom_token.key)
        url = reverse("reviews-detail", kwargs={"pk": 99})
        response = self.client.patch(
            url, {"rating": 4, "description": "Good work!"}, format="json"
        )
        self.assertEqual(response.status_code, http_status.HTTP_404_NOT_FOUND)

    def test_delete_review_return_204(self):
        """Test that a customer can delete their review and receives a 204 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.custom_token.key)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, http_status.HTTP_204_NO_CONTENT)

    def test_delete_reviewis_not_authenticated_returns_401(self):
        """Test that deleting a review without authentication returns a 401 response"""

        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, http_status.HTTP_401_UNAUTHORIZED)

    def test_delete_review_as_different_user_returns_403(self):
        """Test that a user cannot delete another user's review and receives a 403 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.business_token.key)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, http_status.HTTP_403_FORBIDDEN)

    def test_delete_review_with_invalid_id_returns_404(self):
        """Test that deleting a review with an invalid ID returns a 404 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.custom_token.key)
        url = reverse("reviews-detail", kwargs={"pk": 99})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, http_status.HTTP_404_NOT_FOUND)
