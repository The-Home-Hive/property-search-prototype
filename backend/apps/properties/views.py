from django.db.models import Prefetch
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Amenity, Property, PropertyImage
from .serializers import AmenitySerializer, PropertyDetailSerializer, PropertySerializer


class AmenityListView(generics.ListAPIView):
    """Every amenity offered in the filter panel. IDs are what /properties expects."""

    queryset = Amenity.objects.all().order_by("name")
    serializer_class = AmenitySerializer


class PropertyTypeListView(APIView):
    """The distinct property types actually present on active listings.

    Property type is a free-text column rather than its own table, so there are
    no IDs here — the strings returned are exactly what /properties?property_type=
    matches on.
    """

    def get(self, request):
        types = (
            Property.objects.filter(status="active")
            .order_by("property_type")
            .values_list("property_type", flat=True)
            .distinct()
        )
        return Response(list(types))


def _with_related(queryset):
    """Town/city/country, amenities and ordered images, without N+1 queries."""
    return queryset.select_related("town__city__country").prefetch_related(
        "amenities",
        Prefetch("images", queryset=PropertyImage.objects.order_by("sort_order")),
    )


class PropertyDetailView(generics.RetrieveAPIView):
    """One active property with its description and full ordered image list."""

    serializer_class = PropertyDetailSerializer

    def get_queryset(self):
        return _with_related(Property.objects.filter(status="active"))


class PropertySearchView(generics.ListAPIView):
    serializer_class = PropertySerializer

    def get_queryset(self):
        queryset = _with_related(Property.objects.filter(status="active"))
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
