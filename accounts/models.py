from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    VISIBILITY_CHOICES = [
        ("public", "Public"),
        ("followers", "Followers Only"),
        ("private", "Private"),
    ]

    ROLE_CHOICES = [
        ("dom", "Dom"),
        ("sub", "Sub"),
        ("switch", "Switch"),
        ("curious", "Curious"),
        ("other", "Other"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Core identity
    display_name = models.CharField(max_length=50, unique=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True)

    # Visibility controls
    bio_visibility = models.CharField(
        max_length=20,
        choices=VISIBILITY_CHOICES,
        default="public",
    )

    location_visibility = models.CharField(
        max_length=20,
        choices=VISIBILITY_CHOICES,
        default="followers",
    )

    role_visibility = models.CharField(
        max_length=20,
        choices=VISIBILITY_CHOICES,
        default="public",
    )

    # Trust / verification
    is_verified = models.BooleanField(default=False)
    verification_level = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.display_name


class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        related_name="following",
        on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        User,
        related_name="followers",
        on_delete=models.CASCADE
    )

    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")

    def __str__(self):
        return f"{self.follower.username} → {self.following.username}"

