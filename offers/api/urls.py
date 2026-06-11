from django.urls import path
from .views import OfferAPIView

# from .views import

urlpatterns = [
    path("offers/", OfferAPIView.as_view(), name="offers"),
]
