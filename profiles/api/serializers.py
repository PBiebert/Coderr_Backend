from rest_framework import serializers
from profiles.models import Profile


class ProfileDetailSerializer(serializers.ModelSerializer):
    """Serializer for retrieving and updating a user's profile"""

    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")
    type = serializers.CharField(source="user.type", read_only=True)
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%dT%H:%M:%SZ")

    class Meta:
        model = Profile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
            "email",
            "created_at",
        ]

    def update(self, instance, validated_data):
        """Override the update method to handle nested user data"""

        user_data = validated_data.pop("user", {})
        user = instance.user

        user.first_name = user_data.get("first_name", user.first_name)
        user.last_name = user_data.get("last_name", user.last_name)
        user.email = user_data.get("email", user.email)

        user.save()

        return super().update(instance, validated_data)


class ProfileListSerializer(serializers.ModelSerializer):
    """Serializer for retrieving a list of profiles"""

    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    type = serializers.CharField(source="user.type", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
        ]
