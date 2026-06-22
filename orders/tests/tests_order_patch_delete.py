from rest_framework.test import APITestCase
from tests_helpers.users import create_user
from tests_helpers.offers import offer_data, create_offer
from tests_helpers.orders import order_data, create_order
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework import status


class OrderPatchDeleteAPIViewTestCase(APITestCase):
    def setUp(self):
        """Set up test data and authentication tokens for the tests"""

        self.custom_user = create_user()
        self.custom_token = Token.objects.create(user=self.custom_user)

        self.business_user = create_user(username="exampleBusiness", type="business")
        self.business_token = Token.objects.create(user=self.business_user)

        self.offer = create_offer(self.business_user, offer_data())
        self.order = create_order(order_data(self.custom_user, self.business_user))
        self.url = reverse("orders-detail", kwargs={"pk": self.order.id})

    def test_patch_order_as_business_user_returns_200(self):
        """Test that a business user can update an order and receives a 200 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.business_token.key)
        data = {"status": "completed"}
        response = self.client.patch(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_order_invalid_field_returns_400(self):
        """Test that updating an order with an invalid field returns a 400 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.business_token.key)
        data = {"delivery_time_in_days": 7}
        response = self.client.patch(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_order_with_empty_data_returns_400(self):
        """Test that updating an order with empty data returns a 400 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.business_token.key)
        data = {}
        response = self.client.patch(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_order_with_invalid_status_value_returns_400(self):
        """Test that updating an order with an invalid status value returns a 400 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.business_token.key)
        data = {"status": "invalid_status"}
        response = self.client.patch(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_order_is_not_authenticated_returns_401(self):
        """Test that an unauthenticated user cannot update an order and receives a 401 response"""

        data = {"status": "completed"}
        response = self.client.patch(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_order_as_customer_returns_403(self):
        """Test that a customer cannot update an order and receives a 403 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.custom_token.key)
        data = {"status": "completed"}
        response = self.client.patch(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_order_not_found_returns_404(self):
        """Test that updating a non-existent order returns a 404 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.business_token.key)
        data = {"status": "completed"}
        url = reverse("orders-detail", kwargs={"pk": 99})
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_order_as_business_user_returns_204(self):
        """Test that a business user can delete an order and receives a 204 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.business_token.key)
        response = self.client.delete(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_order_is_not_authenticated_returns_401(self):
        """Test that an unauthenticated user cannot delete an order and receives a 401 response"""

        response = self.client.delete(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_order_as_customer_returns_403(self):
        """Test that a customer cannot delete an order and receives a 403 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.custom_token.key)
        response = self.client.delete(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_order_not_found_returns_404(self):
        """Test that deleting a non-existent order returns a 404 response"""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.business_token.key)
        url = reverse("orders-detail", kwargs={"pk": 99})
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
