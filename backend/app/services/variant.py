import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product_variant import ProductVariant
from app.repositories.product import ProductRepository
from app.repositories.variant import VariantRepository


class VariantService:

    def __init__(self):
        self.repository = VariantRepository()
        self.product_repository = ProductRepository()

    async def create(
        self,
        db: AsyncSession,
        product_id: uuid.UUID,
    ):
        product = await self.product_repository.get_by_id(
            db,
            product_id,
        )

        if not product:
            return "product_not_found"
        if product.is_active is not True:
            return "product_inactive"

        variant = ProductVariant(
            product_id=product_id,
        )

        return await self.repository.create(
            db,
            variant,
        )

    async def get_by_product(
        self,
        db: AsyncSession,
        product_id: uuid.UUID,
    ):
        product = await self.product_repository.get_by_id(
            db,
            product_id,
        )

        if not product:
            return "product_not_found"

        return await self.repository.get_by_product(
            db,
            product_id,
        )

    async def get_by_id(
        self,
        db: AsyncSession,
        product_id: uuid.UUID,
        variant_id: uuid.UUID,
    ):
        
        product = await self.product_repository.get_by_id(
            db,
            product_id,
        )
        if not product:
            return None
        variant = await self.repository.get_by_id(
            db,
            variant_id,
        )

        if not variant:
            return None

        if variant.product_id != product_id:
            return None

        return variant

    async def delete(
        self,
        db: AsyncSession,
        product_id: uuid.UUID,
        variant_id: uuid.UUID,
    ):
        variant = await self.repository.get_by_id(
            db,
            variant_id,
        )

        if not variant:
            return None

        if variant.product_id != product_id:
            return None

        await self.repository.delete(
            db,
            variant,
        )

        return variant