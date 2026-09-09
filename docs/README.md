# Docs index

- `requirements/property-search-prototype-overview.pdf` — the client-facing overview: what the prototype demonstrates, and the proposed phase-by-phase timeline (roughly two weeks: setup, core build, review pause, refinement, handover).
- `design/technical-design.pdf` — the technical design: three-layer architecture, data model (`country` → `city` → `town`, `price_range`, `property`, `amenity`, `property_amenity`), the search query construction rules, indexing strategy, and the API surface (`/countries`, `/cities`, `/towns`, `/price-range`, `/properties`).
- `decisions/` — architecture decision records (ADRs). One file per significant decision, numbered in the order they were made, never edited after the fact — a reversal gets a new ADR that supersedes the old one.

Read the overview first for the "why," then the technical design for the "how." The ADRs capture choices the technical design left open (e.g. which backend framework).
