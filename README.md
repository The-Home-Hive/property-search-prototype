# Property Search Prototype

A property search web app for Kenya, Tanzania and Uganda: switch between For Sale and To Rent, narrow down by country → city → town, set a price range in the correct local currency, and filter by property type, bedrooms, bathrooms and amenities. No ranking or relevance scoring — a property either matches every active filter or it doesn't, and results update as filters are added, changed or cleared.

This repo covers the prototype phase: proving the search and filtering approach works end to end, on a small fictional dataset, before it's extended into the full platform.

## Architecture

Three layers, talking over a REST API:

```
frontend (React)  --HTTP-->  backend (Django + DRF)  --SQL-->  PostgreSQL
```

- **Frontend** — the tabs, location/price dropdowns, filter panel and results grid. Built responsive-first, so one codebase covers desktop and mobile.
- **Backend** — owns all filter-combination logic. Exposes endpoints for populating dropdowns (`/countries`, `/cities`, `/towns`, `/price-range`) and for running searches (`/properties`). The frontend never combines filters itself.
- **Database** — reference data (countries, cities, towns, price ranges, amenities) separated from transactional data (the property listings), so dropdown population stays fast regardless of listing volume.

Full design detail — schema, the search query construction rules, indexing strategy, API surface — is in [`docs/design/technical-design.pdf`](docs/design/technical-design.pdf). The framework choice is recorded in [`docs/decisions/0001-backend-framework-django.md`](docs/decisions/0001-backend-framework-django.md).

## Repository structure

```
.
├── docs/                    Requirements, technical design, decision records
│   ├── requirements/
│   ├── design/
│   └── decisions/
├── data/
│   └── source/              Raw client-supplied reference data (source of truth) — by country
│       ├── kenya/
│       ├── tanzania/
│       └── uganda/
├── backend/                 Django REST API
│   ├── config/               Project settings, urls (generated on setup — see backend/README.md)
│   └── apps/
│       ├── locations/         Country, City, Town
│       ├── pricing/            PriceRange
│       ├── properties/         Property, Amenity, PropertyAmenity + search endpoint
│       └── seeding/             Parses data/source/ into the database
├── frontend/                 React app
│   └── src/
│       ├── components/         SearchBar, FilterPanel, ResultsGrid
│       ├── api/                  Backend endpoint wrappers
│       ├── hooks/
│       └── pages/
└── scripts/                  One-off dev/ops scripts
```

Every non-obvious folder has its own short `README.md` — read the one closest to what you're touching before adding files.

## Getting started

Backend and frontend each have their own setup instructions:

- [`backend/README.md`](backend/README.md) — Django project setup, running migrations, seeding the database.
- [`frontend/README.md`](frontend/README.md) — installing dependencies, running the dev server.

Copy `.env.example` to `.env` and fill in real values before running either.

## Data and seeding

The client supplied raw reference data — city/town lists and price-dropdown ranges per country — as CSV and Word files. Those live untouched in `data/source/`, organized by country, and are treated as source of truth: if a value needs to change, it changes there first.

`backend/apps/seeding/` parses those raw files into the database via two management commands, `seed_locations` and `seed_prices`. Nothing in `data/source/` is loaded by hand, and the generated intermediate files are never hand-edited — rerun the parser instead.

## Project status

Currently in the prototype phase described in `docs/requirements/property-search-prototype-overview.pdf`: roughly a two-week build across setup, core build, a review pause, refinement, and handover. This repo structure is the setup-phase deliverable; models, endpoints and components get filled in during core build.

## Docs

| Doc | Covers |
|---|---|
| [`docs/requirements/property-search-prototype-overview.pdf`](docs/requirements/property-search-prototype-overview.pdf) | Plain-language scope and the proposed build timeline |
| [`docs/design/technical-design.pdf`](docs/design/technical-design.pdf) | Architecture, data model, query construction, indexing, API surface |
| [`docs/decisions/`](docs/decisions/) | Architecture decision records — one file per significant choice |
