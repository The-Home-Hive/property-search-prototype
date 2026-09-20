from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils.text import slugify

from apps.properties.models import Property, PropertyImage

IMAGES_PER_TYPE = 3
IMAGE_EXTENSION = "jpg"


class Command(BaseCommand):
    help = (
        "Gives every property a property_image row per photo in the shared "
        "per-type set at backend/resources/media/properties/<type>/{1,2,3}.jpg. "
        "Idempotent: rebuilds each property's rows from scratch."
    )

    def handle(self, *args, **options):
        media_root = Path(settings.MEDIA_ROOT)
        rows = []
        property_ids = []

        for prop in Property.objects.all().order_by("id"):
            slug = slugify(prop.property_type)
            available = [
                f"properties/{slug}/{n}.{IMAGE_EXTENSION}"
                for n in range(1, IMAGES_PER_TYPE + 1)
                if (media_root / "properties" / slug / f"{n}.{IMAGE_EXTENSION}").exists()
            ]
            if not available:
                raise CommandError(
                    f"No images for property type {prop.property_type!r} "
                    f"(expected under {media_root / 'properties' / slug})"
                )
            property_ids.append(prop.id)
            for order, path in enumerate(available):
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
