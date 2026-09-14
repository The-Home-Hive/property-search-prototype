from rest_framework import serializers

from .models import City, Country, Town


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name", "currency_code"]


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["id", "name"]


class TownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Town
        fields = ["id", "name"]
