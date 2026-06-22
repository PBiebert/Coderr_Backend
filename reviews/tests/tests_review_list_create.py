from rest_framework.test import APITestCase
from tests_helpers.users import create_user
from tests_helpers.reviews import review_data
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework import status as http_status


class ReviewListCreateAPITestCase(APITestCase):
    def setUp(self):
        self.custom_user = create_user()
        self.custom_token = Token.objects.create(user=self.custom_user)

        self.business_user = create_user(username="exampleBusiness", type="business")
        self.business_token = Token.objects.create(user=self.business_user)

        self.url = reverse("reviews-list")

    def test_create_review_return_201(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.custom_token.key)
        response = self.client.post(
            self.url,
            review_data(self.custom_user.id, self.business_user.id),
            format="json",
        )
        self.assertEqual(response.status_code, http_status.HTTP_201_CREATED)
