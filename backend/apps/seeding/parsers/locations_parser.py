"""Parses <country>_cities_and_towns.csv files into Country/City/Town rows."""

import csv
from pathlib import Path

from apps.locations.models import City, Country, Town

# Countries are seeded in this fixed order (not a directory glob) so that a
# fresh run's auto-increment IDs match the ones baked into
# apps/properties/fixtures/properties_seed.json (see PROVENANCE.md next to it).
COUNTRY_ORDER = ["kenya", "uganda", "tanzania"]

COUNTRY_CURRENCY = {
    "Kenya": "KES",
    "Uganda": "UGX",
    "Tanzania": "TZS",
}


def parse_and_load(csv_path: Path) -> dict:
    """Loads one <country>_cities_and_towns.csv file. Idempotent."""
    counts = {"countries": 0, "cities": 0, "towns": 0}

    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            country_name = row["Country"].strip()
            city_name = row["City"].strip()
            town_name = row["Town"].strip()

            country, created = Country.objects.get_or_create(
                name=country_name,
                defaults={"currency_code": COUNTRY_CURRENCY[country_name]},
            )
            counts["countries"] += int(created)

            city, created = City.objects.get_or_create(country=country, name=city_name)
            counts["cities"] += int(created)

            _, created = Town.objects.get_or_create(city=city, name=town_name)
            counts["towns"] += int(created)

    return counts
