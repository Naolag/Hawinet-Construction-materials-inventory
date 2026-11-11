import uuid
from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class InventoryItemCreate(BaseModel):
    product_id: uuid.UUID | None = None
    product_variant_id: uuid.UUID | None = None
    stock_unit_id: uuid.UUID

    @model_validator(mode="after")
    def exactly_one_reference(self):
        if (self.product_id is None) == (self.product_variant_id is None):
            raise ValueError("Provide exactly one of product_id or product_variant_id")
        return self


class InventoryItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    inventory_item_id: uuid.UUID
    product_id: uuid.UUID | None
    product_variant_id: uuid.UUID | None
    stock_unit_id: uuid.UUID
    created_at: datetime
    is_active: bool


class InventoryItemUnitCreate(BaseModel):
    unit_id: uuid.UUID
    conversion_factor: Decimal = Field(gt=0, max_digits=20, decimal_places=6)
    can_purchase: bool = False
    can_sell: bool = False
    purchase_price: Decimal | None = Field(default=None, ge=0, max_digits=20, decimal_places=6)
    selling_price: Decimal | None = Field(default=None, ge=0, max_digits=20, decimal_places=6)

    @model_validator(mode="after")
    def unit_has_a_use(self):
        if not self.can_purchase and not self.can_sell:
            raise ValueError("A unit must be enabled for purchase, sale, or both")
        return self


class InventoryItemUnitUpdate(BaseModel):
    conversion_factor: Decimal | None = Field(default=None, gt=0, max_digits=20, decimal_places=6)
    can_purchase: bool | None = None
    can_sell: bool | None = None
    purchase_price: Decimal | None = Field(default=None, ge=0, max_digits=20, decimal_places=6)
    selling_price: Decimal | None = Field(default=None, ge=0, max_digits=20, decimal_places=6)


class InventoryItemUnitResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    inventory_item_unit_id: uuid.UUID
    inventory_item_id: uuid.UUID
    unit_id: uuid.UUID
    conversion_factor: Decimal
    can_purchase: bool
    can_sell: bool
    purchase_price: Decimal | None
    selling_price: Decimal | None
    created_at: datetime
    is_active: bool


TransactionType = Literal["RECEIPT", "SALE", "CUSTOMER_RETURN", "SUPPLIER_RETURN", "ADJUSTMENT_IN", "ADJUSTMENT_OUT"]


class TransactionLineCreate(BaseModel):
    inventory_item_id: uuid.UUID
    unit_id: uuid.UUID
    quantity: Decimal = Field(gt=0, max_digits=20, decimal_places=6)
    unit_price: Decimal | None = Field(default=None, ge=0, max_digits=20, decimal_places=6)


class InventoryTransactionCreate(BaseModel):
    transaction_type: TransactionType
    transaction_date: datetime | None = None
    reference_number: str | None = Field(default=None, max_length=255)
    notes: str | None = None
    items: list[TransactionLineCreate] = Field(min_length=1)


class InventoryTransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    inventory_transaction_id: uuid.UUID
    transaction_type: str
    transaction_date: datetime
    reference_number: str | None
    notes: str | None
    status: str
    created_at: datetime
    posted_at: datetime | None
    items: list["InventoryTransactionItemResponse"] = Field(default_factory=list)


class InventoryTransactionItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    transaction_item_id: uuid.UUID
    inventory_transaction_id: uuid.UUID
    inventory_item_id: uuid.UUID
    unit_id: uuid.UUID
    quantity: Decimal
    conversion_factor: Decimal
    stock_quantity: Decimal
    unit_price: Decimal | None
    line_total: Decimal | None
    created_at: datetime


class StockBalanceResponse(BaseModel):
    inventory_item_id: uuid.UUID
    product_id: uuid.UUID | None
    product_variant_id: uuid.UUID | None
    stock_unit_id: uuid.UUID
    current_stock: Decimal


class InventoryReportRow(BaseModel):
    inventory_item_id: uuid.UUID
    product_id: uuid.UUID | None
    product_variant_id: uuid.UUID | None
    stock_unit_id: uuid.UUID
    sold_quantity: Decimal
    current_stock: Decimal
