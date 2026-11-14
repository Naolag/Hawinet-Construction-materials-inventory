import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProductVariantCreate(BaseModel):
    pass


class ProductVariantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_variant_id: uuid.UUID
    product_id: uuid.UUID
    created_at: datetime