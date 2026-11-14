import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AttributeCreate(BaseModel):
    name: str


class AttributeUpdate(BaseModel):
    name: str | None = None


class AttributeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    attribute_id: uuid.UUID
    created_at: datetime
    name: str