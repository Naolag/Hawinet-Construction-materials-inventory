import uuid
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.repositories.category import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:

    def __init__(self):
        self.repository = CategoryRepository()

    async def create(
        self,
        db: AsyncSession,
        data: CategoryCreate,
    ) -> Category:

        category = Category(
            name=data.name.strip(),
            description=data.description,
            parent_category_id=data.parent_category_id,
        )

        return await self.repository.create(db, category)

    async def get_all(
        self,
        db: AsyncSession,
    ):
        return await self.repository.get_all(db)

    async def get_by_id(
        self,
        db: AsyncSession,
        category_id: uuid.UUID,
    ):
        return await self.repository.get_by_id(db, category_id)

    async def update(
        self,
        db: AsyncSession,
        category_id: uuid.UUID,
        data: CategoryUpdate,
    ):
        category = await self.repository.get_by_id(db, category_id)

        if not category:
            return None

        if data.name is not None:
            category.name = data.name.strip()

        if data.description is not None:
            category.description = data.description

        if data.parent_category_id is not None:
            category.parent_category_id = data.parent_category_id

        return await self.repository.update(db, category)

    async def delete(
        self,
        db: AsyncSession,
        category_id: uuid.UUID,
    ):
        category = await self.repository.get_by_id(db, category_id)

        if not category:
            return None

        category.is_active = False
        category.deleted_at = datetime.now(timezone.utc)

        await db.flush()

        return category