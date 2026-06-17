from django.urls import path
from .views import OfferAPIView, OfferDetailAPIView, OfferSingleDetailAPIView

# from .views import

urlpatterns = [
    path("offers/", OfferAPIView.as_view(), name="offer-list"),
    path("offers/<pk>/", OfferDetailAPIView.as_view(), name="offers-details"),
    path(
        "offerdetails/<pk>/",
        OfferSingleDetailAPIView.as_view(),
        name="offers_single_detail",
    ),
]
