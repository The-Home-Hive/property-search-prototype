# seeding

No models of its own. This app is the pipeline that turns `data/source/` (the client-supplied raw files) into rows in the `locations` and `pricing` tables.

```
parsers/
    locations_parser.py     # reads <country>_cities_and_towns.csv -> Country/City/Town rows
    price_list_parser.py    # reads <country>_{rent,sale}_price_list.docx -> PriceRange rows
management/commands/
    seed_locations.py       # `python manage.py seed_locations`
    seed_prices.py           # `python manage.py seed_prices`
generated/
    (parser output cached as clean CSV/JSON — gitignored; regenerate with the commands above rather than editing)
```

Rerun the relevant command whenever a file under `data/source/` changes. Don't hand-edit anything in `generated/`.
