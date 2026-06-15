from django.shortcuts import render
from rest_framework import generics
from offers.models import Offer
from .serializers import OfferCreateSerializer, OfferListSerializer
from .premissions import IsBusinessUser
from rest_framework.permissions import IsAuthenticated, AllowAny
from .pagination import StandardOfferResultsPagination


class OfferAPIView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    pagination_class = StandardOfferResultsPagination

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OfferCreateSerializer
        return OfferListSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), IsBusinessUser()]
