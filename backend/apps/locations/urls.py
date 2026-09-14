from django.urls import path

from .views import CityListView, CountryListView, TownListView

urlpatterns = [
    path("countries", CountryListView.as_view(), name="country-list"),
    path("cities", CityListView.as_view(), name="city-list"),
    path("towns", TownListView.as_view(), name="town-list"),
]
