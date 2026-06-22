from django.urls import path
from .views import ReviewApiView

urlpatterns = [
    path("reviews/", ReviewApiView.as_view(), name="reviews-list"),
]
