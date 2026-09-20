# properties_seed.json

Transliterated from `seed_properties.sql` (repo root) — the client/dev-supplied
fictional property dataset (220 properties, 6 amenities, 329 property↔amenity
links across Kenya, Uganda and Tanzania).

`town` FKs on `property` rows are raw integer IDs (1–148), not natural keys.
They assume `Town`/`City` rows were seeded with the same auto-increment IDs
`seed_properties.sql` used, which requires countries to be seeded in the exact
order **Kenya → Uganda → Tanzania**, each contributing cities/towns in
`data/source/<country>/<country>_cities_and_towns.csv` row order. This is
exactly what `apps/seeding/parsers/locations_parser.py`'s `COUNTRY_ORDER` does
— don't change that order without regenerating this fixture.

Load order: `migrate` → `seed_locations` → `seed_prices` → `loaddata properties_seed`.

Regenerate with `python manage.py loaddata properties_seed` after truncating
the `property`/`property_amenity`/`amenity` tables, or by re-running the
one-off conversion script that produced this file from `seed_properties.sql`.
