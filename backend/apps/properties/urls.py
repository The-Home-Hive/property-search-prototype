from django.urls import path

from .views import (
    AmenityListView,
    PropertyDetailView,
    PropertySearchView,
    PropertyTypeListView,
)

urlpatterns = [
    path("amenities", AmenityListView.as_view(), name="amenity-list"),
    path("property-types", PropertyTypeListView.as_view(), name="property-type-list"),
    path("properties", PropertySearchView.as_view(), name="property-search"),
    path("properties/<int:pk>", PropertyDetailView.as_view(), name="property-detail"),
]
