import uuid
from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.inventory import InventoryItem, InventoryItemUnit, InventoryTransaction, InventoryTransactionItem
from app.repositories.inventory import InventoryRepository
from app.schemas.inventory import InventoryItemCreate, InventoryItemUnitCreate, InventoryItemUnitUpdate, InventoryTransactionCreate


OUTBOUND_TYPES = {"SALE", "SUPPLIER_RETURN", "ADJUSTMENT_OUT"}
PRICE_TYPE = {"RECEIPT": "purchase_price", "SUPPLIER_RETURN": "purchase_price", "SALE": "selling_price", "CUSTOMER_RETURN": "selling_price"}


class InventoryService:
    def __init__(self):
        self.repository = InventoryRepository()

    async def create_item(self, db: AsyncSession, data: InventoryItemCreate):
        unit = await self.repository.active_unit(db, data.stock_unit_id)
        if not unit:
            return "stock_unit_not_found"

        if data.product_id:
            product = await self.repository.get_product(db, data.product_id)
            if not product:
                return "product_not_found"
            if await self.repository.product_has_variants(db, data.product_id):
                return "product_has_variants"
        else:
            if not await self.repository.get_variant(db, data.product_variant_id):
                return "variant_not_found"

        item = InventoryItem(
            product_id=data.product_id,
            product_variant_id=data.product_variant_id,
            stock_unit_id=data.stock_unit_id,
            is_active=True,
        )
        await self.repository.create_item(db, item)
        base_unit = InventoryItemUnit(
            inventory_item_id=item.inventory_item_id,
            unit_id=data.stock_unit_id,
            conversion_factor=Decimal("1"),
            can_purchase=True,
            can_sell=True,
            is_active=True,
        )
        await self.repository.create_item_unit(db, base_unit)
        return item

    async def list_items(self, db: AsyncSession):
        return await self.repository.list_items(db)

    async def get_item(self, db: AsyncSession, item_id: uuid.UUID):
        return await self.repository.get_item(db, item_id)

    async def add_item_unit(self, db: AsyncSession, item_id: uuid.UUID, data: InventoryItemUnitCreate):
        item = await self.repository.get_item(db, item_id)
        if not item:
            return None
        if not await self.repository.active_unit(db, data.unit_id):
            return "unit_not_found"
        if await self.repository.get_item_unit(db, item_id, data.unit_id):
            return "unit_already_configured"
        row = InventoryItemUnit(inventory_item_id=item_id, **data.model_dump(), is_active=True)
        return await self.repository.create_item_unit(db, row)

    async def list_item_units(self, db: AsyncSession, item_id: uuid.UUID):
        if not await self.repository.get_item(db, item_id):
            return None
        return await self.repository.get_item_units(db, item_id)

    async def update_item_unit(self, db: AsyncSession, item_id: uuid.UUID, unit_id: uuid.UUID, data: InventoryItemUnitUpdate):
        row = await self.repository.get_item_unit(db, item_id, unit_id)
        if not row:
            return None
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(row, field, value)
        if not row.can_purchase and not row.can_sell:
            return "unit_must_have_usage"
        await db.flush()
        await db.refresh(row)
        return row

    async def create_transaction(self, db: AsyncSession, data: InventoryTransactionCreate):
        transaction = InventoryTransaction(
            transaction_type=data.transaction_type,
            transaction_date=data.transaction_date or datetime.now(timezone.utc),
            reference_number=data.reference_number,
            notes=data.notes,
            status="DRAFT",
        )
        await self.repository.create_transaction(db, transaction)

        for line in data.items:
            item = await self.repository.get_item(db, line.inventory_item_id)
            if not item:
                return "inventory_item_not_found"
            configured = await self.repository.get_allowed_unit(db, line.inventory_item_id, line.unit_id)
            if not configured:
                return "unit_not_configured_for_item"

            if data.transaction_type in {"RECEIPT", "CUSTOMER_RETURN", "ADJUSTMENT_IN"} and not configured.can_purchase and data.transaction_type == "RECEIPT":
                return "unit_not_enabled_for_purchase"
            if data.transaction_type == "SALE" and not configured.can_sell:
                return "unit_not_enabled_for_sale"
            if data.transaction_type == "SUPPLIER_RETURN" and not configured.can_purchase:
                return "unit_not_enabled_for_purchase"

            price = line.unit_price
            if price is None:
                price_field = PRICE_TYPE.get(data.transaction_type)
                if price_field:
                    price = getattr(configured, price_field)

            transaction.items.append(InventoryTransactionItem(
                inventory_item_id=line.inventory_item_id,
                unit_id=line.unit_id,
                quantity=line.quantity,
                conversion_factor=configured.conversion_factor,
                unit_price=price,
            ))

        await db.flush()
        return transaction

    async def get_transaction(self, db: AsyncSession, transaction_id: uuid.UUID):
        return await self.repository.get_transaction(db, transaction_id)

    async def list_transactions(self, db: AsyncSession, limit: int, offset: int):
        return await self.repository.list_transactions(db, limit, offset)

    async def post_transaction(self, db: AsyncSession, transaction_id: uuid.UUID):
        transaction = await self.repository.get_transaction(db, transaction_id, lock=True)
        if not transaction:
            return "transaction_not_found"
        if transaction.status != "DRAFT":
            return "transaction_not_draft"
        if not transaction.items:
            return "transaction_empty"

        item_ids = sorted({line.inventory_item_id for line in transaction.items}, key=str)
        locked = await self.repository.lock_items(db, item_ids)
        if len(locked) != len(item_ids):
            return "inventory_item_not_found"

        if transaction.transaction_type in OUTBOUND_TYPES:
            required: dict[uuid.UUID, Decimal] = {}
            for line in transaction.items:
                required[line.inventory_item_id] = required.get(line.inventory_item_id, Decimal("0")) + line.stock_quantity
            for item_id, quantity in required.items():
                available = await self.repository.current_stock(db, item_id)
                if available < quantity:
                    return {"insufficient_stock": str(item_id), "available": str(available), "requested": str(quantity)}

        transaction.status = "POSTED"
        transaction.posted_at = datetime.now(timezone.utc)
        await db.flush()
        return transaction

    async def void_transaction(self, db: AsyncSession, transaction_id: uuid.UUID):
        transaction = await self.repository.get_transaction(db, transaction_id, lock=True)
        if not transaction:
            return "transaction_not_found"
        if transaction.status != "DRAFT":
            return "only_draft_can_be_voided"
        transaction.status = "VOID"
        await db.flush()
        return transaction

    async def list_stock(self, db: AsyncSession):
        return await self.repository.list_stock(db)

    async def report(self, db: AsyncSession, start: datetime, end: datetime):
        return await self.repository.report(db, start, end)
