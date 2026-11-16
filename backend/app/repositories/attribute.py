import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.attribute import Attribute


class AttributeRepository:

    async def create(
        self,
        db: AsyncSession,
        attribute: Attribute,
    ) -> Attribute:
        db.add(attribute)
        await db.flush()
        await db.refresh(attribute)
        return attribute

    async def get_by_id(
        self,
        db: AsyncSession,
        attribute_id: uuid.UUID,
    ) -> Attribute | None:
        result = await db.execute(
            select(Attribute).where(
                Attribute.attribute_id == attribute_id,
            )
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        db: AsyncSession,
    ) -> list[Attribute]:
        result = await db.execute(
            select(Attribute).order_by(Attribute.name)
        )
        return list(result.scalars().all())

    async def update(
        self,
        db: AsyncSession,
        attribute: Attribute,
    ) -> Attribute:
        await db.flush()
        await db.refresh(attribute)
        return attribute

    async def delete(
        self,
        db: AsyncSession,
        attribute: Attribute,
    ) -> None:
        await db.delete(attribute)
        await db.flush()