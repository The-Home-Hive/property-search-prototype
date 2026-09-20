# properties

Owns `Property`, `Amenity`, `PropertyAmenity`, and three endpoints:

| Endpoint | Returns |
|---|---|
| `GET /properties?[filters]` | The main search. |
| `GET /amenities` | `[{id, name}]` — the ids `/properties?amenities=` matches on. |
| `GET /property-types` | `["Apartment", ...]` — the distinct `property_type` values on active listings. |

`/amenities` and `/property-types` exist so the filter panel can populate itself
from the database instead of hardcoding values that have to be kept in sync with
the seed fixture. Property type is a free-text column rather than its own table,
so it has no ids — the strings returned are exactly what `?property_type=`
matches.

Search has no ranking or scoring — every optional filter parameter that's present gets appended as a `WHERE`/join condition; a property matches only if it satisfies all of them. See technical-design.pdf section 3 for the exact query shape and section 4 for the indexing strategy (composite index on `town_id, listing_type, price`, plus separate indexes on `property_type`/`bedrooms` and the `property_amenity` FK pair).

Seed data here is fictional test properties spanning all three countries — used to prove filter combinations work, not real listings.
