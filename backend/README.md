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
python manage.py runserver
```

Run those four data commands in that order. `properties_seed.json` references
towns by raw integer id, so it only lines up if `seed_locations` ran first and
seeded countries in its fixed Kenya → Uganda → Tanzania order — see
`apps/properties/fixtures/PROVENANCE.md`.

```
pytest        # 24 tests
```

## App layout

| App | Owns | Notes |
|---|---|---|
| `apps/locations` | `Country`, `City`, `Town` | Backs `GET /countries`, `/cities`, `/towns` |
| `apps/pricing` | `PriceRange` | Backs `GET /price-range?country_id=&listing_type=` |
| `apps/properties` | `Property`, `Amenity`, `PropertyAmenity` | Backs `GET /properties?[filters]` (the main search endpoint), plus `GET /amenities` and `GET /property-types` for populating the filter panel |
| `apps/seeding` | nothing (no models) | Parses `data/source/` into `apps/seeding/generated/`, and loads it via management commands |

Each app keeps its own `migrations/`, `serializers.py`, `views.py`, `urls.py` and `tests/` once scaffolded — standard Django app shape, not a shared "models.py at the root" pattern.
