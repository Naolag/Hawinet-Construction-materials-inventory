import uuid

from pydantic import BaseModel


class CategoryAttributeCreate(BaseModel):
    attribute_id: uuid.UUID


class CategoryAttributeResponse(BaseModel):
    attribute_id: uuid.UUID
    name: str