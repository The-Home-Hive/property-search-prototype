from rest_framework import serializers

from .models import PriceRange


class PriceRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceRange
        fields = ["currency_code", "min_price", "max_price"]
