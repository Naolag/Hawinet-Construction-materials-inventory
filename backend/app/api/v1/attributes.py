import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.attribute import (
    AttributeCreate,
    AttributeResponse,
    AttributeUpdate,
)
from app.services.attribute import AttributeService


router = APIRouter(
    prefix="/attributes",
    tags=["Attributes"],
)

service = AttributeService()


@router.post(
    "",
    response_model=AttributeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_attribute(
    data: AttributeCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        attribute = await service.create(db, data)
        await db.commit()
        return attribute

    except Exception:
        await db.rollback()
        raise


@router.get(
    "",
    response_model=list[AttributeResponse],
)
async def get_attributes(
    db: AsyncSession = Depends(get_db),
):
    return await service.get_all(db)


@router.get(
    "/{attribute_id}",
    response_model=AttributeResponse,
)
async def get_attribute(
    attribute_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    attribute = await service.get_by_id(
        db,
        attribute_id,
    )

    if not attribute:
        raise HTTPException(
            status_code=404,
            detail="Attribute not found",
        )

    return attribute


@router.patch(
    "/{attribute_id}",
    response_model=AttributeResponse,
)
async def update_attribute(
    attribute_id: uuid.UUID,
    data: AttributeUpdate,
    db: AsyncSession = Depends(get_db),
):
    try:
        attribute = await service.update(
            db,
            attribute_id,
            data,
        )

        if not attribute:
            raise HTTPException(
                status_code=404,
                detail="Attribute not found",
            )

        await db.commit()
        return attribute

    except HTTPException:
        await db.rollback()
        raise

    except Exception:
        await db.rollback()
        raise


@router.delete(
    "/{attribute_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_attribute(
    attribute_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    try:
        attribute = await service.delete(
            db,
            attribute_id,
        )

        if not attribute:
            raise HTTPException(
                status_code=404,
                detail="Attribute not found",
            )

        await db.commit()

    except HTTPException:
        await db.rollback()
        raise

    except Exception:
        await db.rollback()
        raise