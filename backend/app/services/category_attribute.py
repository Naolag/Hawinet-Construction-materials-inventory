import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category_attribute import CategoryAttribute
from app.repositories.category import CategoryRepository
from app.repositories.attribute import AttributeRepository
from app.repositories.category_attribute import CategoryAttributeRepository


class CategoryAttributeService:

    def __init__(self):
        self.repository = CategoryAttributeRepository()
        self.category_repository = CategoryRepository()
        self.attribute_repository = AttributeRepository()

    async def get_attributes(
        self,
        db: AsyncSession,
        category_id: uuid.UUID,
    ):
        category = await self.category_repository.get_by_id(
            db,
            category_id,
        )

        if not category:
            return None

        return await self.repository.get_attributes_by_category(
            db,
            category_id,
        )

    async def add_attribute(
        self,
        db: AsyncSession,
        category_id: uuid.UUID,
        attribute_id: uuid.UUID,
    ):
        category = await self.category_repository.get_by_id(
            db,
            category_id,
        )

        if not category:
            return "category_not_found"

        attribute = await self.attribute_repository.get_by_id(
            db,
            attribute_id,
        )

        if not attribute:
            return "attribute_not_found"

        existing = await self.repository.get_relationship(
            db,
            category_id,
            attribute_id,
        )

        if existing:
            return "relationship_exists"

        relationship = CategoryAttribute(
            category_id=category_id,
            attribute_id=attribute_id,
        )

        return await self.repository.create(
            db,
            relationship,
        )

    async def remove_attribute(
        self,
        db: AsyncSession,
        category_id: uuid.UUID,
        attribute_id: uuid.UUID,
    ):
        relationship = await self.repository.get_relationship(
            db,
            category_id,
            attribute_id,
        )

        if not relationship:
            return None

        await self.repository.delete(
            db,
            relationship,
        )

        return relationship