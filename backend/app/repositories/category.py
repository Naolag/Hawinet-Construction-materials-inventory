import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category


class CategoryRepository:

    async def create(
        self,
        db: AsyncSession,
        category: Category,
    ) -> Category:
        db.add(category)
        await db.flush()
        await db.refresh(category)
        return category

    async def get_by_id(
        self,
        db: AsyncSession,
        category_id: uuid.UUID,
    ) -> Category | None:
        result = await db.execute(
            select(Category).where(
                Category.category_id == category_id,
                Category.is_active.is_(True),
            )
        )

        return result.scalar_one_or_none()

    async def get_all(
        self,
        db: AsyncSession,
    ) -> list[Category]:
        result = await db.execute(
            select(Category)
            .where(Category.is_active.is_(True))
            .order_by(Category.name)
        )

        return list(result.scalars().all())

    async def update(
        self,
        db: AsyncSession,
        category: Category,
    ) -> Category:
        await db.flush()
        await db.refresh(category)
        return category