from django.contrib import admin

from .models import PriceRange


@admin.register(PriceRange)
class PriceRangeAdmin(admin.ModelAdmin):
    list_display = ("country", "listing_type", "currency_code", "min_price", "max_price")
    list_filter = ("country", "listing_type")
