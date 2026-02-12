from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [
        ('dom', 'Dom'),
        ('sub', 'Sub'),
        ('switch', 'Switch'),
        ('curious', 'Curious'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=50, unique=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True)

    is_verified = models.BooleanField(default=False)
    verification_level = models.IntegerField(default=0)  # 0 = none, 1 = email, 2 = ID, 3 = full

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.display_name

