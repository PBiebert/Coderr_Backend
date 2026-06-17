from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .permissions import IsCustomUser
from orders.models import Order
from .serializers import OfferCreateSerializer, OrderListSerializer


class OrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated, IsCustomUser]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OfferCreateSerializer
        return OrderListSerializer
