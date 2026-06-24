from django.db.models import Min
from rest_framework import generics
from offers.models import Offer, OfferDetail
from .serializers import (
    OfferCreateSerializer,
    OfferListSerializer,
    OfferDetailSerializer,
    OfferUpdateSerializer,
    OfferSingleDetailSerializer,
)
from .premissions import IsBusinessUser, IsOwner
from rest_framework.permissions import IsAuthenticated, AllowAny
from .pagination import StandardOfferResultsPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import OfferFilter


class OfferAPIView(generics.ListCreateAPIView):
    """API view for listing and creating offers."""

    queryset = Offer.objects.all()
    pagination_class = StandardOfferResultsPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ["updated_at", "min_price"]
    ordering = ["-updated_at"]
    filterset_class = OfferFilter
    search_fields = ["title", "description"]

    def get_queryset(self):
        """
        Return the queryset for the view, annotated with the minimum price of
        related OfferDetail objects.
        """

        return Offer.objects.all().annotate(min_price=Min("details__price"))

    def get_serializer_class(self):
        """Return the appropriate serializer class based on the request method."""

        if self.request.method == "POST":
            return OfferCreateSerializer
        return OfferListSerializer

    def get_permissions(self):
        """Return the appropriate permissions based on the request method."""

        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated(), IsBusinessUser()]


class OfferDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API view for retrieving, updating, and deleting offers."""

    serializer_class = OfferDetailSerializer
    http_method_names = ["get", "patch", "delete", "head", "options"]

    def get_queryset(self):
        """
        Return the queryset for the view, annotated with the minimum price of
        related OfferDetail objects.
        """

        return Offer.objects.all().annotate(min_price=Min("details__price"))

    def get_permissions(self):
        """Return the appropriate permissions based on the request method."""

        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsOwner()]

    def get_serializer_class(self):
        """Return the appropriate serializer class based on the request method."""

        if self.request.method in ["PATCH"]:
            return OfferUpdateSerializer
        return OfferDetailSerializer


class OfferSingleDetailAPIView(generics.RetrieveAPIView):
    """API view for retrieving a single OfferDetail object."""

    queryset = OfferDetail.objects.all()
    serializer_class = OfferSingleDetailSerializer
    permission_classes = [IsAuthenticated]
