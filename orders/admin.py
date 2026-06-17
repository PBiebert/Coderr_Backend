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

    def __str__(self):
        return (
            f"Title: {self.title},Erstellt am: {self.created_at},Status: {self.status}"
        )


admin.site.register(Order, OrderAdmin)
