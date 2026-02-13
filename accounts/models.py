from django.db import models
from django.contrib.auth.models import User


class Like(models.Model):
    from_user = models.ForeignKey(
        User,
        related_name="likes_sent",
        on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        User,
        related_name="likes_received",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("from_user", "to_user")

    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username}"

