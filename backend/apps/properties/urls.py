from django.urls import path

from .views import PropertySearchView

urlpatterns = [
    path("properties", PropertySearchView.as_view(), name="property-search"),
]
