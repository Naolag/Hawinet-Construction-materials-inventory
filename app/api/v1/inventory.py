import uuid
from datetime import datetime, time, timedelta, timezone
from typing import Literal
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.inventory import (
    InventoryItemCreate, InventoryItemResponse, InventoryItemUnitCreate,
    InventoryItemUnitResponse, InventoryItemUnitUpdate, InventoryReportRow,
    InventoryTransactionCreate, InventoryTransactionResponse, StockBalanceResponse,
)
from app.services.inventory import InventoryService

router = APIRouter(tags=["Inventory"])
service = InventoryService()


def handle_result(value):
    if value == "product_not_found":
        raise HTTPException(404, "Active product not found")
    if value == "variant_not_found":
        raise HTTPException(404, "Active product variant not found")
    if value == "stock_unit_not_found" or value == "unit_not_found":
        raise HTTPException(404, "Active measurement unit not found")
    if value == "product_has_variants":
        raise HTTPException(409, "A product with variants cannot have stock at the parent-product level")
    if value == "unit_already_configured":
        raise HTTPException(409, "This unit is already configured for the inventory item")
    if value == "unit_not_configured_for_item":
        raise HTTPException(422, "The selected unit is not configured for this inventory item")
    if value == "unit_not_enabled_for_purchase":
        raise HTTPException(422, "This unit is not enabled for purchase")
    if value == "unit_not_enabled_for_sale":
        raise HTTPException(422, "This unit is not enabled for sale")
    if value == "unit_must_have_usage":
        raise HTTPException(422, "A unit must be enabled for purchase, sale, or both")
    if value == "inventory_item_not_found":
        raise HTTPException(404, "Active inventory item not found")
    if value == "transaction_not_found":
        raise HTTPException(404, "Inventory transaction not found")
    if value == "transaction_not_draft":
        raise HTTPException(409, "Only draft transactions can be posted")
    if value == "transaction_empty":
        raise HTTPException(422, "An inventory transaction must contain at least one line")
    if value == "only_draft_can_be_voided":
        raise HTTPException(409, "Only draft transactions can be voided")
    if isinstance(value, dict) and "insufficient_stock" in value:
        raise HTTPException(409, detail={
            "message": "Insufficient stock to post this transaction",
            **value,
        })
    return value


@router.post("/inventory-items", response_model=InventoryItemResponse, status_code=201)
async def create_inventory_item(data: InventoryItemCreate, db: AsyncSession = Depends(get_db)):
    try:
        result = handle_result(await service.create_item(db, data))
        await db.commit()
        return result
    except HTTPException:
        await db.rollback()
        raise
    except IntegrityError:
        await db.rollback()
        raise HTTPException(409, "Inventory item already exists or violates a database constraint")
    except Exception:
        await db.rollback()
        raise


@router.get("/inventory-items", response_model=list[InventoryItemResponse])
async def get_inventory_items(db: AsyncSession = Depends(get_db)):
    return await service.list_items(db)


