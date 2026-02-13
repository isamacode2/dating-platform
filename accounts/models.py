from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    GENDER_CHOICES = (
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    display_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    location = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)

    profile_image = models.URLField(blank=True)

    verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.display_name

