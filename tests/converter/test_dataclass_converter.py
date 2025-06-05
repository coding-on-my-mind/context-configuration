from typing import Optional

import pytest
from dataclasses import dataclass, is_dataclass

from src.context_configuration.converter import DataclassConverter


@dataclass
class RegularTestDataclass:
    field_str: str
    field_int: int
    field_float: float


@dataclass
class OptionalTestDataclass:
    field_str: Optional[str]
    field_int: Optional[int]
    field_float: Optional[float]


@dataclass
class DefaultValueTestDataclass:
    field_str = "default string"
    field_int = -1
    field_float = 3.2


def test_should_return_correct_type():
    # Given
    converter = DataclassConverter(RegularTestDataclass)

    # When
    t = converter.for_type()

    # Then
    assert is_dataclass(t)


def test_should_raise_exception_on_invalid_type_of_class():
    # When
    with pytest.raises(ValueError):
        DataclassConverter(DataclassConverter)


def test_should_return_correct_converted_value():
    # Given
    converter = DataclassConverter(RegularTestDataclass)

    # When
    test_dataclass = converter.convert({
        "field_str": "a string",
        "field_int": 20,
        "field_float": 3.2,
    })

    # Then
    assert test_dataclass.__class__ == RegularTestDataclass
    assert test_dataclass.field_str == "a string"
    assert test_dataclass.field_int == 20
    # TODO Sonar compare floating point values
    assert test_dataclass.field_float == 3.2


def test_should_return_correct_converted_value_with_optional_fields():
    # Given
    converter = DataclassConverter(OptionalTestDataclass)

    # When
    test_dataclass = converter.convert({})

    # Then
    assert test_dataclass.__class__ == OptionalTestDataclass
    assert test_dataclass.field_str is None
    assert test_dataclass.field_int is None
    assert test_dataclass.field_float is None


def test_should_return_correct_converted_value_with_default_fields():
    # Given
    converter = DataclassConverter(DefaultValueTestDataclass)

    # When
    test_dataclass = converter.convert({})

    # Then
    assert test_dataclass.__class__ == DefaultValueTestDataclass
    assert test_dataclass.field_str == "default string"
    assert test_dataclass.field_int == -1
    # TODO Sonar compare floating point values
    assert test_dataclass.field_float == 3.2


def test_should_return_raise_value_error_on_invalid_type():
    # Given
    converter = DataclassConverter(RegularTestDataclass)

    # When
    with pytest.raises(ValueError):
        converter.convert("not a dictionary")


def test_should_return_raise_value_error_on_missing_key():
    # Given
    converter = DataclassConverter(RegularTestDataclass)

    # When
    with pytest.raises(ValueError):
        converter.convert({
            "field_str": "float value is missing",
            "field_int": 20,
        })


def test_should_return_raise_value_error_on_invalid_type_of_key():
    # Given
    converter = DataclassConverter(RegularTestDataclass)

    # When
    with pytest.raises(ValueError):
        converter.convert({
            "field_str": "float value is missing",
            "field_int": 20,
            "field_float": "string is not a float",
        })
