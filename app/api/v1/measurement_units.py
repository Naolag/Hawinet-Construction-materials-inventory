import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.measurement_unit import MeasurementUnitCreate, MeasurementUnitResponse, MeasurementUnitUpdate
from app.services.measurement_unit import MeasurementUnitService

router = APIRouter(prefix="/measurement-units", tags=["Measurement Units"])
service = MeasurementUnitService()


@router.post("", response_model=MeasurementUnitResponse, status_code=status.HTTP_201_CREATED)
async def create_measurement_unit(data: MeasurementUnitCreate, db: AsyncSession = Depends(get_db)):
    try:
        unit = await service.create(db, data)
        if unit == "unit_already_exists":
            raise HTTPException(status_code=409, detail="A measurement unit with this name or symbol already exists")
        if unit == "category_not_found":
            raise HTTPException(status_code=404, detail="Measurement unit category not found")
        await db.commit()
        return unit
    except HTTPException:
        await db.rollback()
        raise
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Measurement unit conflicts with an existing database constraint")
    except Exception:
        await db.rollback()
        raise


@router.get("", response_model=list[MeasurementUnitResponse])
async def get_measurement_units(db: AsyncSession = Depends(get_db)):
    """Return primary units and active uncategorized units for the frontend."""
    return await service.get_all(db)


@router.get("/{unit_id}/alternatives", response_model=list[MeasurementUnitResponse])
async def get_measurement_unit_alternatives(unit_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    units = await service.get_alternatives(db, unit_id)
    if units is None:
        raise HTTPException(status_code=404, detail="Measurement unit not found")
    return units


@router.get("/{unit_id}", response_model=MeasurementUnitResponse)
async def get_measurement_unit(unit_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    unit = await service.get_by_id(db, unit_id)
    if unit is None:
        raise HTTPException(status_code=404, detail="Measurement unit not found")
    return unit


@router.patch("/{unit_id}", response_model=MeasurementUnitResponse)
async def update_measurement_unit(unit_id: uuid.UUID, data: MeasurementUnitUpdate, db: AsyncSession = Depends(get_db)):
    try:
        unit = await service.update(db, unit_id, data)
        if unit is None:
            raise HTTPException(status_code=404, detail="Measurement unit not found")
        if unit == "unit_already_exists":
            raise HTTPException(status_code=409, detail="A measurement unit with this name or symbol already exists")
        if unit == "category_not_found":
            raise HTTPException(status_code=404, detail="Measurement unit category not found")
        await db.commit()
        return unit
    except HTTPException:
        await db.rollback()
        raise
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Measurement unit conflicts with an existing database constraint")
    except Exception:
        await db.rollback()
        raise


@router.delete("/{unit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_measurement_unit(unit_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    try:
        unit = await service.deactivate(db, unit_id)
        if unit is None:
            raise HTTPException(status_code=404, detail="Measurement unit not found")
        await db.commit()
    except HTTPException:
        await db.rollback()
        raise
    except Exception:
        await db.rollback()
        raise
