from django.urls import path
from .views import (
    ProfileDetailAPIView,
    BusinessPorfilesAPIView,
    CustomerPorfilesAPIView,
)

urlpatterns = [
    path("profile/<int:pk>/", ProfileDetailAPIView.as_view(), name="profile-details"),
    path(
        "profiles/customer/",
        CustomerPorfilesAPIView.as_view(),
        name="customer-profiles",
    ),
    path(
        "profiles/business/",
        BusinessPorfilesAPIView.as_view(),
        name="business-profiles",
    ),
]
