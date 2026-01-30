from django.db import models
from django.conf import settings


class Profile(models.Model):
    """
    Extended user profile to support ecoSwap-specific data.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    display_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(
        max_length=255,
        blank=True,
        help_text="City or neighborhood to help match local swaps.",
    )
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    total_items_shared = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.display_name or self.user.get_username()

