import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.measurement_unit import MeasurementUnit
from app.repositories.measurement_unit import MeasurementUnitRepository
from app.schemas.measurement_unit import (
    MeasurementUnitCreate,
    MeasurementUnitUpdate,
)


class MeasurementUnitService:

    def __init__(self):
        self.repository = MeasurementUnitRepository()

    async def create(
        self,
        db: AsyncSession,
        data: MeasurementUnitCreate,
    ) -> MeasurementUnit | str:
        existing = await self.repository.find_conflict(
            db,
            data.name,
            data.symbol,
        )
        if existing:
            return "unit_already_exists"

        unit = MeasurementUnit(
            name=data.name,
            symbol=data.symbol,
            is_active=True,
        )
        return await self.repository.create(db, unit)

    async def get_all(
        self,
        db: AsyncSession,
    ) -> list[MeasurementUnit]:
        return await self.repository.get_all(db)

    async def get_by_id(
        self,
        db: AsyncSession,
        unit_id: uuid.UUID,
    ) -> MeasurementUnit | None:
        return await self.repository.get_by_id(db, unit_id)

    async def update(
        self,
        db: AsyncSession,
        unit_id: uuid.UUID,
        data: MeasurementUnitUpdate,
    ) -> MeasurementUnit | str | None:
        unit = await self.repository.get_by_id(db, unit_id)
        if not unit:
            return None

        new_name = data.name if data.name is not None else unit.name
        new_symbol = data.symbol if data.symbol is not None else unit.symbol

        existing = await self.repository.find_conflict(
            db,
            new_name,
            new_symbol,
            exclude_unit_id=unit_id,
        )
        if existing:
            return "unit_already_exists"

        unit.name = new_name
        unit.symbol = new_symbol
        return await self.repository.update(db, unit)

    async def deactivate(
        self,
        db: AsyncSession,
        unit_id: uuid.UUID,
    ) -> MeasurementUnit | None:
        unit = await self.repository.get_by_id(db, unit_id)
        if not unit:
            return None
        return await self.repository.deactivate(db, unit)
