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


def test_amenities_endpoint_lists_all_with_ids(amenities):
    response = APIClient().get("/amenities")
    assert response.status_code == 200
    assert response.data == [
        {"id": amenities["garden"].id, "name": "Garden"},
        {"id": amenities["pool"].id, "name": "Pool"},
    ]


def test_property_types_endpoint_lists_distinct_active_types(properties):
    response = APIClient().get("/property-types")
    assert response.status_code == 200
    assert response.data == ["Apartment", "House"]


# --- images, title, description, detail endpoint ---------------------------


def test_search_result_includes_title_and_primary_image(properties):
    from apps.properties.models import PropertyImage

    PropertyImage.objects.create(property=properties["p1"], file_path="properties/apartment/2.svg", sort_order=1)
    PropertyImage.objects.create(
        property=properties["p1"], file_path="properties/apartment/1.svg", sort_order=0, is_primary=True
    )
    response = APIClient().get("/properties", {"town": properties["p1"].town_id})
    result = next(r for r in response.json() if r["id"] == properties["p1"].id)
    assert result["title"] == "3-bedroom Apartment in Westlands, Nairobi"
    assert result["primary_image"].endswith("/media/properties/apartment/1.svg")
    assert result["primary_image"].startswith("http")


def test_primary_image_falls_back_to_lowest_sort_order(properties):
    from apps.properties.models import PropertyImage

    PropertyImage.objects.create(property=properties["p2"], file_path="b.svg", sort_order=1)
    PropertyImage.objects.create(property=properties["p2"], file_path="a.svg", sort_order=0)
    response = APIClient().get("/properties", {"property_type": "House"})
    assert response.json()[0]["primary_image"].endswith("/media/a.svg")


def test_property_without_images_has_null_primary_image(properties):
    response = APIClient().get("/properties", {"property_type": "House"})
    assert response.json()[0]["primary_image"] is None


def test_detail_returns_ordered_images_and_description(properties):
    from apps.properties.models import PropertyImage

    p = properties["p1"]
    p.description = "Lovely."
    p.save()
    PropertyImage.objects.create(property=p, file_path="c.svg", sort_order=2)
    PropertyImage.objects.create(property=p, file_path="a.svg", sort_order=0, is_primary=True)
    PropertyImage.objects.create(property=p, file_path="b.svg", sort_order=1)

    body = APIClient().get(f"/properties/{p.id}").json()
    assert body["description"] == "Lovely."
    assert [i["sort_order"] for i in body["images"]] == [0, 1, 2]
    assert [i["url"].rsplit("/", 1)[-1] for i in body["images"]] == ["a.svg", "b.svg", "c.svg"]
    assert body["images"][0]["is_primary"] is True


def test_detail_404_for_inactive_or_missing(properties):
    client = APIClient()
    assert client.get(f"/properties/{properties['p4_inactive'].id}").status_code == 404
    assert client.get("/properties/999999").status_code == 404
