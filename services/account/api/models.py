import uuid

from django.db import models


class Account(models.Model):
    user_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    supabase_user_id = models.UUIDField(unique=True)
    user_number = models.PositiveBigIntegerField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    display_name = models.CharField(max_length=80, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["username"]),
            models.Index(fields=["user_number"]),
        ]

    def __str__(self):
        return f"@{self.username}"
