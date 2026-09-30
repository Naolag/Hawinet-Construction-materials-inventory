from fastapi import APIRouter

from app.api.v1.attributes import router as attributes_router
from app.api.v1.categories import router as categories_router
from app.api.v1.category_attributes import router as category_attributes_router
from app.api.v1.products import router as products_router


api_router = APIRouter(prefix="/api/v1")

api_router.include_router(categories_router)
api_router.include_router(attributes_router)
api_router.include_router(category_attributes_router)
api_router.include_router(products_router)