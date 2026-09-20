import pytest
from rest_framework.test import APIClient

from apps.locations.models import City, Country, Town

pytestmark = pytest.mark.django_db


@pytest.fixture
def kenya():
    country = Country.objects.create(name="Kenya", currency_code="KES")
    nairobi = City.objects.create(country=country, name="Nairobi")
    Town.objects.create(city=nairobi, name="Westlands")
    return country


def test_countries_list(kenya):
    response = APIClient().get("/countries")
    assert response.status_code == 200
    assert [c["name"] for c in response.data] == ["Kenya"]


def test_cities_filtered_by_country(kenya):
    other = Country.objects.create(name="Uganda", currency_code="UGX")
    City.objects.create(country=other, name="Kampala")

    response = APIClient().get(f"/cities?country_id={kenya.id}")
    assert response.status_code == 200
    assert [c["name"] for c in response.data] == ["Nairobi"]


def test_towns_filtered_by_city(kenya):
    city = kenya.cities.get(name="Nairobi")
    response = APIClient().get(f"/towns?city_id={city.id}")
    assert response.status_code == 200
    assert [t["name"] for t in response.data] == ["Westlands"]
