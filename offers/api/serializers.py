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
        """
        Validate that there are no duplicate offer types and that there are
        exactly 3 details.
        """

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


class OfferDetailRefUrlSerializer(serializers.ModelSerializer):
    """Serializer for the OfferDetail model that returns a reference URL."""

    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ["id", "url"]

    def get_url(self, obj):
        """Return the reference URL for the OfferDetail object."""

        return f"/offerdetails/{obj.id}/"


class OfferDetailAbsUrlSerializer(serializers.ModelSerializer):
    """Serializer for the OfferDetail model that returns an absolute URL."""

    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetail
        fields = ["id", "url"]

    def get_url(self, obj):
        """Return the absolute URL for the OfferDetail object."""

        request = self.context.get("request")
        return request.build_absolute_uri(f"/api/offerdetails/{obj.id}/")


class UserDetailsSerializer(serializers.ModelSerializer):
    """Serializer for the User model to return user details."""

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username"]


class BaseOfferSerializer(serializers.ModelSerializer):
    """Base serializer for the Offer model, including common fields."""

    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%dT%H:%M:%SZ")
    updated_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%dT%H:%M:%SZ")
    details = OfferDetailRefUrlSerializer(many=True, read_only=True)
    min_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, coerce_to_string=False
    )
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
        ]

    def get_min_delivery_time(self, obj):
        """Return the minimum delivery time in days from the related OfferDetail objects."""

        return min(
            (detail.delivery_time_in_days for detail in obj.details.all()), default=None
        )


class OfferListSerializer(BaseOfferSerializer):
    """Serializer for listing offers, including user details."""

    user_details = UserDetailsSerializer(source="user", read_only=True)

    class Meta(BaseOfferSerializer.Meta):
        fields = BaseOfferSerializer.Meta.fields + ["user_details"]


class OfferDetailSerializer(BaseOfferSerializer):
    """
    Serializer for retrieving offer details, including absolute URLs for
    related details.
    """

    details = OfferDetailAbsUrlSerializer(many=True, read_only=True)


class OfferUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating an offer and its related details."""

    details = OfferCreateDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ["id", "title", "image", "description", "details"]

    def validate_details(self, value):
        """Validate that each detail includes offer_type for updates."""

        for detail in value:
            if not detail.get("offer_type"):
                raise serializers.ValidationError(
                    "Each detail must include offer_type."
                )
        return value

    def update(self, instance, validated_data):
        """Update an offer and its related details."""

        details_data = validated_data.pop("details")

        instance.title = validated_data.get("title", instance.title)
        instance.image = validated_data.get("image", instance.image)
        instance.description = validated_data.get("description", instance.description)
        instance.save()

        for detail in details_data:
            offer_type = detail.get("offer_type")
            if offer_type:
                offer_detail = OfferDetail.objects.get(
                    offer_type=offer_type, offer=instance
                )
                offer_detail.title = detail.get("title", offer_detail.title)
                offer_detail.revisions = detail.get("revisions", offer_detail.revisions)
                offer_detail.delivery_time_in_days = detail.get(
                    "delivery_time_in_days", offer_detail.delivery_time_in_days
                )
                offer_detail.price = detail.get("price", offer_detail.price)
                offer_detail.features = detail.get("features", offer_detail.features)
                offer_detail.offer_type = detail.get(
                    "offer_type", offer_detail.offer_type
                )
                offer_detail.save()

        return instance


class OfferSingleDetailSerializer(serializers.ModelSerializer):
    """Serializer for the OfferDetail model, including all fields."""

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
