from django.shortcuts import render
from rest_framework import generics
from profiles.models import Profile
from .serializers import ProfileDetailSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated


class ProfileDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer
    permission_classes = [IsAuthenticated]
