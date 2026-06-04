from django.urls import path
from .views import ProfileDetailAPIView

urlpatterns = [
    path("profile/<int:pk>", ProfileDetailAPIView.as_view(), name="profile_details"),
]
