# Hawinet — Construction Material Inventory Management

Hawinet is a specialized inventory-management workspace for a local construction-material shop.

## Repository layout
- `backend/`: existing FastAPI application, moved without source edits.
- `frontend/`: Next.js UI recreation based on the Framer design.
- `docs/`: design system, page specifications and backend-deviation notes.

## Frontend
```bash
cd frontend
npm install
npm run dev
```

The current frontend is a static design prototype using illustrative local data. It intentionally has no API integration, authentication or persistent operations.

## Backend
The existing FastAPI source is located in `backend/app`. Its code was relocated only; no endpoint, model, schema, repository or service behavior was changed as part of the UI work.
