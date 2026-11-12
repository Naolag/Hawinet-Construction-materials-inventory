import uuid
from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.schemas.inventory import (
    InventoryItemCreate,
    InventoryItemUnitCreate,
    InventoryTransactionCreate,
)


def test_inventory_item_requires_exactly_one_product_reference():
    with pytest.raises(ValidationError):
        InventoryItemCreate(stock_unit_id=uuid.uuid4())

    with pytest.raises(ValidationError):
        InventoryItemCreate(
            product_id=uuid.uuid4(),
            product_variant_id=uuid.uuid4(),
            stock_unit_id=uuid.uuid4(),
        )


def test_inventory_item_accepts_product_or_variant():
    product_item = InventoryItemCreate(
        product_id=uuid.uuid4(),
        stock_unit_id=uuid.uuid4(),
    )
    variant_item = InventoryItemCreate(
        product_variant_id=uuid.uuid4(),
        stock_unit_id=uuid.uuid4(),
    )
    assert product_item.product_id is not None
    assert variant_item.product_variant_id is not None


def test_inventory_item_unit_requires_positive_conversion_and_usage():
    with pytest.raises(ValidationError):
        InventoryItemUnitCreate(
            unit_id=uuid.uuid4(),
            conversion_factor=Decimal("0"),
            can_purchase=True,
        )
    with pytest.raises(ValidationError):
        InventoryItemUnitCreate(
            unit_id=uuid.uuid4(),
            conversion_factor=Decimal("1"),
        )


def test_transaction_requires_at_least_one_line():
    with pytest.raises(ValidationError):
        InventoryTransactionCreate(
            transaction_type="SALE",
            items=[],
        )


def test_transaction_line_quantity_must_be_positive():
    with pytest.raises(ValidationError):
        InventoryTransactionCreate(
            transaction_type="SALE",
            items=[{
                "inventory_item_id": str(uuid.uuid4()),
                "unit_id": str(uuid.uuid4()),
                "quantity": "0",
            }],
        )


def test_transaction_date_is_not_accepted_from_client():
    with pytest.raises(ValidationError):
        InventoryTransactionCreate(
            transaction_type="SALE",
            transaction_date="2026-11-12T10:00:00Z",
            items=[{
                "inventory_item_id": str(uuid.uuid4()),
                "unit_id": str(uuid.uuid4()),
                "quantity": "2",
            }],
        )


def test_transaction_line_does_not_require_conversion_factor_or_unit_price():
    transaction = InventoryTransactionCreate(
        transaction_type="SALE",
        items=[{
            "inventory_item_id": str(uuid.uuid4()),
            "unit_id": str(uuid.uuid4()),
            "quantity": "2",
        }],
    )
    line = transaction.items[0]
    assert line.quantity == Decimal("2")
    assert line.unit_price is None
    assert not hasattr(line, "conversion_factor")
