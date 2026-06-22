from django.contrib import admin

from .models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("business_user", "reviewer", "rating", "created_at")
    readonly_fields = ("created_at", "updated_at")


admin.site.register(Review, ReviewAdmin)
