# Attributes and Variants API (existing)

- `POST /api/v1/attributes`, `GET /api/v1/attributes`, `GET /api/v1/attributes/{attribute_id}`, `PATCH /api/v1/attributes/{attribute_id}`, `DELETE /api/v1/attributes/{attribute_id}`
- `GET /api/v1/categories/{category_id}/attributes`, `POST /api/v1/categories/{category_id}/attributes`, `DELETE /api/v1/categories/{category_id}/attributes/{attribute_id}`
- `POST /api/v1/products/{product_id}/variants`, `GET /api/v1/products/{product_id}/variants`, `GET /api/v1/products/{product_id}/variants/{variant_id}`, `DELETE /api/v1/products/{product_id}/variants/{variant_id}`
- `POST /api/v1/variants/{variant_id}/attributes`, `GET /api/v1/variants/{variant_id}/attributes`, `PATCH /api/v1/variants/{variant_id}/attributes/{variant_attribute_id}`, `DELETE /api/v1/variants/{variant_id}/attributes/{variant_attribute_id}`

The inspected variant router does not currently expose `PATCH /products/{product_id}/variants/{variant_id}`; the Framer UI has an Edit Variant flow, so that contract needs a decision before integration.
