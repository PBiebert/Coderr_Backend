from django.contrib import admin
from .models import Offer, OfferDetail


class OfferAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "created_at", "updated_at")


class OfferDetailAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "revisions",
        "delivery_time_in_days",
        "price",
        "offer_type",
    )


admin.site.register(Offer, OfferAdmin)
admin.site.register(OfferDetail, OfferDetailAdmin)
