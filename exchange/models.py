from django.db import models
from django.conf import settings


class Category(models.Model):
    """
    High-level grouping for exchangeable items, e.g. Electronics, Clothing, Furniture.
    """

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.name


class Item(models.Model):
    """
    An item that a user is willing to swap, donate or give away.
    """

    CONDITION_CHOICES = [
        ("new", "Like New"),
        ("good", "Good"),
        ("fair", "Fair"),
        ("poor", "Well-loved"),
    ]

    EXCHANGE_TYPE_CHOICES = [
        ("swap", "Swap"),
        ("donate", "Donate"),
        ("reuse", "Reuse / Borrow"),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="items"
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="items"
    )
    condition = models.CharField(
        max_length=20, choices=CONDITION_CHOICES, default="good"
    )
    exchange_type = models.CharField(
        max_length=20, choices=EXCHANGE_TYPE_CHOICES, default="swap"
    )
    location = models.CharField(
        max_length=255,
        help_text="Neighborhood or city to help people find nearby items.",
    )
    image = models.ImageField(upload_to="items/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.title


class SwapRequest(models.Model):
    """
    A request from one user to the item owner to swap or receive an item.
    """

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("declined", "Declined"),
        ("completed", "Completed"),
    ]

    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="swap_requests"
    )
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="swap_requests_made",
    )
    message = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"Request for {self.item} by {self.from_user}"


class EcoPlace(models.Model):
    """
    Places that support the circular economy: recycling centers, repair shops, donation hubs.
    """

    TYPE_CHOICES = [
        ("recycling", "Recycling Center"),
        ("repair", "Repair Shop"),
        ("donation", "Donation Hub"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=200)
    place_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["city", "name"]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.name


class CommunityPost(models.Model):
    """
    Lightweight community module: sustainability stories, tips, or upcycling ideas.
    """

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="community_posts",
    )
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.title


class ImpactLog(models.Model):
    """
    Simple impact tracking per user over time.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="impact_logs"
    )
    items_kept_in_circulation = models.PositiveIntegerField(
        default=0,
        help_text="How many items were swapped/donated instead of thrown away.",
    )
    co2_saved_kg = models.FloatField(
        default=0.0,
        help_text="Approximate CO₂ saved in kilograms (rough estimate).",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"Impact for {self.user} on {self.created_at.date()}"

