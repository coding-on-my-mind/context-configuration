from enum import EnumMeta
from typing import Any, Callable, Dict

from .. import P


def convert_string(value: Any) -> str:
    """
    Simple function to convert an object to a string.

    :param value: Any object that can be converted to a string.
    :return: The string representation of the object.
    """
    return str(value)


def convert_int(value: Any) -> int:
    """
    Simple function to convert an object to an integer.

    :param value: Any object that can be converted to an integer.
    :return: The integer representation of the object.
    """
    return int(value)


def convert_float(value: Any) -> float:
    """
    Simple function to convert an object to a floating point number.

    :param value: Any object that can be converted to a floating point number.
    :return: The floating point number representation of the object.
    """
    return float(value)


def default_converter() -> Dict[type, Callable]:
    """
    The built-in converter.

    :return: Dictionary with default converters like strings, integers, etc.
    """
    return {
        str: convert_string,
        int: convert_int,
        float: convert_float,
    }


# For duration take isodate.parse_duration('PT1H5M26S')

def convert(value: Any, converter_list: Dict[type, Callable], cls: type[P]) -> P:
    """
    Converts the given value to the given type.

    :param value: The value that we want to convert.
    :param converter_list: A list of converters we iterate through.
    :param cls: The class of the converted value.
    :return: The converted value.
    """
    # First, we check if we can convert the value to an Enum.
    if isinstance(cls, EnumMeta):
        return cls(value)

    for clazz, converter_callable in converter_list.items():
        if clazz == cls:
            try:
                return converter_callable(value)
            except Exception as e:
                raise KeyError(f"Error while trying to convert '{value}' to '{cls.__name__}'.") from e

    raise KeyError(f"Could not convert property '{value}'to {cls.__name__}, no converter found!")
