from datetime import datetime

import pytest

from converter.iso_format_datetime_converter import IsoFormatDateTimeConverter


def test_should_return_correct_type():
    # Given
    converter = IsoFormatDateTimeConverter()

    # When
    t = converter.for_type()

    # Then
    assert t == datetime


def test_should_return_correct_converted_value():
    # Given
    converter = IsoFormatDateTimeConverter()

    # When
    iso_date = converter.convert("2020-01-22T03:40:52.812658")

    # Then
    assert iso_date.year == 2020
    assert iso_date.month == 1
    assert iso_date.day == 22
    assert iso_date.hour == 3
    assert iso_date.minute == 40
    assert iso_date.second == 52
    assert iso_date.microsecond == 812658


def test_should_return_raise_value_error_on_invalid_date():
    # Given
    converter = IsoFormatDateTimeConverter()

    # When
    with pytest.raises(ValueError):
        converter.convert("22.01.2020 03:40:52")
