# Products API (existing)

Base prefix: `/api/v1/products`

- `POST /api/v1/products` — create product (201)
- `GET /api/v1/products` — list products
- `GET /api/v1/products/{product_id}` — retrieve one
- `PATCH /api/v1/products/{product_id}` — update
- `DELETE /api/v1/products/{product_id}` — delete (204)

Confirm request/response schemas in `backend/app/schemas/product.py` before writing the frontend service. The UI's active/deactivate and soft-delete expectations must be reconciled with the actual backend behavior.
