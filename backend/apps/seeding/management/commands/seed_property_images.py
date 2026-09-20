from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.text import slugify

from apps.properties.models import Property, PropertyImage

IMAGES_PER_TYPE = 3


class Command(BaseCommand):
    help = (
        "Gives every property 2-3 property_image rows pointing at the shared "
        "per-type placeholders in backend/resources/media/properties/<type>/. "
        "Idempotent: rebuilds each property's rows from scratch."
    )

    def handle(self, *args, **options):
        media_root = Path(settings.MEDIA_ROOT)
        rows = []
        property_ids = []

        for prop in Property.objects.all().order_by("id"):
            slug = slugify(prop.property_type)
            available = [
                f"properties/{slug}/{n}.svg"
                for n in range(1, IMAGES_PER_TYPE + 1)
                if (media_root / "properties" / slug / f"{n}.svg").exists()
            ]
            if not available:
                raise CommandError(
                    f"No placeholder images for property type {prop.property_type!r} "
                    f"(expected under {media_root / 'properties' / slug})"
                )
            # Deterministic 2 or 3 images per property (never fewer than 2 when
            # the pool has them), so the carousel exercises both counts.
            count = 2 + (prop.id % 2) if len(available) >= 3 else len(available)
            property_ids.append(prop.id)
            for order, path in enumerate(available[:count]):
                rows.append(
                    PropertyImage(
                        property=prop, file_path=path, sort_order=order, is_primary=order == 0
                    )
                )

        with transaction.atomic():
            PropertyImage.objects.filter(property_id__in=property_ids).delete()
            PropertyImage.objects.bulk_create(rows, batch_size=500)

        self.stdout.write(
            self.style.SUCCESS(f"created {len(rows)} images for {len(property_ids)} properties")
        )
