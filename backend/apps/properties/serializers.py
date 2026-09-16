from rest_framework import serializers

from .models import Amenity, Property


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ["id", "name"]


class PropertySerializer(serializers.ModelSerializer):
    town = serializers.CharField(source="town.name")
    city = serializers.CharField(source="town.city.name")
    country = serializers.CharField(source="town.city.country.name")
    amenities = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")

    class Meta:
        model = Property
        fields = [
            "id",
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
