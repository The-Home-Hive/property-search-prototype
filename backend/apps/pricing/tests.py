import pytest
from rest_framework.test import APIClient

from apps.locations.models import Country
from apps.pricing.models import PriceRange

pytestmark = pytest.mark.django_db


@pytest.fixture
def kenya():
    return Country.objects.create(name="Kenya", currency_code="KES")


def test_price_range_returns_matching_bounds(kenya):
    PriceRange.objects.create(
        country=kenya, listing_type="sale", currency_code="KES",
        min_price=500_000, max_price=1_000_000_000,
    )

    response = APIClient().get(f"/price-range?country_id={kenya.id}&listing_type=sale")
    assert response.status_code == 200
    assert response.data == {
        "currency_code": "KES", "min_price": 500_000, "max_price": 1_000_000_000,
    }


def test_price_range_no_match_returns_empty_not_error(kenya):
    response = APIClient().get(f"/price-range?country_id={kenya.id}&listing_type=rent")
    assert response.status_code == 200
    assert response.data == {}
