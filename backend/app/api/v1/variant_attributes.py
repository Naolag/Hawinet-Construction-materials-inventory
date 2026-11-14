import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.variant_attribute import (
    VariantAttributeCreate,
    VariantAttributeResponse,
    VariantAttributeUpdate,
)
from app.services.variant_attribute import VariantAttributeService


router = APIRouter(
    prefix="/variants",
    tags=["Variant Attributes"],
)

service = VariantAttributeService()


@router.post(
    "/{variant_id}/attributes",
    response_model=VariantAttributeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_variant_attribute(
    variant_id: uuid.UUID,
    data: VariantAttributeCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        result = await service.create(
            db,
            variant_id,
            data.attribute_id,
            data.value,
        )

        if result == "variant_not_found":
            raise HTTPException(
                status_code=404,
                detail="Product variant not found",
            )

        if result == "attribute_not_allowed":
            raise HTTPException(
                status_code=409,
                detail="Attribute is not assigned to the product category",
            )

        if result == "attribute_exists":
            raise HTTPException(
                status_code=409,
                detail="Attribute already exists for this variant",
            )

        await db.commit()

        result = await service.repository.get_by_id_with_name(
            db,
            result.variant_attribute_id,
        )

        variant_attribute, attribute_name = result

        return VariantAttributeResponse(
            variant_attribute_id=variant_attribute.variant_attribute_id,
            attribute_id=variant_attribute.attribute,
            attribute_name=attribute_name,
            value=variant_attribute.value,
            is_universal=variant_attribute.is_universal,
            created_at=variant_attribute.created_at,
        )

    except HTTPException:
        await db.rollback()
        raise

    except Exception:
        await db.rollback()
        raise


@router.get(
    "/{variant_id}/attributes",
    response_model=list[VariantAttributeResponse],
)
async def get_variant_attributes(
    variant_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await service.get_all(
        db,
        variant_id,
    )

    if result == "variant_not_found":
        raise HTTPException(
            status_code=404,
            detail="Product variant not found",
        )

    return [
        VariantAttributeResponse(
            variant_attribute_id=variant_attribute.variant_attribute_id,
            attribute_id=variant_attribute.attribute,
            attribute_name=attribute_name,
            value=variant_attribute.value,
            is_universal=variant_attribute.is_universal,
            created_at=variant_attribute.created_at,
        )
        for variant_attribute, attribute_name in result
    ]


@router.patch(
    "/{variant_id}/attributes/{variant_attribute_id}",
    response_model=VariantAttributeResponse,
)
async def update_variant_attribute(
    variant_id: uuid.UUID,
    variant_attribute_id: uuid.UUID,
    data: VariantAttributeUpdate,
    db: AsyncSession = Depends(get_db),
):
    try:
        result = await service.update(
            db,
            variant_id,
            variant_attribute_id,
            data.value,
        )

        if result == "variant_attribute_not_found":
            raise HTTPException(
                status_code=404,
                detail="Variant attribute not found",
            )

        await db.commit()

        result = await service.repository.get_by_id_with_name(
            db,
            result.variant_attribute_id,
        )

        variant_attribute, attribute_name = result

        return VariantAttributeResponse(
            variant_attribute_id=variant_attribute.variant_attribute_id,
            attribute_id=variant_attribute.attribute,
            attribute_name=attribute_name,
            value=variant_attribute.value,
            is_universal=variant_attribute.is_universal,
            created_at=variant_attribute.created_at,
        )

    except HTTPException:
        await db.rollback()
        raise

    except Exception:
        await db.rollback()
        raise


@router.delete(
    "/{variant_id}/attributes/{variant_attribute_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_variant_attribute(
    variant_id: uuid.UUID,
    variant_attribute_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    try:
        result = await service.delete(
            db,
            variant_id,
            variant_attribute_id,
        )

        if not result:
            raise HTTPException(
                status_code=404,
                detail="Variant attribute not found",
            )

        await db.commit()

    except HTTPException:
        await db.rollback()
        raise

    except Exception:
        await db.rollback()
        raise