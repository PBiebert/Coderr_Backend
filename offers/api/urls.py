from django.urls import path
from .views import OfferAPIView, OfferDetailAPIView

# from .views import

urlpatterns = [
    path("offers/", OfferAPIView.as_view(), name="offer-list"),
    path("offers/<pk>", OfferDetailAPIView.as_view(), name="offers_details"),
]
