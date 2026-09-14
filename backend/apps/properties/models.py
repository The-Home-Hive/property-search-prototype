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


class PropertyAmenity(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("property", "amenity")

    def __str__(self) -> str:
        return f"{self.property_id} - {self.amenity.name}"
