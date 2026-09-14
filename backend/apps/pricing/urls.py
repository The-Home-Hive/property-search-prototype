from django.urls import path

from .views import PriceRangeView

urlpatterns = [
    path("price-range", PriceRangeView.as_view(), name="price-range"),
]
