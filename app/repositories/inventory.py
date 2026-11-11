import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import case, func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.inventory import InventoryItem, InventoryItemUnit, InventoryTransaction, InventoryTransactionItem
from app.models.measurement_unit import MeasurementUnit
from app.models.product import Product
from app.models.product_variant import ProductVariant


class InventoryRepository:
    async def get_item(self, db: AsyncSession, item_id: uuid.UUID, active_only: bool = True):
        query = select(InventoryItem).where(InventoryItem.inventory_item_id == item_id)
        if active_only:
            query = query.where(InventoryItem.is_active.is_(True))
        return (await db.execute(query)).scalar_one_or_none()

    async def list_items(self, db: AsyncSession):
        result = await db.execute(select(InventoryItem).where(InventoryItem.is_active.is_(True)).order_by(InventoryItem.created_at.desc()))
        return list(result.scalars().all())

    async def get_product(self, db: AsyncSession, product_id: uuid.UUID):
        return (await db.execute(select(Product).where(Product.product_id == product_id, Product.is_active.is_(True)))).scalar_one_or_none()

    async def get_variant(self, db: AsyncSession, variant_id: uuid.UUID):
        result = await db.execute(
            select(ProductVariant).join(Product, Product.product_id == ProductVariant.product_id)
            .where(ProductVariant.product_variant_id == variant_id, Product.is_active.is_(True))
        )
        return result.scalar_one_or_none()

    async def product_has_variants(self, db: AsyncSession, product_id: uuid.UUID) -> bool:
        result = await db.execute(select(ProductVariant.product_variant_id).where(ProductVariant.product_id == product_id).limit(1))
        return result.scalar_one_or_none() is not None

    async def active_unit(self, db: AsyncSession, unit_id: uuid.UUID):
        return (await db.execute(select(MeasurementUnit).where(MeasurementUnit.unit_id == unit_id, MeasurementUnit.is_active.is_(True)))).scalar_one_or_none()

    async def create_item(self, db: AsyncSession, item: InventoryItem):
        db.add(item)
        await db.flush()
        await db.refresh(item)
        return item

    async def get_item_units(self, db: AsyncSession, item_id: uuid.UUID):
        result = await db.execute(
            select(InventoryItemUnit).where(
                InventoryItemUnit.inventory_item_id == item_id,
                InventoryItemUnit.is_active.is_(True),
            ).order_by(InventoryItemUnit.created_at)
        )
        return list(result.scalars().all())

    async def get_item_unit(self, db: AsyncSession, item_id: uuid.UUID, unit_id: uuid.UUID):
        result = await db.execute(select(InventoryItemUnit).where(
            InventoryItemUnit.inventory_item_id == item_id,
            InventoryItemUnit.unit_id == unit_id,
            InventoryItemUnit.is_active.is_(True),
        ))
        return result.scalar_one_or_none()

    async def create_item_unit(self, db: AsyncSession, row: InventoryItemUnit):
        db.add(row)
        await db.flush()
        await db.refresh(row)
        return row

    async def lock_items(self, db: AsyncSession, item_ids: list[uuid.UUID]):
        result = await db.execute(
            select(InventoryItem)
            .where(InventoryItem.inventory_item_id.in_(item_ids), InventoryItem.is_active.is_(True))
            .order_by(InventoryItem.inventory_item_id)
            .with_for_update()
        )
        return list(result.scalars().all())

    async def current_stock(self, db: AsyncSession, item_id: uuid.UUID) -> Decimal:
        result = await db.execute(
            text("SELECT current_stock FROM public.inventory_stock_balances WHERE inventory_item_id = :item_id"),
            {"item_id": str(item_id)},
        )
        value = result.scalar_one_or_none()
        return value if value is not None else Decimal("0")

    async def create_transaction(self, db: AsyncSession, transaction: InventoryTransaction):
        db.add(transaction)
        await db.flush()
        return transaction

    async def get_transaction(self, db: AsyncSession, transaction_id: uuid.UUID, lock: bool = False):
        query = select(InventoryTransaction).where(
            InventoryTransaction.inventory_transaction_id == transaction_id
        )
        if lock:
            query = query.with_for_update()
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def list_transactions(self, db: AsyncSession, limit: int = 100, offset: int = 0):
        result = await db.execute(
            select(InventoryTransaction)
            .order_by(InventoryTransaction.transaction_date.desc())
            .limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def get_allowed_unit(self, db: AsyncSession, item_id: uuid.UUID, unit_id: uuid.UUID):
        result = await db.execute(
            select(InventoryItemUnit).where(
                InventoryItemUnit.inventory_item_id == item_id,
                InventoryItemUnit.unit_id == unit_id,
                InventoryItemUnit.is_active.is_(True),
            )
        )
        return result.scalar_one_or_none()

    async def list_stock(self, db: AsyncSession):
        result = await db.execute(text(
            "SELECT inventory_item_id, product_id, product_variant_id, stock_unit_id, current_stock "
            "FROM public.inventory_stock_balances ORDER BY inventory_item_id"
        ))
        return result.mappings().all()

    async def report(self, db: AsyncSession, start: datetime, end: datetime):
        result = await db.execute(text("""
            SELECT ii.inventory_item_id, ii.product_id, ii.product_variant_id, ii.stock_unit_id,
                   COALESCE(SUM(ti.stock_quantity) FILTER (
                       WHERE t.status = 'POSTED' AND t.transaction_type = 'SALE'
                         AND t.transaction_date >= :start_at AND t.transaction_date < :end_at
                   ), 0) AS sold_quantity,
                   COALESCE(b.current_stock, 0) AS current_stock
            FROM public.inventory_items ii
            LEFT JOIN public.inventory_transaction_items ti ON ti.inventory_item_id = ii.inventory_item_id
            LEFT JOIN public.inventory_transactions t ON t.inventory_transaction_id = ti.inventory_transaction_id
            LEFT JOIN public.inventory_stock_balances b ON b.inventory_item_id = ii.inventory_item_id
            WHERE ii.is_active = true
            GROUP BY ii.inventory_item_id, ii.product_id, ii.product_variant_id, ii.stock_unit_id, b.current_stock
            ORDER BY ii.inventory_item_id
        """), {"start_at": start, "end_at": end})
        return result.mappings().all()
