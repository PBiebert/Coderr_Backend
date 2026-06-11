from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    file = models.ImageField(upload_to="uploads", blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, default="")
    tel = models.CharField(max_length=20, blank=True, default="")
    description = models.TextField(blank=True, default="")
    working_hours = models.CharField(max_length=50, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"id:{self.id}, Profile of {self.user.username}"
