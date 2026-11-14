# Hawinet — Construction Material Inventory Management

Hawinet is a construction-material shop inventory management project. The repository is organized as a monorepo:

- `backend/` — existing FastAPI backend, relocated without changing source contents.
- `frontend/` — Next.js design-only UI implementation based on the Framer prototype. It uses illustrative local data and is not connected to the backend.
- `docs/` — design system, page specifications and API handoff documentation.

## Frontend

```bash
cd frontend
npm install
npm run dev
```

## Backend

The existing backend source and tests are under `backend/`. Its implementation files were moved without content edits. Refer to `backend/README.md` for the original repository note.

## Scope note

The frontend is a visual prototype. No API, database, authentication or live transaction processing is connected.
