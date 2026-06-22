from django.urls import path
from .views import ReviewApiView, ReviewDetailApiView

urlpatterns = [
    path("reviews/", ReviewApiView.as_view(), name="reviews-list"),
    path("reviews/<int:pk>/", ReviewDetailApiView.as_view(), name="reviews-detail"),
]
