from rest_framework import serializers
from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%dT%H:%M:%SZ")
    updated_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%dT%H:%M:%SZ")
    rating = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Review
        fields = "__all__"

    def create(self, validated_data):
        review = Review.objects.create(
            reviewer=self.context["request"].user, **validated_data
        )
        return review
