// Existing backend routes only. These constants document future integration; no page calls them.
export const apiEndpoints = {
  products: "/api/v1/products",
  product: (productId: string) => `/api/v1/products/${productId}`,
  categories: "/api/v1/categories",
  category: (categoryId: string) => `/api/v1/categories/${categoryId}`,
  measurementUnits: "/api/v1/measurement-units",
  measurementUnit: (unitId: string) => `/api/v1/measurement-units/${unitId}`,
  attributes: "/api/v1/attributes",
  attribute: (attributeId: string) => `/api/v1/attributes/${attributeId}`,
  categoryAttributes: (categoryId: string) => `/api/v1/categories/${categoryId}/attributes`,
  productVariants: (productId: string) => `/api/v1/products/${productId}/variants`,
  productVariant: (productId: string, variantId: string) => `/api/v1/products/${productId}/variants/${variantId}`,
  variantAttributes: (variantId: string) => `/api/v1/variants/${variantId}/attributes`,
} as const;

// Inventory, transactions, reports, employees and settings endpoints do not exist in the inspected backend yet.
