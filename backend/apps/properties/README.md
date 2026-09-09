# properties

Owns `Property`, `Amenity`, `PropertyAmenity`, and the main search endpoint (`GET /properties?[filters]`).

Search has no ranking or scoring — every optional filter parameter that's present gets appended as a `WHERE`/join condition; a property matches only if it satisfies all of them. See technical-design.pdf section 3 for the exact query shape and section 4 for the indexing strategy (composite index on `town_id, listing_type, price`, plus separate indexes on `property_type`/`bedrooms` and the `property_amenity` FK pair).

Seed data here is fictional test properties spanning all three countries — used to prove filter combinations work, not real listings.
