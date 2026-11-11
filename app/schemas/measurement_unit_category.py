import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MeasurementUnitCategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    category_id: uuid.UUID
    name: str
    description: str | None
    default_unit_id: uuid.UUID
    created_at: datetime
    is_active: bool
