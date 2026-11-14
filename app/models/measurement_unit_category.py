import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKeyConstraint, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class MeasurementUnitCategory(Base):
    __tablename__ = "measurement_unit_categories"
    __table_args__ = (
        ForeignKeyConstraint(
            ["category_id", "default_unit_id"],
            ["measurement_units.category_id", "measurement_units.unit_id"],
            name="measurement_unit_categories_default_unit_same_category_fkey",
            ondelete="RESTRICT",
        ),
    )

    category_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    default_unit_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, server_default="true", nullable=False)
