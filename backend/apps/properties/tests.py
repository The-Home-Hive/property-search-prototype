import pytest
from rest_framework.test import APIClient

from apps.locations.models import City, Country, Town
from apps.properties.models import Amenity, Property

pytestmark = pytest.mark.django_db


@pytest.fixture
def locations():
    kenya = Country.objects.create(name="Kenya", currency_code="KES")
    uganda = Country.objects.create(name="Uganda", currency_code="UGX")
    nairobi = City.objects.create(country=kenya, name="Nairobi")
    kampala = City.objects.create(country=uganda, name="Kampala")
    westlands = Town.objects.create(city=nairobi, name="Westlands")
    karen = Town.objects.create(city=nairobi, name="Karen")
    nakawa = Town.objects.create(city=kampala, name="Nakawa")
    return {
        "kenya": kenya, "uganda": uganda,
        "nairobi": nairobi, "kampala": kampala,
        "westlands": westlands, "karen": karen, "nakawa": nakawa,
    }


@pytest.fixture
def amenities():
    return {
        "pool": Amenity.objects.create(name="Pool"),
        "garden": Amenity.objects.create(name="Garden"),
    }


@pytest.fixture
def properties(locations, amenities):
    p1 = Property.objects.create(
        town=locations["westlands"], listing_type="sale", property_type="Apartment",
        price=8_000_000, bedrooms=3, bathrooms=2, status="active",
    )
    p1.amenities.set([amenities["pool"], amenities["garden"]])

    p2 = Property.objects.create(
        town=locations["karen"], listing_type="sale", property_type="House",
        price=20_000_000, bedrooms=5, bathrooms=4, status="active",
    )
    p2.amenities.set([amenities["pool"]])

    p3 = Property.objects.create(
        town=locations["nakawa"], listing_type="rent", property_type="Apartment",
        price=1_500_000, bedrooms=2, bathrooms=1, status="active",
    )

    p4_inactive = Property.objects.create(
        town=locations["westlands"], listing_type="sale", property_type="Apartment",
        price=8_500_000, bedrooms=3, bathrooms=2, status="inactive",
    )

    return {"p1": p1, "p2": p2, "p3": p3, "p4_inactive": p4_inactive}


def search(**params):
    return APIClient().get("/properties", params)


def test_filter_by_country(locations, properties):
    response = search(country=locations["kenya"].id)
    ids = {p["id"] for p in response.data}
    assert ids == {properties["p1"].id, properties["p2"].id}


def test_filter_by_listing_type(locations, properties):
    response = search(listing_type="rent")
    assert [p["id"] for p in response.data] == [properties["p3"].id]


def test_filter_by_city(locations, properties):
    response = search(city=locations["nairobi"].id)
    ids = {p["id"] for p in response.data}
    assert ids == {properties["p1"].id, properties["p2"].id}


def test_filter_by_town(locations, properties):
    response = search(town=locations["karen"].id)
    assert [p["id"] for p in response.data] == [properties["p2"].id]


def test_filter_by_price_range(properties):
    response = search(min_price=5_000_000, max_price=10_000_000)
    assert [p["id"] for p in response.data] == [properties["p1"].id]


def test_filter_by_property_type(properties):
    response = search(property_type="House")
    assert [p["id"] for p in response.data] == [properties["p2"].id]


def test_filter_by_bedrooms_at_least(properties):
    response = search(bedrooms=4)
    assert [p["id"] for p in response.data] == [properties["p2"].id]


def test_filter_by_bathrooms_at_least(properties):
    response = search(bathrooms=4)
    assert [p["id"] for p in response.data] == [properties["p2"].id]


def test_amenity_filter_requires_all_selected(locations, amenities, properties):
    response = search(amenities=f"{amenities['pool'].id},{amenities['garden'].id}")
    assert [p["id"] for p in response.data] == [properties["p1"].id]


def test_inactive_properties_excluded(properties):
    response = search(town=properties["p4_inactive"].town_id)
    ids = {p["id"] for p in response.data}
    assert properties["p4_inactive"].id not in ids


def test_combined_filters(locations, amenities, properties):
    response = search(
        country=locations["kenya"].id, listing_type="sale",
        bedrooms=1, amenities=str(amenities["pool"].id),
    )
    ids = {p["id"] for p in response.data}
    assert ids == {properties["p1"].id, properties["p2"].id}


def test_no_match_returns_empty_200(properties):
    response = search(property_type="Land")
    assert response.status_code == 200
    assert response.data == []
