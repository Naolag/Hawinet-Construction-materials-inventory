import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.product_variant import (
    ProductVariantResponse,
)
from app.services.variant import VariantService


router = APIRouter(
    prefix="/products",
    tags=["Product Variants"],
)

service = VariantService()


@router.post(
    "/{product_id}/variants",
    response_model=ProductVariantResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_variant(
    product_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    try:
        variant = await service.create(
            db,
            product_id,
        )

        if variant == "product_not_found":
            raise HTTPException(
                status_code=404,
                detail="Product not found",
            )

        await db.commit()

        return variant

    except HTTPException:
        await db.rollback()
        raise

    except Exception:
        await db.rollback()
        raise


@router.get(
    "/{product_id}/variants",
    response_model=list[ProductVariantResponse],
)
async def get_product_variants(
    product_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    variants = await service.get_by_product(
        db,
        product_id,
    )

    if variants == "product_not_found":
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )
    if variants == "product_inactive":
        raise HTTPException(
            status_code=409,
            detail="Cannot create a variant for an inactive product",
    )

    return variants


@router.get(
    "/{product_id}/variants/{variant_id}",
    response_model=ProductVariantResponse,
)
async def get_variant(
    product_id: uuid.UUID,
    variant_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    variant = await service.get_by_id(
        db,
        product_id,
        variant_id,
    )

    if not variant:
        raise HTTPException(
            status_code=404,
            detail="Product variant not found",
        )

    return variant


@router.delete(
    "/{product_id}/variants/{variant_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_variant(
    product_id: uuid.UUID,
    variant_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    try:
        variant = await service.delete(
            db,
            product_id,
            variant_id,
        )

        if not variant:
            raise HTTPException(
                status_code=404,
                detail="Product variant not found",
            )

        await db.commit()

    except HTTPException:
        await db.rollback()
        raise

    except Exception:
        await db.rollback()
        raise