from rest_framework.test import APITestCase
from tests_helpers.users import create_user
from tests_helpers.offers import offer_data, create_offer
from tests_helpers.orders import order_data, create_order
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework import status


class OrderListCreateAPIViewTestCase(APITestCase):
    def setUp(self):
        """Set up test data and authentication tokens for the tests"""

        self.custom_user = create_user()
        self.custom_token = Token.objects.create(user=self.custom_user)

        self.business_user = create_user(username="exampleBusiness", type="business")
        self.business_token = Token.objects.create(user=self.business_user)

        self.offer = create_offer(self.business_user, offer_data())
        self.url = reverse("order-list")

    def test_create_order_as_customer_returns_201(self):
        """Test that a customer can create an order and receives a 201 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.custom_token.key)
        data = {"offer_detail_id": 1}

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_order_valid_response_structure(self):
        """Test that the response data structure when creating an order contains the expected fields"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.custom_token.key)
        data = {"offer_detail_id": 1}

        response = self.client.post(self.url, data, format="json")

        expected_fields = {
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
        }

        self.assertEqual(set(response.data.keys()), expected_fields)

    def test_create_order_without_offer_detail_id_returns_400(self):
        """Test that creating an order without providing an offer_detail_id returns a 400 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.custom_token.key)
        data = {}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_is_not_authenticated_returns_401(self):
        """Test that an unauthenticated user cannot create an order and receives a 401 response"""

        data = {"offer_detail_id": 1}

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_order_as_business_user_returns_403(self):
        """Test that a business user cannot create an order and receives a 403 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.business_token.key)
        data = {"offer_detail_id": 1}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_order_with_invalid_offer_detail_id_returns_404(self):
        """Test that creating an order with a non-existent offer_detail_id returns a 404 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.custom_token.key)
        data = {"offer_detail_id": 999}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_orders_as_customer_returns_200(self):
        """Test that a customer can retrieve their orders and receives a 200 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.custom_token.key)
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_orders_as_customer_returns_only_own_orders(self):
        """Test that a customer retrieves only their own orders and not orders of other customers"""

        for order in range(3):
            create_order(order_data(self.custom_user, self.business_user))

        other_customer = create_user(username="othercustomer", type="customer")
        for order in range(2):
            create_order(order_data(other_customer, self.business_user))

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.custom_token.key)
        response = self.client.get(self.url, format="json")

        self.assertEqual(len(response.data), 3)
        for order in response.data:
            self.assertEqual(order["customer_user"], self.custom_user.id)

    def test_get_orders_as_business_user_returns_only_associated_orders(self):
        """Test that a business user retrieves only orders associated with them and not orders of other businesses"""

        for order in range(3):
            create_order(order_data(self.custom_user, self.business_user))

        other_business = create_user(username="otherbusiness", type="business")
        for order in range(2):
            create_order(order_data(self.custom_user, other_business))

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.business_token.key)
        response = self.client.get(self.url, format="json")

        self.assertEqual(len(response.data), 3)
        for order in response.data:
            self.assertEqual(order["business_user"], self.business_user.id)

    def test_get_orders_is_not_authenticated_returns_401(self):
        """Test that an unauthenticated user cannot retrieve orders and receives a 401 response"""

        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
