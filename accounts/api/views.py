from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from profiles.models import Profile

User = get_user_model()


class RegistrationAPIView(APIView):
    """View for user registration."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Handle user registration and return authentication token."""

        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            saved_account = serializer.save()
            Profile.objects.create(user=saved_account)
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                "token": token.key,
                "username": saved_account.username,
                "email": saved_account.email,
                "user_id": saved_account.id,
            }
            return Response(data, status=201)

        return Response(serializer.errors, status=400)


class LoginAPIView(APIView):
    """View for user login."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Handle user login and return authentication token."""

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(username=serializer.validated_data["username"])
            token, created = Token.objects.get_or_create(user=user)
            data = {
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.id,
            }
            return Response(data, status=200)
        return Response(serializer.errors, status=400)
