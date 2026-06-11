from django.shortcuts import render
from rest_framework import generics
from offers.models import Offer
from .serializers import OfferSerializer


class OfferAPIView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
