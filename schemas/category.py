import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CategoryCreate(BaseModel):
    name: str
    description: str | None = None
    parent_category_id: uuid.UUID | None = None


class CategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    parent_category_id: uuid.UUID | None = None


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    category_id: uuid.UUID
    name: str
    description: str | None
    parent_category_id: uuid.UUID | None
    created_at: datetime
    is_active: bool