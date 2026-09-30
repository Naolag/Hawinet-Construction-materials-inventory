import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product


class ProductRepository:

    async def create(
        self,
        db: AsyncSession,
        product: Product,
    ) -> Product:
        db.add(product)
        await db.flush()
        await db.refresh(product)

        return product

    async def get_by_id(
        self,
        db: AsyncSession,
        product_id: uuid.UUID,
    ) -> Product | None:
        result = await db.execute(
            select(Product).where(
                Product.product_id == product_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_all(
        self,
        db: AsyncSession,
    ) -> list[Product]:
        result = await db.execute(
            select(Product).order_by(Product.created_at.desc())
        )

        return list(result.scalars().all())

    async def update(
        self,
        db: AsyncSession,
        product: Product,
    ) -> Product:
        await db.flush()
        await db.refresh(product)

        return product