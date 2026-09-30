import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.product import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)
from app.services.product import ProductService


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)

service = ProductService()


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    data: ProductCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        product = await service.create(
            db,
            data,
        )

        if product == "category_not_found":
            raise HTTPException(
                status_code=404,
                detail="Category not found",
            )

        await db.commit()

        return product

    except HTTPException:
        await db.rollback()
        raise

    except Exception:
        await db.rollback()
        raise


@router.get(
    "",
    response_model=list[ProductResponse],
)
async def get_products(
    db: AsyncSession = Depends(get_db),
):
    return await service.get_all(db)


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
)
async def get_product(
    product_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    product = await service.get_by_id(
        db,
        product_id,
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return product


@router.patch(
    "/{product_id}",
    response_model=ProductResponse,
)
async def update_product(
    product_id: uuid.UUID,
    data: ProductUpdate,
    db: AsyncSession = Depends(get_db),
):
    try:
        product = await service.update(
            db,
            product_id,
            data,
        )

        if product == "product_not_found":
            raise HTTPException(
                status_code=404,
                detail="Product not found",
            )

        if product == "category_not_found":
            raise HTTPException(
                status_code=404,
                detail="Category not found",
            )

        await db.commit()

        return product

    except HTTPException:
        await db.rollback()
        raise

    except Exception:
        await db.rollback()
        raise


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_product(
    product_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    try:
        product = await service.delete(
            db,
            product_id,
        )

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found",
            )

        await db.commit()

    except HTTPException:
        await db.rollback()
        raise

    except Exception:
        await db.rollback()
        raise