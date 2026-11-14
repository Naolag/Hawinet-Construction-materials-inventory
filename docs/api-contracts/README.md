# API and Backend Deviation Notes

API integration is deliberately out of scope for this frontend pass. The Next.js interface uses local illustrative sample records only. Do not add fetch calls, API base URLs, credentials, authentication or persistence until explicitly authorized.

## Preserve backend behavior
The existing FastAPI application was moved from the repository root into `backend/app` and `backend/tests` without editing its Python source. The backend currently contains product, category, attribute, variant and measurement-unit routes, schemas, services and repositories. Transaction endpoints, inventory-item configuration and related workflows may require later backend work; do not invent endpoint contracts in the UI implementation.

## Known design/backend alignment topics to revisit later
- Product UI distinguishes identity from inventory, while existing product schema fields may still include quantity and price.
- Inventory item records, base units, alternative units, item-specific conversion factors and per-unit prices need to be reconciled with the existing schema.
- Transaction workflows and draft/post/void lifecycle need backend support and atomic stock updates.
- Sales payment state must support paid, partially paid and unpaid amounts.
- Returns must reference original transactions and validate eligible return quantities.
- Employee access, roles and settings require backend/authentication support.

These are implementation review notes, not claims that the backend already supports these features.
