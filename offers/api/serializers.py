from rest_framework import serializers
from offers.models import Offer, OfferDetail


class OfferDetailSerializer(serializers.ModelSerializer):
    """Serializer for the OfferDetail model."""

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


class OfferSerializer(serializers.ModelSerializer):
    """Serializer for the Offer model, including nested details."""

    details = OfferDetailSerializer(many=True)

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
