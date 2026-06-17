from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

OFFER_TYPE_CHOICES = [
    ("basic", "Basic"),
    ("standard", "Standard"),
    ("premium", "Premium"),
]

STATUS_CHOICES = [
    ("in_progress", "In Progress"),
    ("completed", "Completed"),
    ("cancelled", "Cancelled"),
]


class Order(models.Model):
    business_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="business_orders"
    )
    customer_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="customer_orders"
    )
    title = models.CharField(max_length=255)
    revisions = models.PositiveSmallIntegerField(default=0)
    delivery_time_in_days = models.PositiveSmallIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField()
    offer_type = models.CharField(max_length=50, choices=OFFER_TYPE_CHOICES)
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default="in_progress"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
