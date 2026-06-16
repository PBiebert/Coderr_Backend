from django.shortcuts import render
from rest_framework import generics
from offers.models import Offer
from .serializers import OfferCreateSerializer, OfferListSerializer
from .premissions import IsBusinessUser
from rest_framework.permissions import IsAuthenticated, AllowAny
from .pagination import StandardOfferResultsPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import OfferFilter


class OfferAPIView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    pagination_class = StandardOfferResultsPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ["updated_at", "min_price"]
    ordering = ["-updated_at"]
    filterset_class = OfferFilter
    search_fields = ["title", "description"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OfferCreateSerializer
        return OfferListSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), IsBusinessUser()]
