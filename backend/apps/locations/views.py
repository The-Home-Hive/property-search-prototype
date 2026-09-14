from rest_framework import generics

from .models import City, Country, Town
from .serializers import CitySerializer, CountrySerializer, TownSerializer


class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all().order_by("name")
    serializer_class = CountrySerializer


class CityListView(generics.ListAPIView):
    serializer_class = CitySerializer

    def get_queryset(self):
        queryset = City.objects.all().order_by("name")
        country_id = self.request.query_params.get("country_id")
        if country_id:
            queryset = queryset.filter(country_id=country_id)
        return queryset


class TownListView(generics.ListAPIView):
    serializer_class = TownSerializer

    def get_queryset(self):
        queryset = Town.objects.all().order_by("name")
        city_id = self.request.query_params.get("city_id")
        if city_id:
            queryset = queryset.filter(city_id=city_id)
        return queryset
