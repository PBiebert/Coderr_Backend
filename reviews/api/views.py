from rest_framework import generics
from reviews.models import Review
from .serializers import ReviewSerializer


class ReviewApiView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
