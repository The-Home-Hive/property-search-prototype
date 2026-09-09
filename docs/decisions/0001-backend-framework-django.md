# ADR 0001: Backend framework — Django

## Status

Accepted — 2026-09-09

## Context

`docs/design/technical-design.pdf` specifies a REST API backend over PostgreSQL, and names Django or Node/Express as equally viable options for the prototype. The data model is small and relational (six reference/transactional tables), the search endpoint is a single parameterized query with optional filter clauses, and there's a recurring need to load and re-load reference data (countries, cities, towns, price ranges) from the source files in `data/source/`.

## Decision

Build the backend with Django (Python), using Django REST Framework for the API layer and the Django ORM against PostgreSQL.

## Rationale

- The admin panel gives a working interface for inspecting and hand-correcting seeded reference data without writing a separate internal tool.
- Django's migration system tracks schema changes for the six-table model cleanly, app by app (`locations`, `pricing`, `properties`).
- Management commands (`manage.py seed_locations`, `manage.py seed_prices`) are a natural fit for the parse-raw-data-into-the-database pipeline described in `backend/apps/seeding/`.
- The ORM's query builder maps directly onto the conditional `WHERE` clause construction described in section 3 of the technical design (append a filter only if the parameter is present).

## Consequences

- The frontend (React) and backend are different languages, so there's no shared type layer between them — API contracts need to be documented explicitly (see `backend/apps/*/serializers.py` once built, and keep `docs/design/technical-design.pdf` section 5 as the source of truth for endpoints).
- Team members need Python familiarity, not just JavaScript.
