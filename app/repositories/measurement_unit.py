import uuid

from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.measurement_unit import MeasurementUnit, MeasurementUnitCategory


class MeasurementUnitRepository:

    async def create(self, db: AsyncSession, unit: MeasurementUnit) -> MeasurementUnit:
        db.add(unit)
        await db.flush()
        await db.refresh(unit)
        return unit

    async def get_by_id(self, db: AsyncSession, unit_id: uuid.UUID) -> MeasurementUnit | None:
        result = await db.execute(select(MeasurementUnit).where(
            MeasurementUnit.unit_id == unit_id,
            MeasurementUnit.is_active.is_(True),
        ))
        return result.scalar_one_or_none()

    async def get_all(self, db: AsyncSession) -> list[MeasurementUnit]:
        result = await db.execute(
            select(MeasurementUnit)
            .outerjoin(MeasurementUnitCategory, MeasurementUnitCategory.category_id == MeasurementUnit.category_id)
            .where(
                MeasurementUnit.is_active.is_(True),
                or_(
                    MeasurementUnit.category_id.is_(None),
                    and_(
                        MeasurementUnitCategory.is_active.is_(True),
                        MeasurementUnitCategory.default_unit_id == MeasurementUnit.unit_id,
                    ),
                ),
            )
            .order_by(MeasurementUnit.name)
        )
        return list(result.scalars().all())

    async def get_alternatives(self, db: AsyncSession, primary_unit: MeasurementUnit) -> list[MeasurementUnit]:
        if primary_unit.category_id is None:
            return []
        result = await db.execute(
            select(MeasurementUnit)
            .join(MeasurementUnitCategory, MeasurementUnitCategory.category_id == MeasurementUnit.category_id)
            .where(
                MeasurementUnit.category_id == primary_unit.category_id,
                MeasurementUnit.unit_id != primary_unit.unit_id,
                MeasurementUnit.is_active.is_(True),
                MeasurementUnitCategory.is_active.is_(True),
            )
            .order_by(MeasurementUnit.name)
        )
        return list(result.scalars().all())

    async def find_conflict(self, db: AsyncSession, name: str, symbol: str, exclude_unit_id: uuid.UUID | None = None) -> MeasurementUnit | None:
        query = select(MeasurementUnit).where(or_(
            func.lower(MeasurementUnit.name) == name.lower(),
            func.lower(MeasurementUnit.symbol) == symbol.lower(),
        ))
        if exclude_unit_id is not None:
            query = query.where(MeasurementUnit.unit_id != exclude_unit_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def category_exists(self, db: AsyncSession, category_id: uuid.UUID) -> bool:
        result = await db.execute(select(MeasurementUnitCategory.category_id).where(
            MeasurementUnitCategory.category_id == category_id,
            MeasurementUnitCategory.is_active.is_(True),
        ))
        return result.scalar_one_or_none() is not None

    async def update(self, db: AsyncSession, unit: MeasurementUnit) -> MeasurementUnit:
        await db.flush()
        await db.refresh(unit)
        return unit

    async def deactivate(self, db: AsyncSession, unit: MeasurementUnit) -> MeasurementUnit:
        unit.is_active = False
        await db.flush()
        await db.refresh(unit)
        return unit
