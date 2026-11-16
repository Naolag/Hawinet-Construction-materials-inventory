import pytest
from pydantic import ValidationError

from app.schemas.measurement_unit import (
    MeasurementUnitCreate,
    MeasurementUnitUpdate,
)


def test_create_strips_name_and_symbol():
    unit = MeasurementUnitCreate(name="  Kilogram  ", symbol=" kg ")

    assert unit.name == "Kilogram"
    assert unit.symbol == "kg"


@pytest.mark.parametrize(
    ("payload", "field"),
    [
        ({"name": "   ", "symbol": "kg"}, "name"),
        ({"name": "Kilogram", "symbol": "  "}, "symbol"),
    ],
)
def test_create_rejects_blank_values(payload, field):
    with pytest.raises(ValidationError) as error:
        MeasurementUnitCreate(**payload)

    assert field in str(error.value)


def test_update_rejects_empty_payload():
    with pytest.raises(ValidationError):
        MeasurementUnitUpdate()


def test_update_rejects_explicit_null_values():
    with pytest.raises(ValidationError):
        MeasurementUnitUpdate(name=None)


def test_update_accepts_one_field_and_trims_it():
    unit = MeasurementUnitUpdate(symbol="  KG ")

    assert unit.symbol == "KG"
    assert unit.name is None


def test_create_rejects_values_over_database_limits():
    with pytest.raises(ValidationError):
        MeasurementUnitCreate(name="n" * 101, symbol="kg")

    with pytest.raises(ValidationError):
        MeasurementUnitCreate(name="Kilogram", symbol="s" * 21)
