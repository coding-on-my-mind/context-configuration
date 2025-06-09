"""
Basic protocols used for the context-configuration library.

You can define your own objects to work as you see fit.
"""
from collections import namedtuple
from typing import Protocol, TypeVar, Any

T = TypeVar('T')
P = TypeVar('P')

Property = namedtuple('Property', ['argument', 'property_name', 'type'])

class PropertySource(Protocol):
    """
    Class containing a set of objects that can be referenced by a key.
    """

    def contains_property(self, name: str) -> bool:
        """
        Checks if a given property is available.

        :param name: The key to the object.
        :return: The object assigned to the property.
        """

    def get_property(self, name: str, cls: type[P] = None) -> P:
        """
        Returns an object assigned to the property.

        :param name: The key to the object.
        :param cls: Optional value for the class the returned object should be of.
        :return: The object assigned to the property.
        """


class OrderedPropertySource(PropertySource):
    """
    Protocol for a property source that has the option to get the order in a given set.
    """

    def get_order(self) -> int:
        """
        Returns an integer to make an ordering of PropertySource instances possible.

        :return: The order within a list of PropertySource instances.
        """


class Converter(Protocol[T]):
    """
    Protocol for converters.

    Converters translate on object to a given type of class, if possible.
    """

    def for_type(self) -> T:
        """
        Getter for the type after the conversion.

        :return: The type after the conversion.
        """

    def convert(self, properties: Any) -> T:
        """
        Converts the property object to the type T.

        :param properties: The properties object.
        :return: The object after the conversion.
        """
