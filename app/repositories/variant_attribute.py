import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.attribute import Attribute
from app.models.variant_attribute import VariantAttribute


class VariantAttributeRepository:

    async def create(
        self,
        db: AsyncSession,
        variant_attribute: VariantAttribute,
    ) -> VariantAttribute:
        db.add(variant_attribute)
        await db.flush()
        await db.refresh(variant_attribute)

        return variant_attribute

    async def get_by_id(
        self,
        db: AsyncSession,
        variant_attribute_id: uuid.UUID,
    ) -> VariantAttribute | None:
        result = await db.execute(
            select(VariantAttribute).where(
                VariantAttribute.variant_attribute_id
                == variant_attribute_id
            )
        )

        return result.scalar_one_or_none()

    async def get_by_id_with_name(
        self,
        db: AsyncSession,
        variant_attribute_id: uuid.UUID,
    ):
        result = await db.execute(
            select(
                VariantAttribute,
                Attribute.name,
            )
            .join(
                Attribute,
                Attribute.attribute_id == VariantAttribute.attribute,
            )
            .where(
                VariantAttribute.variant_attribute_id
                == variant_attribute_id
            )
        )

        return result.one_or_none()

    async def get_by_variant(
        self,
        db: AsyncSession,
        variant_id: uuid.UUID,
    ):
        result = await db.execute(
            select(
                VariantAttribute,
                Attribute.name,
            )
            .join(
                Attribute,
                Attribute.attribute_id == VariantAttribute.attribute,
            )
            .where(
                VariantAttribute.variant == variant_id,
            )
            .order_by(VariantAttribute.created_at)
        )

        return result.all()

    async def get_by_variant_and_attribute(
        self,
        db: AsyncSession,
        variant_id: uuid.UUID,
        attribute_id: uuid.UUID,
    ) -> VariantAttribute | None:
        result = await db.execute(
            select(VariantAttribute).where(
                VariantAttribute.variant == variant_id,
                VariantAttribute.attribute == attribute_id,
            )
        )

        return result.scalar_one_or_none()

    async def delete(
        self,
        db: AsyncSession,
        variant_attribute: VariantAttribute,
    ) -> None:
        await db.delete(variant_attribute)
        await db.flush()