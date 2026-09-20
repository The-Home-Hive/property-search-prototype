from rest_framework import generics

from .models import Property
from .serializers import PropertySerializer


class PropertySearchView(generics.ListAPIView):
    serializer_class = PropertySerializer

    def get_queryset(self):
        queryset = Property.objects.filter(status="active").select_related(
            "town__city__country"
        )
        params = self.request.query_params

        if params.get("country"):
            queryset = queryset.filter(town__city__country_id=params["country"])
        if params.get("listing_type"):
            queryset = queryset.filter(listing_type=params["listing_type"])
        if params.get("city"):
            queryset = queryset.filter(town__city_id=params["city"])
        if params.get("town"):
            queryset = queryset.filter(town_id=params["town"])
        if params.get("min_price"):
            queryset = queryset.filter(price__gte=params["min_price"])
        if params.get("max_price"):
            queryset = queryset.filter(price__lte=params["max_price"])
        if params.get("property_type"):
            queryset = queryset.filter(property_type=params["property_type"])
        if params.get("bedrooms"):
            queryset = queryset.filter(bedrooms__gte=params["bedrooms"])
        if params.get("bathrooms"):
            queryset = queryset.filter(bathrooms__gte=params["bathrooms"])

        amenities = [a for a in params.get("amenities", "").split(",") if a]
        for amenity_id in amenities:
            queryset = queryset.filter(amenities__id=amenity_id)

        return queryset.distinct()
