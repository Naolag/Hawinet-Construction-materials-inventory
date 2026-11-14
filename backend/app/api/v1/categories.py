import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)
from app.services.category import CategoryService


router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)

service = CategoryService()


@router.post(
    "",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        category = await service.create(db, data)
        await db.commit()
        return category
    except Exception:
        await db.rollback()
        raise


@router.get(
    "",
    response_model=list[CategoryResponse],
)
async def get_categories(
    db: AsyncSession = Depends(get_db),
):
    return await service.get_all(db)


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
)
async def get_category(
    category_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    category = await service.get_by_id(db, category_id)

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    return category

@router.patch(
    "/{category_id}",
    response_model=CategoryResponse,
)
async def update_category(
    category_id: uuid.UUID,
    data: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
):
    try:
        category = await service.update(
            db,
            category_id,
            data,
        )

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found",
            )

        await db.commit()
        return category

    except HTTPException:
        await db.rollback()
        raise

    except Exception:
        await db.rollback()
        raise


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_category(
    category_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    try:
        category = await service.delete(
            db,
            category_id,
        )

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found",
            )

        await db.commit()

    except HTTPException:
        await db.rollback()
        raise

    except Exception:
        await db.rollback()
        raise