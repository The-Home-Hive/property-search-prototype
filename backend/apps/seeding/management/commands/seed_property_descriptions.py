from django.core.management.base import BaseCommand

from apps.properties.models import Property
from apps.seeding.generators.descriptions import build_description


class Command(BaseCommand):
    help = (
        "Generates a description for every property that lacks one "
        "(pass --force to regenerate all)."
    )

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Overwrite existing descriptions.")

    def handle(self, *args, **options):
        queryset = Property.objects.select_related("town__city__country").prefetch_related(
            "amenities"
        )
        if not options["force"]:
            queryset = queryset.filter(description__isnull=True)

        updated = []
        for prop in queryset:
            names = sorted(a.name for a in prop.amenities.all())
            prop.description = build_description(prop, names)
            updated.append(prop)

        Property.objects.bulk_update(updated, ["description"], batch_size=100)
        self.stdout.write(self.style.SUCCESS(f"wrote descriptions for {len(updated)} properties"))
