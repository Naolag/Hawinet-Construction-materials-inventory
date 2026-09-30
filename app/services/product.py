import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product
from app.repositories.category import CategoryRepository
from app.repositories.product import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:

    def __init__(self):
        self.repository = ProductRepository()
        self.category_repository = CategoryRepository()

    async def create(
        self,
        db: AsyncSession,
        data: ProductCreate,
    ) -> Product | None:

        category = await self.category_repository.get_by_id(
            db,
            data.category_id,
        )

        if not category:
            return None

        product = Product(
            category_id=data.category_id,
            name=data.name.strip() if data.name else None,
            description=data.description,
            is_active=data.is_active,
            quantity=data.quantity,
            price=data.price,
            brand=data.brand,
        )

        return await self.repository.create(
            db,
            product,
        )

    async def get_all(
        self,
        db: AsyncSession,
    ) -> list[Product]:
        return await self.repository.get_all(db)

    async def get_by_id(
        self,
        db: AsyncSession,
        product_id: uuid.UUID,
    ) -> Product | None:
        return await self.repository.get_by_id(
            db,
            product_id,
        )

    async def update(
        self,
        db: AsyncSession,
        product_id: uuid.UUID,
        data: ProductUpdate,
    ) -> Product | None:

        product = await self.repository.get_by_id(
            db,
            product_id,
        )

        if not product:
            return None

        if data.category_id is not None:
            category = await self.category_repository.get_by_id(
                db,
                data.category_id,
            )

            if not category:
                return None

            product.category_id = data.category_id

        if data.name is not None:
            product.name = data.name.strip()

        if data.description is not None:
            product.description = data.description

        if data.is_active is not None:
            product.is_active = data.is_active

        if data.quantity is not None:
            product.quantity = data.quantity

        if data.price is not None:
            product.price = data.price

        if data.brand is not None:
            product.brand = data.brand

        return await self.repository.update(
            db,
            product,
        )

    async def delete(
        self,
        db: AsyncSession,
        product_id: uuid.UUID,
    ) -> Product | None:

        product = await self.repository.get_by_id(
            db,
            product_id,
        )

        if not product:
            return None

        product.is_active = False

        return await self.repository.update(
            db,
            product,
        )