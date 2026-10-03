import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.variant_attribute import VariantAttribute
from app.repositories.category_attribute import CategoryAttributeRepository
from app.repositories.product import ProductRepository
from app.repositories.variant import VariantRepository
from app.repositories.variant_attribute import VariantAttributeRepository


class VariantAttributeService:

    def __init__(self):
        self.repository = VariantAttributeRepository()
        self.variant_repository = VariantRepository()
        self.product_repository = ProductRepository()
        self.category_attribute_repository = (
            CategoryAttributeRepository()
        )

    async def create(
        self,
        db: AsyncSession,
        variant_id: uuid.UUID,
        attribute_id: uuid.UUID,
        value: str,
    ):
        variant = await self.variant_repository.get_by_id(
            db,
            variant_id,
        )

        if not variant:
            return "variant_not_found"

        product = await self.product_repository.get_by_id(
            db,
            variant.product_id,
        )

        if not product:
            return "variant_not_found"

        allowed = await self.category_attribute_repository.exists(
            db,
            product.category_id,
            attribute_id,
        )

        if not allowed:
            return "attribute_not_allowed"

        existing = (
            await self.repository.get_by_variant_and_attribute(
                db,
                variant_id,
                attribute_id,
            )
        )

        if existing:
            return "attribute_exists"

        variant_attribute = VariantAttribute(
            variant=variant_id,
            attribute=attribute_id,
            value=value.strip(),
            is_universal=False,
        )

        return await self.repository.create(
            db,
            variant_attribute,
        )

    async def get_all(
        self,
        db: AsyncSession,
        variant_id: uuid.UUID,
    ):
        variant = await self.variant_repository.get_by_id(
            db,
            variant_id,
        )

        if not variant:
            return "variant_not_found"

        product = await self.product_repository.get_by_id(
            db,
            variant.product_id,
        )

        if not product:
            return "variant_not_found"

        return await self.repository.get_by_variant(
            db,
            variant_id,
        )

    async def update(
        self,
        db: AsyncSession,
        variant_id: uuid.UUID,
        variant_attribute_id: uuid.UUID,
        value: str,
    ):
        variant = await self.variant_repository.get_by_id(
            db,
            variant_id,
        )

        if not variant:
            return "variant_attribute_not_found"

        product = await self.product_repository.get_by_id(
            db,
            variant.product_id,
        )

        if not product:
            return "variant_attribute_not_found"

        variant_attribute = await self.repository.get_by_id(
            db,
            variant_attribute_id,
        )

        if not variant_attribute:
            return "variant_attribute_not_found"

        if variant_attribute.variant != variant_id:
            return "variant_attribute_not_found"

        variant_attribute.value = value.strip()

        await db.flush()
        await db.refresh(variant_attribute)

        return variant_attribute

    async def delete(
        self,
        db: AsyncSession,
        variant_id: uuid.UUID,
        variant_attribute_id: uuid.UUID,
    ):
        variant = await self.variant_repository.get_by_id(
            db,
            variant_id,
        )

        if not variant:
            return None

        product = await self.product_repository.get_by_id(
            db,
            variant.product_id,
        )

        if not product:
            return None

        variant_attribute = await self.repository.get_by_id(
            db,
            variant_attribute_id,
        )

        if not variant_attribute:
            return None

        if variant_attribute.variant != variant_id:
            return None

        await self.repository.delete(
            db,
            variant_attribute,
        )

        return variant_attribute