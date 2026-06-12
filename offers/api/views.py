from django.shortcuts import render
from rest_framework import generics
from offers.models import Offer
from .serializers import OfferSerializer
from .premissions import IsBusinessUser
from rest_framework.permissions import IsAuthenticated


class OfferAPIView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated, IsBusinessUser]
