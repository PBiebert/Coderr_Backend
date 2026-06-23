from rest_framework.test import APITestCase
from tests_helpers.users import create_user
from tests_helpers.orders import order_data, create_order
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework import status


class OrderCountAPIViewTestCase(APITestCase):
    def setUp(self):

        self.custom_user = create_user()
        self.custom_token = Token.objects.create(user=self.custom_user)

        self.business_user_1 = create_user(
            username="exampleBusiness_1", type="business"
        )
        self.business_token_1 = Token.objects.create(user=self.business_user_1)

        self.business_user_2 = create_user(
            username="exampleBusiness_2", type="business"
        )
        self.business_token_2 = Token.objects.create(user=self.business_user_2)

        for order in range(3):
            create_order(order_data(self.custom_user, self.business_user_1))
            create_order(order_data(self.custom_user, self.business_user_2))

        self.url = reverse("order-count", kwargs={"pk": self.business_user_1.id})

    def test_get_order_count_returns_200(self):
        """Test that the order count endpoint returns a 200 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.custom_token.key)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_order_count_returns_correct_count(self):
        """Test that the order count endpoint returns the correct count of in-progress orders for a business user"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.custom_token.key)
        response = self.client.get(self.url)
        expected_count = 3
        self.assertEqual(response.data["order_count"], expected_count)

    def test_get_order_count_user_is_not_authenticated_returns_401(self):
        """Test that the order count endpoint returns a 401 response when the user is not authenticated"""

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_order_count_business_user_not_found_returns_404(self):
        """Test that the order count endpoint returns a 404 response when the specified business user is not found"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.custom_token.key)
        url = reverse("order-count", kwargs={"pk": 99})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class OrderCountAPIViewTestCase(APITestCase):
    def setUp(self):

        self.custom_user = create_user()
        self.custom_token = Token.objects.create(user=self.custom_user)

        self.business_user = create_user(username="exampleBusiness", type="business")
        self.business_token = Token.objects.create(user=self.business_user)

        for order in range(3):
            create_order(
                order_data(
                    self.custom_user,
                    self.business_user,
                    status="completed",
                )
            )
            create_order(order_data(self.custom_user, self.business_user))

        self.url = reverse(
            "completed-order-count", kwargs={"pk": self.business_user.id}
        )

    def test_get_completed_order_count_returns_200(self):
        """Test that the completed order count endpoint returns a 200 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.custom_token.key)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_completed_order_count_returns_correct_count(self):
        """Test that the completed order count endpoint returns the correct count of completed orders for a business user"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.custom_token.key)
        response = self.client.get(self.url)
        expected_count = 3
        self.assertEqual(response.data["completed"], expected_count)

    def test_get_completed_order_count_user_is_not_authenticated_returns_401(self):
        """Test that the completed order count endpoint returns a 401 response when the user is not authenticated"""

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_completed_order_count_business_user_not_found_returns_404(self):
        """Test that the completed order count endpoint returns a 404 response when the specified business user is not found"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.custom_token.key)
        url = reverse("completed-order-count", kwargs={"pk": 99})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
