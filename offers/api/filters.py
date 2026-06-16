import django_filters
from offers.models import Offer


class OfferFilter(django_filters.FilterSet):
    creator_id = django_filters.NumberFilter(field_name="user__id", lookup_expr="exact")
    min_price = django_filters.NumberFilter(
        field_name="details__price", lookup_expr="gte", distinct=True
    )
    max_delivery_time = django_filters.NumberFilter(
        field_name="details__delivery_time_in_days", lookup_expr="lte", distinct=True
    )

    class Meta:
        model = Offer
        fields = []
