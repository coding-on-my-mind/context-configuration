from collections import namedtuple
from typing import Protocol, TypeVar, Any

T = TypeVar('T')
P = TypeVar('P')

Property = namedtuple('Property', ['argument', 'property_name', 'type'])


class Converter(Protocol[T]):

    def for_type(self) -> T:
        ...

    def convert(self, properties: Any) -> T:
        ...


class PropertySource(Protocol):

    def contains_property(self, name: str) -> bool: ...

    def get_property(self, name: str, cls: type[P]) -> P: ...


class OrderedPropertySource(PropertySource):

    def get_order(self) -> int: ...


from .converter import DataclassConverter, IsoFormatDateTimeConverter
from .property_source import AbstractPropertySource, CLIPropertySource, DictionaryPropertySource, EnvVarsPropertySource, \
    PyYAMLPropertySource

__all__ = (
    DataclassConverter,
    IsoFormatDateTimeConverter,
    AbstractPropertySource,
    CLIPropertySource,
    DictionaryPropertySource,
    EnvVarsPropertySource,
    PyYAMLPropertySource,
)
