from django.db import models


class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name


class Property(models.Model):
    LISTING_TYPE_CHOICES = [
        ("sale", "Sale"),
        ("rent", "Rent"),
    ]
    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]

    town = models.ForeignKey(
        "locations.Town", on_delete=models.CASCADE, related_name="properties"
    )
    listing_type = models.CharField(max_length=4, choices=LISTING_TYPE_CHOICES)
    property_type = models.CharField(max_length=50)
    price = models.BigIntegerField()
    bedrooms = models.SmallIntegerField()
    bathrooms = models.SmallIntegerField()
    furnished = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default="active")
    amenities = models.ManyToManyField(
        Amenity, through="PropertyAmenity", related_name="properties"
    )

    class Meta:
        verbose_name_plural = "properties"
        indexes = [
            models.Index(
                fields=["town", "listing_type", "price"], name="prop_town_ltype_price_idx"
            ),
            models.Index(fields=["property_type"], name="prop_ptype_idx"),
            models.Index(fields=["bedrooms"], name="prop_bedrooms_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.property_type} in {self.town.name} ({self.listing_type})"

    @property
    def title(self) -> str:
        """Display name derived from the row — there is no stored name column.

        Deliberately omits ``property_type`` so the Property Type filter can be
        verified against the field itself rather than the title text.

        Land and offices have no meaningful bedroom count, and studios are
        bedroom-less by definition, so only residential types get the prefix.
        """
        place = f"{self.town.name}, {self.town.city.name}"
        prefixed = self.property_type not in {"Land", "Office", "Studio Apartment"}
        if prefixed and self.bedrooms:
            return f"{self.bedrooms}-bedroom property in {place}"
        return f"Property in {place}"


class PropertyAmenity(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("property", "amenity")

    def __str__(self) -> str:
        return f"{self.property_id} - {self.amenity.name}"


class PropertyImage(models.Model):
    """One image of a property. A property has 2-3 of these (multivalued).

    ``file_path`` is relative to ``settings.MEDIA_ROOT``.
    """

    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="images"
    )
    file_path = models.CharField(max_length=255)
    sort_order = models.SmallIntegerField(default=0)
    is_primary = models.BooleanField(default=False)

    class Meta:
        ordering = ["sort_order"]
        constraints = [
            models.UniqueConstraint(
                fields=["property", "sort_order"], name="prop_image_order_uniq"
            ),
        ]

    def __str__(self) -> str:
        return f"{self.property_id} #{self.sort_order} {self.file_path}"
