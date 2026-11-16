import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.attribute import Attribute
from app.repositories.attribute import AttributeRepository
from app.schemas.attribute import AttributeCreate, AttributeUpdate


class AttributeService:

    def __init__(self):
        self.repository = AttributeRepository()

    async def create(
        self,
        db: AsyncSession,
        data: AttributeCreate,
    ) -> Attribute:
        attribute = Attribute(
            name=data.name.strip(),
        )

        return await self.repository.create(
            db,
            attribute,
        )

    async def get_all(
        self,
        db: AsyncSession,
    ) -> list[Attribute]:
        return await self.repository.get_all(db)

    async def get_by_id(
        self,
        db: AsyncSession,
        attribute_id: uuid.UUID,
    ) -> Attribute | None:
        return await self.repository.get_by_id(
            db,
            attribute_id,
        )

    async def update(
        self,
        db: AsyncSession,
        attribute_id: uuid.UUID,
        data: AttributeUpdate,
    ) -> Attribute | None:
        attribute = await self.repository.get_by_id(
            db,
            attribute_id,
        )

        if not attribute:
            return None

        if data.name is not None:
            attribute.name = data.name.strip()

        return await self.repository.update(
            db,
            attribute,
        )

    async def delete(
        self,
        db: AsyncSession,
        attribute_id: uuid.UUID,
    ) -> Attribute | None:
        attribute = await self.repository.get_by_id(
            db,
            attribute_id,
        )

        if not attribute:
            return None

        await self.repository.delete(
            db,
            attribute,
        )

        return attribute