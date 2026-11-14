import uuid
from datetime import datetime

from pydantic import BaseModel


class VariantAttributeCreate(BaseModel):
    attribute_id: uuid.UUID
    value: str


class VariantAttributeUpdate(BaseModel):
    value: str


class VariantAttributeResponse(BaseModel):
    variant_attribute_id: uuid.UUID
    attribute_id: uuid.UUID
    attribute_name: str
    value: str
    is_universal: bool
    created_at: datetime