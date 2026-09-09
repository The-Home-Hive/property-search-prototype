# Frontend — React

Single-page app: For Sale / To Rent tabs, location + price dropdowns, the filter panel, and the results grid. Built responsive-first (technical-design.pdf section 1) so the same codebase serves desktop and mobile.

## First-time setup

```
cd frontend
npm install
npm run dev
```

## Layout

- `src/components/SearchBar` — country/city/town dropdowns and the For Sale / To Rent tabs.
- `src/components/FilterPanel` — price range, property type, bedrooms, bathrooms, amenities.
- `src/components/ResultsGrid` — the results list, including the "no properties found" empty state.
- `src/api/` — thin wrappers around the five backend endpoints (`/countries`, `/cities`, `/towns`, `/price-range`, `/properties`) — this is the only layer that knows the API's shape.
- `src/hooks/` — shared state logic (e.g. the selected-country → dependent-dropdown cascade).
- `src/pages/` — top-level route(s); the prototype likely needs just one.
