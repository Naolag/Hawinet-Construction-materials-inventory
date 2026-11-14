import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product_variant import ProductVariant


class VariantRepository:

    async def create(
        self,
        db: AsyncSession,
        variant: ProductVariant,
    ) -> ProductVariant:
        db.add(variant)
        await db.flush()
        await db.refresh(variant)

        return variant

    async def get_by_id(
        self,
        db: AsyncSession,
        variant_id: uuid.UUID,
    ) -> ProductVariant | None:
        result = await db.execute(
            select(ProductVariant).where(
                ProductVariant.product_variant_id == variant_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_by_product(
        self,
        db: AsyncSession,
        product_id: uuid.UUID,
    ) -> list[ProductVariant]:
        result = await db.execute(
            select(ProductVariant)
            .where(
                ProductVariant.product_id == product_id,
            )
            .order_by(ProductVariant.created_at)
        )

        return list(result.scalars().all())

    async def delete(
        self,
        db: AsyncSession,
        variant: ProductVariant,
    ) -> None:
        await db.delete(variant)
        await db.flush()