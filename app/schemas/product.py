import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ProductCreate(BaseModel):
    category_id: uuid.UUID
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None
    quantity: int | None = None
    price: Decimal | None = None
    brand: str | None = None


class ProductUpdate(BaseModel):
    category_id: uuid.UUID | None = None
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None
    quantity: int | None = None
    price: Decimal | None = None
    brand: str | None = None


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: uuid.UUID
    category_id: uuid.UUID
    created_at: datetime
    description: str | None
    name: str | None
    is_active: bool | None
    quantity: int | None
    price: Decimal | None
    brand: str | None