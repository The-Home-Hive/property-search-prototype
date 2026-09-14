from pathlib import Path

from django.core.management.base import BaseCommand

from apps.seeding.parsers.locations_parser import COUNTRY_ORDER, parse_and_load

DATA_SOURCE_DIR = Path(__file__).resolve().parents[5] / "data" / "source"


class Command(BaseCommand):
    help = "Seeds Country/City/Town from data/source/<country>/<country>_cities_and_towns.csv"

    def handle(self, *args, **options):
        for country in COUNTRY_ORDER:
            csv_path = DATA_SOURCE_DIR / country / f"{country}_cities_and_towns.csv"
            counts = parse_and_load(csv_path)
            self.stdout.write(
                self.style.SUCCESS(
                    f"{country}: +{counts['countries']} countries, "
                    f"+{counts['cities']} cities, +{counts['towns']} towns"
                )
            )
