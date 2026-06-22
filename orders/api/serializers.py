from rest_framework import serializers
from orders.models import Order
from offers.models import OfferDetail
from rest_framework.exceptions import NotFound


class OfferCreateSerializer(serializers.Serializer):
    """Serializer for creating an order based on an offer detail. It includes a write-only field
    for the offer_detail_id and read-only fields for the order details."""

    offer_detail_id = serializers.IntegerField(write_only=True)

    id = serializers.IntegerField(read_only=True)
    business_user = serializers.PrimaryKeyRelatedField(read_only=True)
    customer_user = serializers.PrimaryKeyRelatedField(read_only=True)
    title = serializers.CharField(read_only=True)
    revisions = serializers.IntegerField(read_only=True)
    delivery_time_in_days = serializers.IntegerField(read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    features = serializers.JSONField(read_only=True)
    offer_type = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%dT%H:%M:%SZ")
    updated_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%dT%H:%M:%SZ")

    def create(self, validated_data):
        """Serializer for creating an order based on an offer detail.
        It creates a snapshot of the offer details using the offer_detail_id."""

        offer_detail_id = validated_data.get("offer_detail_id")

        try:
            offer = OfferDetail.objects.get(id=offer_detail_id)
        except OfferDetail.DoesNotExist:
            raise NotFound("OfferDetail with the given ID does not exist.")

        order = Order.objects.create(
            business_user=offer.offer.user,
            customer_user=self.context["request"].user,
            title=offer.title,
            revisions=offer.revisions,
            delivery_time_in_days=offer.delivery_time_in_days,
            price=offer.price,
            features=offer.features,
            offer_type=offer.offer_type,
            status="in_progress",
        )
        return order


class OrderListSerializer(serializers.ModelSerializer):
    """Serializer for listing orders. It includes all fields of the Order model."""

    class Meta:
        model = Order
        fields = "__all__"


class OrderDetailUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating order details. It includes all fields of the Order model, but only allows updates to specific fields."""

    class Meta:
        model = Order
        fields = ["status"]

    def validate(self, attrs):
        """Ensure that only the 'status' field can be updated."""

        ALLOWED_FIELDS = {"status"}
        extra_fields = set(self.initial_data) - ALLOWED_FIELDS

        if extra_fields:
            raise serializers.ValidationError("Only the 'status' field can be updated.")
        return attrs
