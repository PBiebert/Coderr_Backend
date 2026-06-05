from django.shortcuts import render
from rest_framework import generics
from profiles.models import Profile
from .serializers import ProfileDetailSerializer, ProfileListSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .premissions import IsOwner


class ProfileDetailAPIView(generics.RetrieveUpdateAPIView):
    """API view to retrieve and update a user's profile"""

    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer

    def get_permissions(self):
        if self.request.method == "PATCH":
            return [IsOwner()]
        return [IsAuthenticated()]


class BusinessPorfilesAPIView(generics.ListAPIView):
    """API view to retrieve a list of all business profiles"""

    queryset = Profile.objects.filter(user__type="business")
    serializer_class = ProfileListSerializer


class CustomerPorfilesAPIView(generics.ListAPIView):
    """API view to retrieve a list of all customer profiles"""

    queryset = Profile.objects.filter(user__type="customer")
    serializer_class = ProfileListSerializer
