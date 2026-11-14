import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class MeasurementUnitCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    symbol: str = Field(min_length=1, max_length=20)
    category_id: uuid.UUID | None = None

    @field_validator("name", "symbol", mode="before")
    @classmethod
    def strip_and_validate_text(cls, value: str) -> str:
        if not isinstance(value, str):
            raise ValueError("Must be a string")
        value = value.strip()
        if not value:
            raise ValueError("Value cannot be blank")
        return value


class MeasurementUnitUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    symbol: str | None = Field(default=None, min_length=1, max_length=20)
    category_id: uuid.UUID | None = None

    @field_validator("name", "symbol", mode="before")
    @classmethod
    def strip_and_validate_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        if not isinstance(value, str):
            raise ValueError("Must be a string")
        value = value.strip()
        if not value:
            raise ValueError("Value cannot be blank")
        return value

    @model_validator(mode="after")
    def require_a_change(self):
        if not self.model_fields_set:
            raise ValueError("At least one field must be provided")
        if self.name is None and self.symbol is None and "category_id" not in self.model_fields_set:
            raise ValueError("At least one field must be provided")
        return self


class MeasurementUnitResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    unit_id: uuid.UUID
    name: str
    symbol: str
    category_id: uuid.UUID | None
    created_at: datetime
    is_active: bool
