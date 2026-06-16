from django.contrib import admin
from .models import Offer, OfferDetail


class OfferAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "created_at", "updated_at")


class OfferDetailAdmin(admin.ModelAdmin):
    list_display = (
        "offer",
        "title",
        "revisions",
        "delivery_time_in_days",
        "price",
        "offer_type",
    )


admin.site.register(Offer, OfferAdmin)
admin.site.register(OfferDetail, OfferDetailAdmin)
