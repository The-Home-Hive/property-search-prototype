# Reference data — source of truth

This folder holds the raw reference data exactly as it was supplied by the client, organized by country. Nothing in here is hand-edited — if a number or a town name needs to change, it changes in the client-supplied file (or a corrected version of it), never in a generated seed file.

Each country folder contains:

- `<country>_cities_and_towns.csv` — the country → city → town hierarchy used to populate the `Country`, `City` and `Town` tables.
- `<country>_rent_price_list.docx` — the dropdown values for the "To Rent" price filter, in local currency.
- `<country>_sale_price_list.docx` — the dropdown values for the "For Sale" price filter, in local currency.

These files are parsed by `backend/apps/seeding/parsers/` into clean, machine-loadable seed data under `backend/apps/seeding/generated/`, which is what the Django seed commands actually load into the database. See `backend/apps/seeding/README.md` for that pipeline.

If the client sends an updated or corrected version of one of these files, replace it here and re-run the seed pipeline — don't patch the generated output directly.
