from pathlib import Path

from django.core.management.base import BaseCommand

from apps.locations.models import Country
from apps.pricing.models import PriceRange
from apps.seeding.parsers.price_list_parser import parse

DATA_SOURCE_DIR = Path(__file__).resolve().parents[5] / "data" / "source"


class Command(BaseCommand):
    help = (
        "Seeds PriceRange from data/source/<country>/<country>_{sale,rent}_price_list.docx"
    )

    def handle(self, *args, **options):
        docx_paths = sorted(DATA_SOURCE_DIR.glob("*/*_sale_price_list.docx")) + sorted(
            DATA_SOURCE_DIR.glob("*/*_rent_price_list.docx")
        )

        for docx_path in docx_paths:
            result = parse(docx_path)
            country = Country.objects.get(name=result["country"])
            _, created = PriceRange.objects.update_or_create(
                country=country,
                listing_type=result["listing_type"],
                defaults={
                    "currency_code": result["currency_code"],
                    "min_price": result["min_price"],
                    "max_price": result["max_price"],
                },
            )
            verb = "created" if created else "updated"
            self.stdout.write(
                self.style.SUCCESS(
                    f"{verb} {result['country']} {result['listing_type']}: "
                    f"{result['min_price']}-{result['max_price']} {result['currency_code']}"
                )
            )
