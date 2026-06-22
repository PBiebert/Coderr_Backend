from rest_framework import generics, mixins
from reviews.models import Review
from .serializers import (
    ReviewSerializer,
    ReviewCreateSerializer,
    ReviewDetailSerializer,
)
from .permissions import IsCustomUser, IsReviewer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class ReviewApiView(generics.ListCreateAPIView):
    """API view for listing and creating reviews, with appropriate permissions and serializers based on the request method."""

    queryset = Review.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["business_user_id", "reviewer_id"]
    ordering_fields = ["updated_at", "rating"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ReviewCreateSerializer
        return ReviewSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsCustomUser()]
        return [IsAuthenticated()]


class ReviewDetailApiView(
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView
):

    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializer
    permission_classes = [IsAuthenticated, IsReviewer]

    def patch(self, request, *args, **kwargs):
        """Handle PATCH requests to update a review instance, ensuring that only the reviewer can update their review."""

        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Handle DELETE requests to delete a review instance, ensuring that only the reviewer can delete their review."""

        return self.destroy(request, *args, **kwargs)
