# Hawinet — Construction Material Inventory Management

Hawinet is an inventory-management workspace for a construction-material shop.

## Repository layout
- `backend/` — the existing FastAPI application and tests, relocated without editing their source contents.
- `frontend/` — Next.js App Router visual prototype recreated from the Framer workspace.
- `docs/` — design system, page specifications, business rules, API handoff and architecture notes.

## Frontend
```bash
cd frontend
npm install
npm run dev
```
The frontend is a visual prototype with local state only. It does not call the backend, connect to a database, or perform real stock movements.

## Backend
The original FastAPI source and tests are under `backend/app` and `backend/tests`. Their contents are preserved. See `backend/README.md` for setup notes.
