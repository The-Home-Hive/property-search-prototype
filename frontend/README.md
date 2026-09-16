# Frontend — React

Single-page app: For Sale / To Rent tabs, location + price dropdowns, the filter
panel, and the results grid. Built responsive-first (technical-design.pdf
section 1) so the same codebase serves desktop and mobile.

No UI framework and no state library — the surface is small enough that React
plus one stylesheet stays easier to read than the alternatives.

## First-time setup

The app reads the live API, so start the backend first (see
[`../backend/README.md`](../backend/README.md)) — it must be serving on the URL
in `VITE_API_BASE_URL`.

```
cd frontend
npm install
npm run dev      # http://localhost:5173
npm test         # vitest
npm run build
```

`VITE_API_BASE_URL` is read from the repo-root `.env`, not a second one in this
folder — `vite.config.js` sets `envDir: '..'` so there is a single env file for
the whole repo. Django's `DJANGO_CORS_ALLOWED_ORIGINS` already allows
`http://localhost:5173`, so the ports need to match.

## Layout

- `src/pages/SearchPage.jsx` — the one route: owns the filter state, fetches
  countries (the selected country's `currency_code` formats every price on the
  page), and wires the three components together.
- `src/components/SearchBar` — the For Sale / To Rent tabs and the
  country → city → town cascade.
- `src/components/FilterPanel` — price range, property type, bedrooms,
  bathrooms, amenities, and "clear all".
- `src/components/ResultsGrid` — the results list, the loading and error states,
  and the "no properties found" empty state.
- `src/api/` — thin wrappers around the backend endpoints; the only layer that
  knows the API's shape.
- `src/hooks/` — `useSearchFilters` (filter state and the cascade rules),
  `useSearchData` (one hook per endpoint), `useApiResource` (fetch + cancel).
- `src/lib/` — currency formatting and the price-dropdown ladder.

## How the search behaves

- **Country and listing type are always sent.** The technical design leaves them
  unbracketed in the query, and the price band and currency are defined per
  country + listing type, so the page selects the first country as soon as the
  list loads rather than sitting in a state that cannot search. Everything else
  is optional; an unset filter is dropped from the query string entirely.
- **Every filter change re-runs the search.** Each filter is a dependency of the
  search hook, so adding, changing or clearing one refetches, and the previous
  request is aborted so fast changes can't land out of order.
- **The backend does all the combining.** This layer never filters a result set
  client-side.
- **Bedrooms and bathrooms are minimums** (`3+`), because the API filters them
  with `>=`.
- **Ticking several amenities narrows, never widens** — a property must have all
  of them, which is how the API applies the `amenities` id list.
- **No results is a normal outcome**, not an error: the API returns `200` with an
  empty array and the grid renders the empty state.

### Cascade and reset rules

| Change | What it clears | Why |
|---|---|---|
| Country | city, town, min/max price | The old city/town belong to another country, and the price band is in another currency |
| Listing type | min/max price | A rent figure is meaningless against the sale band |
| City | town | The old town belongs to another city |
| Min or max price crossing the other | the other end | The bound just picked wins |
| "Clear all" | every optional filter | Country and listing type are required, so they stay |

## The price dropdowns

`GET /price-range` returns only the bounds for a country + listing type — the
documented `price_range` schema has no step column, so the per-increment values
enumerated in the client's source documents aren't stored. The rungs between the
bounds are therefore derived in `src/lib/priceOptions.js`: it picks a round step
(1, 2, 2.5 or 5 × a power of ten) that keeps the list at roughly forty options,
snaps the intermediate values to exact multiples of that step, and always
includes the true minimum and maximum.

This matters because the Kenyan sale list in `data/source/` runs to about ten
thousand increments — rendering it verbatim would be unusable. If exact
client-specified increments become a requirement, the step belongs in the
`price_range` table and this helper should read it instead of choosing one.
`tests/priceOptions.test.js` covers the ladder against all four real bands.
