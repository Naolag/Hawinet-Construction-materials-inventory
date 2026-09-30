import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.category_attribute import (
    CategoryAttributeCreate,
    CategoryAttributeResponse,
)
from app.services.category_attribute import CategoryAttributeService


router = APIRouter(
    prefix="/categories",
    tags=["Category Attributes"],
)

service = CategoryAttributeService()


@router.get(
    "/{category_id}/attributes",
    response_model=list[CategoryAttributeResponse],
)
async def get_category_attributes(
    category_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    attributes = await service.get_attributes(
        db,
        category_id,
    )

    if attributes is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    return attributes


@router.post(
    "/{category_id}/attributes",
    response_model=CategoryAttributeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_category_attribute(
    category_id: uuid.UUID,
    data: CategoryAttributeCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        result = await service.add_attribute(
            db,
            category_id,
            data.attribute_id,
        )

        if result == "category_not_found":
            raise HTTPException(
                status_code=404,
                detail="Category not found",
            )

        if result == "attribute_not_found":
            raise HTTPException(
                status_code=404,
                detail="Attribute not found",
            )

        if result == "relationship_exists":
            raise HTTPException(
                status_code=409,
                detail="Attribute is already assigned to this category",
            )

        await db.commit()

        attribute = await service.attribute_repository.get_by_id(
            db,
            data.attribute_id,
        )

        return attribute

    except HTTPException:
        await db.rollback()
        raise

    except Exception:
        await db.rollback()
        raise


@router.delete(
    "/{category_id}/attributes/{attribute_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_category_attribute(
    category_id: uuid.UUID,
    attribute_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    try:
        relationship = await service.remove_attribute(
            db,
            category_id,
            attribute_id,
        )

        if not relationship:
            raise HTTPException(
                status_code=404,
                detail="Category attribute relationship not found",
            )

        await db.commit()

    except HTTPException:
        await db.rollback()
        raise

    except Exception:
        await db.rollback()
        raise