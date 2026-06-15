from rest_framework import serializers
from offers.models import Offer, OfferDetail
from django.contrib.auth import get_user_model

User = get_user_model()


class OfferCreateDetailSerializer(serializers.ModelSerializer):
    """Serializer for the OfferDetail model."""

    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, coerce_to_string=False
    )

    class Meta:
        model = OfferDetail
        fields = [
            "id",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        ]


class OfferCreateSerializer(serializers.ModelSerializer):
    """Serializer for the Offer model, including nested details."""

    details = OfferCreateDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = [
            "id",
            "title",
            "image",
            "description",
            "details",
        ]

    def validate_details(self, value):
        """Validate that there are no duplicate offer types and that there are exactly 3 details."""

        types = []
        for detail in value:
            if detail["offer_type"] in types:
                raise serializers.ValidationError(
                    "Duplicate offer types are not allowed."
                )
            types.append(detail["offer_type"])

        if len(types) != 3:
            raise serializers.ValidationError("Exactly 3 details are required.")
        return value

    def create(self, validated_data):
        """Create an offer and its related details."""

        details_data = validated_data.pop("details")

        user = self.context["request"].user
        offer = Offer.objects.create(user=user, **validated_data)

        for detail in details_data:
            OfferDetail.objects.create(offer=offer, **detail)

        return offer


class OfferDetailsListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ["id", "url"]

    def get_url(self, obj):
        return f"/offerdetails/{obj.id}/"


class userDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username"]


class OfferListSerializer(serializers.ModelSerializer):
    """Serializer for listing offers without nested details."""

    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%dT%H:%M:%SZ")
    updated_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%dT%H:%M:%SZ")
    details = OfferDetailsListSerializer(many=True, read_only=True)
    user_details = userDetailsSerializer(source="user", read_only=True)
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            "id",
            "user",
            "title",
            "image",
            "description",
            "created_at",
            "updated_at",
            "details",
            "min_price",
            "min_delivery_time",
            "user_details",
        ]

    def get_min_price(self, obj):
        """Calculate the minimum price from the related details."""

        return min(detail.price for detail in obj.details.all())

    def get_min_delivery_time(self, obj):
        return min(detail.delivery_time_in_days for detail in obj.details.all())
