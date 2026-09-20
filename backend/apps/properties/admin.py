from django.contrib import admin

from .models import Amenity, Property, PropertyAmenity, PropertyImage


class PropertyAmenityInline(admin.TabularInline):
    model = PropertyAmenity
    extra = 1


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 0


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "town",
        "listing_type",
        "property_type",
        "price",
        "bedrooms",
        "bathrooms",
        "furnished",
        "status",
    )
    list_filter = ("listing_type", "property_type", "status", "furnished")
    inlines = [PropertyAmenityInline, PropertyImageInline]
