from django.contrib import admin
from .models import Offer


class OfferAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "created_at", "updated_at")


admin.site.register(Offer, OfferAdmin)
