from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    type = models.CharField(
        max_length=50, choices=[("customer", "Customer"), ("business", "Business")]
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return f"id:{self.id}, username:{self.username}, type:({self.type})"