@router.get("/inventory-items/{item_id}", response_model=InventoryItemResponse)
async def get_inventory_item(item_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    item = await service.get_item(db, item_id)
    if not item:
        raise HTTPException(404, "Inventory item not found")
    return item


@router.get("/inventory-items/{item_id}/units", response_model=list[InventoryItemUnitResponse])
async def get_inventory_item_units(item_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await service.list_item_units(db, item_id)
    if result is None:
        raise HTTPException(404, "Inventory item not found")
    return result


@router.post("/inventory-items/{item_id}/units", response_model=InventoryItemUnitResponse, status_code=201)
async def add_inventory_item_unit(item_id: uuid.UUID, data: InventoryItemUnitCreate, db: AsyncSession = Depends(get_db)):
    try:
        result = handle_result(await service.add_item_unit(db, item_id, data))
        await db.commit()
        return result
    except HTTPException:
        await db.rollback()
        raise
    except IntegrityError:
        await db.rollback()
        raise HTTPException(409, "Unit configuration conflicts with an existing database constraint")
    except Exception:
        await db.rollback()
        raise


@router.patch("/inventory-items/{item_id}/units/{unit_id}", response_model=InventoryItemUnitResponse)
async def update_inventory_item_unit(item_id: uuid.UUID, unit_id: uuid.UUID, data: InventoryItemUnitUpdate, db: AsyncSession = Depends(get_db)):
    try:
        result = handle_result(await service.update_item_unit(db, item_id, unit_id, data))
        if result is None:
            raise HTTPException(404, "Configured inventory unit not found")
        await db.commit()
        return result
    except HTTPException:
        await db.rollback()
        raise
    except IntegrityError:
        await db.rollback()
        raise HTTPException(409, "Unit configuration conflicts with an existing database constraint")
    except Exception:
        await db.rollback()
        raise


@router.post("/inventory-transactions", response_model=InventoryTransactionResponse, status_code=201)
async def create_inventory_transaction(data: InventoryTransactionCreate, db: AsyncSession = Depends(get_db)):
    try:
        result = handle_result(await service.create_transaction(db, data))
        await db.commit()
        return result
    except HTTPException:
        await db.rollback()
        raise
    except IntegrityError:
        await db.rollback()
        raise HTTPException(409, "Transaction conflicts with an inventory constraint")
    except Exception:
        await db.rollback()
        raise


@router.get("/inventory-transactions", response_model=list[InventoryTransactionResponse])
async def get_inventory_transactions(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    return await service.list_transactions(db, limit, offset)


@router.get("/inventory-transactions/{transaction_id}", response_model=InventoryTransactionResponse)
async def get_inventory_transaction(transaction_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await service.get_transaction(db, transaction_id)
    if not result:
        raise HTTPException(404, "Inventory transaction not found")
    return result


@router.post("/inventory-transactions/{transaction_id}/post", response_model=InventoryTransactionResponse)
async def post_inventory_transaction(transaction_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    try:
        result = handle_result(await service.post_transaction(db, transaction_id))
        await db.commit()
        return result
    except HTTPException:
        await db.rollback()
        raise
    except IntegrityError:
        await db.rollback()
        raise HTTPException(409, "Could not post transaction because of an inventory constraint")
    except Exception:
        await db.rollback()
        raise


@router.post("/inventory-transactions/{transaction_id}/void", response_model=InventoryTransactionResponse)
async def void_inventory_transaction(transaction_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    try:
        result = handle_result(await service.void_transaction(db, transaction_id))
        await db.commit()
        return result
    except HTTPException:
        await db.rollback()
        raise
    except Exception:
        await db.rollback()
        raise


@router.get("/inventory-stock", response_model=list[StockBalanceResponse])
async def get_inventory_stock(db: AsyncSession = Depends(get_db)):
    return await service.list_stock(db)


@router.get("/inventory-reports/sales", response_model=list[InventoryReportRow])
async def get_inventory_sales_report(
    period: Literal["daily", "weekly", "monthly"] = "daily",
    on_date: datetime | None = None,
    db: AsyncSession = Depends(get_db),
):
    shop_timezone = ZoneInfo("Africa/Addis_Ababa")
    anchor = on_date or datetime.now(shop_timezone)
    if anchor.tzinfo is None:
        anchor = anchor.replace(tzinfo=shop_timezone)
    if period == "daily":
        start = datetime.combine(anchor.date(), time.min, tzinfo=anchor.tzinfo)
        end = start + timedelta(days=1)
    elif period == "weekly":
        start_date = anchor.date() - timedelta(days=anchor.weekday())
        start = datetime.combine(start_date, time.min, tzinfo=anchor.tzinfo)
        end = start + timedelta(days=7)
    else:
        first = anchor.date().replace(day=1)
        start = datetime.combine(first, time.min, tzinfo=anchor.tzinfo)
        if first.month == 12:
            end = start.replace(year=first.year + 1, month=1)
        else:
            end = start.replace(month=first.month + 1)
    rows = await service.report(db, start, end)
    return [dict(row) for row in rows]
