from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from .serializers import RegisterSerializer
from rest_framework.authtoken.models import Token


class RegistrationAPIView(APIView):
    """View for user registration."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                "token": token.key,
                "username": saved_account.username,
                "email": saved_account.email,
                "user_id": saved_account.id,
            }
            return Response(data, status=201)

        return Response(serializer.errors, status=400)
