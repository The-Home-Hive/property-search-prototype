# Backend — Django

REST API over PostgreSQL. See `docs/decisions/0001-backend-framework-django.md` for why, and `docs/design/technical-design.pdf` for the full data model and query design this implements.

## First-time setup

This skeleton has the app folders laid out but not the generated Django boilerplate (`manage.py`, `config/settings.py`, migrations) — that's created locally so it matches each developer's Django version:

```
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# generates manage.py and config/{settings,urls,wsgi,asgi}.py in place
django-admin startproject config .

# registers each app (models already have a home — see below)
python manage.py startapp locations apps/locations
python manage.py startapp pricing apps/pricing
python manage.py startapp properties apps/properties
python manage.py startapp seeding apps/seeding

python manage.py migrate
python manage.py seed_locations   # populates Country/City/Town from data/source/
python manage.py seed_prices      # populates PriceRange from data/source/
python manage.py runserver
```

## App layout

| App | Owns | Notes |
|---|---|---|
| `apps/locations` | `Country`, `City`, `Town` | Backs `GET /countries`, `/cities`, `/towns` |
| `apps/pricing` | `PriceRange` | Backs `GET /price-range?country_id=&listing_type=` |
| `apps/properties` | `Property`, `Amenity`, `PropertyAmenity` | Backs `GET /properties?[filters]`, the main search endpoint |
| `apps/seeding` | nothing (no models) | Parses `data/source/` into `apps/seeding/generated/`, and loads it via management commands |

Each app keeps its own `migrations/`, `serializers.py`, `views.py`, `urls.py` and `tests/` once scaffolded — standard Django app shape, not a shared "models.py at the root" pattern.
