from django.conf import settings
from rest_framework import serializers

from .models import Amenity, Property, PropertyImage


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ["id", "name"]


def _media_url(request, file_path):
    url = f"{settings.MEDIA_URL.rstrip('/')}/{file_path}"
    if not url.startswith("/"):
        url = "/" + url
    return request.build_absolute_uri(url) if request else url


class PropertyImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = PropertyImage
        fields = ["id", "url", "sort_order", "is_primary"]

    def get_url(self, obj):
        return _media_url(self.context.get("request"), obj.file_path)


class PropertySerializer(serializers.ModelSerializer):
    town = serializers.CharField(source="town.name")
    city = serializers.CharField(source="town.city.name")
    country = serializers.CharField(source="town.city.country.name")
    amenities = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    title = serializers.CharField(read_only=True)
    primary_image = serializers.SerializerMethodField()

    def get_primary_image(self, obj):
        # Uses the prefetched, sort_order-ordered images: the row flagged
        # is_primary, else the lowest sort_order.
        images = list(obj.images.all())
        if not images:
            return None
        primary = next((i for i in images if i.is_primary), images[0])
        return _media_url(self.context.get("request"), primary.file_path)

    class Meta:
        model = Property
        fields = [
            "id",
            "title",
            "primary_image",
            "town",
            "city",
            "country",
            "listing_type",
            "property_type",
            "price",
            "bedrooms",
            "bathrooms",
            "furnished",
            "status",
            "amenities",
        ]


class PropertyDetailSerializer(PropertySerializer):
    images = PropertyImageSerializer(many=True, read_only=True)

    class Meta(PropertySerializer.Meta):
        fields = PropertySerializer.Meta.fields + ["description", "images"]
