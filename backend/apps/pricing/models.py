from django.db import models


class PriceRange(models.Model):
    LISTING_TYPE_CHOICES = [
        ("sale", "Sale"),
        ("rent", "Rent"),
    ]

    country = models.ForeignKey(
        "locations.Country", on_delete=models.CASCADE, related_name="price_ranges"
    )
    listing_type = models.CharField(max_length=4, choices=LISTING_TYPE_CHOICES)
    currency_code = models.CharField(max_length=3)
    min_price = models.BigIntegerField()
    max_price = models.BigIntegerField()

    class Meta:
        unique_together = ("country", "listing_type")

    def __str__(self) -> str:
        return f"{self.country.name} {self.listing_type} ({self.min_price}-{self.max_price} {self.currency_code})"
