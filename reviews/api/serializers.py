from rest_framework import serializers
from reviews.models import Review


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Serializer for the Review model, handling validation and serialization of review data."""

    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%dT%H:%M:%SZ")
    updated_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%dT%H:%M:%SZ")
    rating = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Review
        fields = "__all__"

    def validate(self, data):
        """Validation to ensure that a user can only submit one review per business."""

        request = self.context.get("request")
        existing_review = Review.objects.filter(
            reviewer=request.user, business_user=data["business_user"]
        ).exists()

        if existing_review:
            raise serializers.ValidationError(
                "You have already submitted a review for this business."
            )
        return data

    def create(self, validated_data):
        """Create a new review instance with the validated data and the current user as the reviewer."""

        review = Review.objects.create(
            reviewer=self.context["request"].user, **validated_data
        )
        return review


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for the Review model, handling validation and serialization of review data."""

    class Meta:
        model = Review
        fields = "__all__"


class ReviewDetailSerializer(serializers.ModelSerializer):
    """Serializer for the Review model, handling validation and serialization of review data for update and delete operations."""

    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    updated_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%SZ")
    rating = serializers.IntegerField(min_value=1, max_value=5)
    description = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ["reviewer", "business_user", "created_at", "updated_at"]

    def validate(self, attrs):
        """Validation to ensure that only the 'rating' and 'description' fields can be updated."""

        ALLOWED_FIELDS = {"rating", "description"}
        extra_fields = set(self.initial_data) - ALLOWED_FIELDS

        if extra_fields:
            raise serializers.ValidationError(
                "Only 'rating' and 'description' fields can be updated."
            )
        return attrs
