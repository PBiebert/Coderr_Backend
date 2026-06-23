from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "repeated_password", "type"]

    def validate(self, data):
        """Validate that the password and repeated password match."""

        if data["password"] != data["repeated_password"]:
            raise serializers.ValidationError("Password does not match.")
        return data

    def create(self, validated_data):
        """Create a new user instance after removing the repeated password."""

        validated_data.pop("repeated_password")
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.ModelSerializer):
    """Serializer for user login."""

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password"]

    def validate(self, data):
        """Validate that the user exists and the password is correct."""

        try:
            user = User.objects.get(username=data["username"])
        except User.DoesNotExist:
            raise serializers.ValidationError("User doesn't exist")

        if user.check_password(data["password"]):
            return data
        else:
            raise serializers.ValidationError("password isn't right")
