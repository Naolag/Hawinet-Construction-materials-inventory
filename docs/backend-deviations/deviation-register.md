# Backend Deviation Register

No backend source changes were made in the frontend replication phase. The original `app/` and `tests/` trees were moved intact into `backend/`.

## Existing API coverage

The current FastAPI router exposes products, categories, measurement units, attributes, category-attribute associations, product variants, and variant-attribute associations.

## UI areas without matching API coverage

- Inventory configuration, current stock balances, minimum-stock thresholds, item-specific conversions and stock valuation.
- All six transaction types, draft/post/void, payments and transaction history.
- Reports, employees, authentication/permissions and workspace settings.

## Contract mismatch to resolve

The UI supports editing a product variant, but the inspected variant router exposes create/list/get/delete and no variant PATCH route. Resolve this before API integration.

No new backend endpoint should be added until the corresponding business rule and data model are agreed. Record any future deviation here before changing backend code.
