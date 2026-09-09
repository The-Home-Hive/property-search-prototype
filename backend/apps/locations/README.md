# locations

Owns `Country`, `City`, `Town` — the reference hierarchy every search is scoped to. Selecting a country in the frontend drives which cities/towns populate next; see technical-design.pdf section 2 for the exact schema (`country.currency_code`, `city.country_id` FK, `town.city_id` FK).

Populated by `apps/seeding` management commands from `data/source/<country>/<country>_cities_and_towns.csv`, not by hand.
