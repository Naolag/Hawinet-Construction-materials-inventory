import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean, CheckConstraint, Computed, DateTime, ForeignKey, ForeignKeyConstraint,
    Numeric, String, Text, UniqueConstraint, func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class InventoryItem(Base):
    __tablename__ = "inventory_items"
    __table_args__ = (
        CheckConstraint(
            "(product_id IS NOT NULL AND product_variant_id IS NULL) OR "
            "(product_id IS NULL AND product_variant_id IS NOT NULL)",
            name="inventory_item_exactly_one_product_or_variant",
        ),
    )

    inventory_item_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("products.product_id", ondelete="RESTRICT"))
    product_variant_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("product_variants.product_variant_id", ondelete="RESTRICT"))
    stock_unit_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("measurement_units.unit_id", ondelete="RESTRICT"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, server_default="true", nullable=False)

    units = relationship("InventoryItemUnit", back_populates="inventory_item", cascade="all, delete-orphan")
    transaction_items = relationship("InventoryTransactionItem", back_populates="inventory_item")


class InventoryItemUnit(Base):
    __tablename__ = "inventory_item_units"
    __table_args__ = (
        UniqueConstraint("inventory_item_id", "unit_id", name="inventory_item_units_item_unit_key"),
        CheckConstraint("conversion_factor > 0", name="inventory_item_units_conversion_factor_check"),
        CheckConstraint("purchase_price IS NULL OR purchase_price >= 0", name="inventory_item_units_purchase_price_check"),
        CheckConstraint("selling_price IS NULL OR selling_price >= 0", name="inventory_item_units_selling_price_check"),
        CheckConstraint("can_purchase OR can_sell", name="inventory_item_units_purchase_or_sell_check"),
    )

    inventory_item_unit_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    inventory_item_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("inventory_items.inventory_item_id", ondelete="RESTRICT"), nullable=False)
    unit_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("measurement_units.unit_id", ondelete="RESTRICT"), nullable=False)
    conversion_factor: Mapped[Decimal] = mapped_column(Numeric(20, 6), default=1, server_default="1", nullable=False)
    can_purchase: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false", nullable=False)
    can_sell: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false", nullable=False)
    purchase_price: Mapped[Decimal | None] = mapped_column(Numeric(20, 6))
    selling_price: Mapped[Decimal | None] = mapped_column(Numeric(20, 6))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true", nullable=False)

    inventory_item = relationship("InventoryItem", back_populates="units")


class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"
    __table_args__ = (
        CheckConstraint("transaction_type IN ('RECEIPT','SALE','CUSTOMER_RETURN','SUPPLIER_RETURN','ADJUSTMENT_IN','ADJUSTMENT_OUT')", name="inventory_transactions_type_check"),
        CheckConstraint("status IN ('DRAFT','POSTED','VOID')", name="inventory_transactions_status_check"),
        CheckConstraint("(status = 'POSTED' AND posted_at IS NOT NULL) OR (status <> 'POSTED' AND posted_at IS NULL)", name="inventory_transactions_posted_at_check"),
    )

    inventory_transaction_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    transaction_type: Mapped[str] = mapped_column(String(30), nullable=False)
    transaction_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    reference_number: Mapped[str | None] = mapped_column(String)
    notes: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), default="DRAFT", server_default="DRAFT", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    posted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    items = relationship("InventoryTransactionItem", back_populates="transaction", cascade="all, delete-orphan")


class InventoryTransactionItem(Base):
    __tablename__ = "inventory_transaction_items"
    __table_args__ = (
        ForeignKeyConstraint(
            ["inventory_item_id", "unit_id"],
            ["inventory_item_units.inventory_item_id", "inventory_item_units.unit_id"],
            name="inventory_transaction_item_allowed_unit_fkey",
            ondelete="RESTRICT",
        ),
        CheckConstraint("quantity > 0", name="inventory_transaction_items_quantity_check"),
        CheckConstraint("conversion_factor > 0", name="inventory_transaction_items_conversion_factor_check"),
        CheckConstraint("unit_price IS NULL OR unit_price >= 0", name="inventory_transaction_items_unit_price_check"),
    )

    transaction_item_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    inventory_transaction_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("inventory_transactions.inventory_transaction_id", ondelete="RESTRICT"), nullable=False)
    inventory_item_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("inventory_items.inventory_item_id", ondelete="RESTRICT"), nullable=False)
    unit_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("measurement_units.unit_id", ondelete="RESTRICT"), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(20, 6), nullable=False)
    conversion_factor: Mapped[Decimal] = mapped_column(Numeric(20, 6), nullable=False)
    stock_quantity: Mapped[Decimal] = mapped_column(Numeric(20, 6), Computed("quantity * conversion_factor", persisted=True))
    unit_price: Mapped[Decimal | None] = mapped_column(Numeric(20, 6))
    line_total: Mapped[Decimal | None] = mapped_column(Numeric(30, 6), Computed("quantity * unit_price", persisted=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    transaction = relationship("InventoryTransaction", back_populates="items")
    inventory_item = relationship("InventoryItem", back_populates="transaction_items")
