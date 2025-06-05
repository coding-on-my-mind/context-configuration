from enum import EnumMeta
from typing import Any, Callable, Dict

from .. import P


def convert_string(value: Any) -> str:
    return str(value)


def convert_int(value: Any) -> int:
    return int(value)


def convert_float(value: Any) -> float:
    return float(value)


def default_converter() -> Dict[type, Callable]:
    return {
        str: convert_string,
        int: convert_int,
        float: convert_float,
    }


# For duration take isodate.parse_duration('PT1H5M26S')

def convert(value: Any, converter_list: Dict[type, Callable], cls: type[P]) -> P:
    if isinstance(cls, EnumMeta):
        return cls(value)

    for clazz, converter_callable in converter_list.items():
        if clazz == cls:
            try:
                return converter_callable(value)
            except Exception as e:
                raise KeyError(f'Error while trying to convert {value} to {cls.__name__}') from e
    raise KeyError(f"Could not convert property '{value}'to {cls.__name__}, no converter found!")
