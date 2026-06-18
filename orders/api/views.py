from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .permissions import IsCustomUser
from orders.models import Order
from .serializers import OfferCreateSerializer, OrderListSerializer
from django.db.models import Q


class OrderListCreateAPIView(generics.ListCreateAPIView):
    """API view to list and create orders. Customers can create orders,
    while both customers and businesses can view their associated orders."""

    def get_queryset(self):
        """Return orders associated with the authenticated user, either as a customer or business."""

        user = self.request.user
        return Order.objects.filter(Q(customer_user=user) | Q(business_user=user))

    def get_serializer_class(self):
        """Return the appropriate serializer class based on the request method."""

        if self.request.method == "POST":
            return OfferCreateSerializer
        return OrderListSerializer

    def get_permissions(self):
        """Return the appropriate permissions based on the request method."""

        if self.request.method == "POST":
            return [IsAuthenticated(), IsCustomUser()]
        return [IsAuthenticated()]
