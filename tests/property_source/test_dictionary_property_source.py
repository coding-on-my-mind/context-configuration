from datetime import datetime
from uuid import UUID, uuid4

import pytest

from src.context_configuration.converter.iso_format_datetime_converter import IsoFormatDateTimeConverter
from src.context_configuration.property_source.dictionary_property_source import DictionaryPropertySource


def test_should_raise_key_error_on_empty_key():
    # Given
    property_source = DictionaryPropertySource({
        "a": uuid4()
    })

    # When
    with pytest.raises(KeyError):
        property_source.get_property("")


def test_should_raise_key_error_on_key_starting_with_dot():
    # Given
    property_source = DictionaryPropertySource({
        "a": uuid4()
    })

    # When
    with pytest.raises(KeyError):
        property_source.get_property(".a")


def test_should_raise_key_error_on_key_ending_with_dot():
    # Given
    property_source = DictionaryPropertySource({
        "a": uuid4()
    })

    # When
    with pytest.raises(KeyError):
        property_source.get_property("a.")


def test_should_raise_key_error_on_invalid_key():
    # Given
    property_source = DictionaryPropertySource({
        "a": uuid4()
    })

    # When
    with pytest.raises(KeyError):
        property_source.get_property("a..b")


def test_should_return_correct_value_from_property_without_conversion():
    # Given
    property_source = DictionaryPropertySource({
        "a": uuid4()
    })

    # When
    value = property_source.get_property("a")

    # Then
    assert isinstance(value, UUID)


def test_should_return_correct_int_type():
    # Given
    property_source = DictionaryPropertySource({
        "a": 1
    })

    # When
    value = property_source.get_property("a", int)

    # Then
    assert isinstance(value, int)
    assert value == 1


def test_should_return_correct_converted_int_type():
    # Given
    property_source = DictionaryPropertySource({
        "a": "1"
    })

    # When
    value = property_source.get_property("a", int)

    # Then
    assert isinstance(value, int)
    assert value == 1


def test_should_return_correct_string_type():
    # Given
    property_source = DictionaryPropertySource({
        "a": "value"
    })

    # When
    value = property_source.get_property("a", str)

    # Then
    assert isinstance(value, str)
    assert value == "value"


def test_should_return_correct_converted_string_type():
    # Given
    uuid_value = uuid4()
    property_source = DictionaryPropertySource({
        "a": uuid_value
    })

    # When
    value = property_source.get_property("a", str)

    # Then
    assert isinstance(value, str)
    assert value == str(uuid_value)


def test_should_return_correct_float_type():
    # Given
    property_source = DictionaryPropertySource({
        "a": 2.1
    })

    # When
    value = property_source.get_property("a", float)

    # Then
    assert isinstance(value, float)
    assert value == 2.1


def test_should_return_correct_converted_float_type():
    # Given
    property_source = DictionaryPropertySource({
        "a": "2.1"
    })

    # When
    value = property_source.get_property("a", float)

    # Then
    assert isinstance(value, float)
    assert value == 2.1


def test_should_return_correct_value_after_recursion():
    # Given
    property_source = DictionaryPropertySource({
        "a": {
            "b": {
                "c": "value"
            }
        }
    })

    # When
    value = property_source.get_property("a.b.c")

    # Then
    assert value == "value"


def test_should_return_correct_map_value_after_recursion():
    # Given
    property_source = DictionaryPropertySource({
        "a": {
            "b": {
                "c": {
                    "d": "value"
                }
            }
        }
    })

    # When
    value = property_source.get_property("a.b.c")

    # Then
    assert value == {"d": "value"}


def test_should_return_correct_converted_datetime():
    # Given
    property_source = DictionaryPropertySource({
        "a": "2020-01-22T03:40:52.812658"
    })
    property_source.add_converter(IsoFormatDateTimeConverter())

    # When
    value = property_source.get_property("a", datetime)

    # Then
    assert isinstance(value, datetime)
    assert value.year == 2020
