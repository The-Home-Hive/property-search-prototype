# Backend — Django

REST API over PostgreSQL. See `docs/decisions/0001-backend-framework-django.md` for why, and `docs/design/technical-design.pdf` for the full data model and query design this implements.

## First-time setup

Requires a running PostgreSQL (the connection string lives in `DATABASE_URL` —
copy `.env.example` at the repo root to `.env` and fill it in first).

```
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py seed_locations           # Country/City/Town from data/source/
python manage.py seed_prices              # PriceRange from data/source/
python manage.py loaddata properties_seed # the fictional property dataset
python manage.py seed_property_images     # 3 photos per property (property_image rows)
python manage.py seed_property_descriptions # a description for each property
python manage.py runserver
```

**Do not skip the seed commands.** `migrate` only creates empty tables and
columns. Without the last two commands the API still works, but every property
has `primary_image: null` and no description, so the result cards show no photo
and the detail modal has no text.

Run the data commands in the order above. `properties_seed.json` references
towns by raw integer id, so it only lines up if `seed_locations` ran first and
seeded countries in its fixed Kenya → Uganda → Tanzania order — see
`apps/properties/fixtures/PROVENANCE.md`. The two `seed_property_*` commands
need the properties to exist, so they come last.

The photos themselves are files in the repo
(`resources/media/properties/<type>/{1,2,3}.jpg`); `seed_property_images` only
creates the database rows that point at them. Django serves them at `/media/`
when `DJANGO_DEBUG=True`, so no extra setup is needed in development.

### After pulling new changes

If a pull adds a migration (look for new files under `apps/*/migrations/`), run
`python manage.py migrate`, then re-run the seed commands. They are safe to
repeat: `seed_property_images` rebuilds the image rows, `seed_property_descriptions`
only fills descriptions that are still empty (add `--force` to regenerate them),
and `seed_locations`, `seed_prices` and `loaddata` leave existing rows in place or overwrite them.

```
pytest        # 29 tests
```

## App layout

| App | Owns | Notes |
|---|---|---|
| `apps/locations` | `Country`, `City`, `Town` | Backs `GET /countries`, `/cities`, `/towns` |
| `apps/pricing` | `PriceRange` | Backs `GET /price-range?country_id=&listing_type=` |
| `apps/properties` | `Property`, `Amenity`, `PropertyAmenity`, `PropertyImage` | Backs `GET /properties?[filters]` (the main search endpoint) and `GET /properties/<id>` (description + image list for the detail modal), plus `GET /amenities` and `GET /property-types` for populating the filter panel |
| `apps/seeding` | nothing (no models) | Parses `data/source/` into `apps/seeding/generated/`, and loads it via management commands |

Each app keeps its own `migrations/`, `serializers.py`, `views.py`, `urls.py` and `tests/` once scaffolded — standard Django app shape, not a shared "models.py at the root" pattern.
