from django.urls import path
from .views import (
    ProfileDetailAPIView,
    BusinessPorfilesAPIView,
    CustomerPorfilesAPIView,
)

urlpatterns = [
    path("profile/<int:pk>/", ProfileDetailAPIView.as_view(), name="profile_details"),
    path("customer/", CustomerPorfilesAPIView.as_view(), name="customer_profiles"),
    path("business/", BusinessPorfilesAPIView.as_view(), name="business_profiles"),
]
