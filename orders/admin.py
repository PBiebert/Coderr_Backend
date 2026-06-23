from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "created_at",
        "business_user",
        "customer_user",
        "status",
    )

    readonly_fields = ("created_at", "updated_at")


admin.site.register(Order, OrderAdmin)
