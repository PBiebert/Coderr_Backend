from rest_framework import generics, viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from .permissions import IsCustomUser, IsBusinessUser
from orders.models import Order
from .serializers import (
    OfferCreateSerializer,
    OrderListSerializer,
    OrderDetailUpdateSerializer,
)
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


class OrderDetailPatchDeleteViewSet(
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):

    queryset = Order.objects.all()
    serializer_class = OrderDetailUpdateSerializer
    permission_classes = [IsAuthenticated, IsBusinessUser]
