import uuid

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.attribute import Attribute
from app.models.category_attribute import CategoryAttribute


class CategoryAttributeRepository:

    async def get_attributes_by_category(
        self,
        db: AsyncSession,
        category_id: uuid.UUID,
    ) -> list[Attribute]:
        result = await db.execute(
            select(Attribute)
            .join(
                CategoryAttribute,
                CategoryAttribute.attribute_id == Attribute.attribute_id,
            )
            .where(
                CategoryAttribute.category_id == category_id
            )
            .order_by(Attribute.name)
        )

        return list(result.scalars().all())

    async def get_relationship(
        self,
        db: AsyncSession,
        category_id: uuid.UUID,
        attribute_id: uuid.UUID,
    ) -> CategoryAttribute | None:
        result = await db.execute(
            select(CategoryAttribute).where(
                CategoryAttribute.category_id == category_id,
                CategoryAttribute.attribute_id == attribute_id,
            )
        )

        return result.scalar_one_or_none()

    async def create(
        self,
        db: AsyncSession,
        relationship: CategoryAttribute,
    ) -> CategoryAttribute:
        db.add(relationship)
        await db.flush()
        await db.refresh(relationship)

        return relationship

    async def delete(
        self,
        db: AsyncSession,
        relationship: CategoryAttribute,
    ) -> None:
        await db.delete(relationship)
        await db.flush()