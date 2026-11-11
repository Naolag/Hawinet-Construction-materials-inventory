import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.measurement_unit import MeasurementUnit
from app.repositories.measurement_unit import MeasurementUnitRepository
from app.schemas.measurement_unit import MeasurementUnitCreate, MeasurementUnitUpdate


class MeasurementUnitService:
    def __init__(self):
        self.repository = MeasurementUnitRepository()

    async def create(self, db: AsyncSession, data: MeasurementUnitCreate) -> MeasurementUnit | str:
        if await self.repository.find_conflict(db, data.name, data.symbol):
            return "unit_already_exists"
        if data.category_id and not await self.repository.category_exists(db, data.category_id):
            return "category_not_found"
        unit = MeasurementUnit(name=data.name, symbol=data.symbol, category_id=data.category_id, is_active=True)
        return await self.repository.create(db, unit)

    async def get_all(self, db: AsyncSession) -> list[MeasurementUnit]:
        return await self.repository.get_all(db)

    async def get_by_id(self, db: AsyncSession, unit_id: uuid.UUID) -> MeasurementUnit | None:
        return await self.repository.get_by_id(db, unit_id)

    async def get_alternatives(self, db: AsyncSession, unit_id: uuid.UUID) -> list[MeasurementUnit] | None:
        unit = await self.repository.get_by_id(db, unit_id)
        if unit is None:
            return None
        return await self.repository.get_alternatives(db, unit)

    async def update(self, db: AsyncSession, unit_id: uuid.UUID, data: MeasurementUnitUpdate) -> MeasurementUnit | str | None:
        unit = await self.repository.get_by_id(db, unit_id)
        if unit is None:
            return None
        new_name = data.name if data.name is not None else unit.name
        new_symbol = data.symbol if data.symbol is not None else unit.symbol
        if await self.repository.find_conflict(db, new_name, new_symbol, unit_id):
            return "unit_already_exists"
        if "category_id" in data.model_fields_set and data.category_id is not None:
            if not await self.repository.category_exists(db, data.category_id):
                return "category_not_found"
        unit.name, unit.symbol = new_name, new_symbol
        if "category_id" in data.model_fields_set:
            unit.category_id = data.category_id
        return await self.repository.update(db, unit)

    async def deactivate(self, db: AsyncSession, unit_id: uuid.UUID) -> MeasurementUnit | None:
        unit = await self.repository.get_by_id(db, unit_id)
        if unit is None:
            return None
        return await self.repository.deactivate(db, unit)
