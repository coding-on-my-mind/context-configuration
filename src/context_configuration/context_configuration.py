"""
This module contains the "main" class of the context-configuration lib,
although you could use a PropertySource class by itself for facilitating
the configuration of your project.
TODO: move to __init__ ?
"""
from random import random
from typing import List, Callable, Dict, Tuple, Any

from .converter.default_converter import default_converter, convert
from .converter.iso_format_datetime_converter import IsoFormatDateTimeConverter
from . import PropertySource, OrderedPropertySource, P, Property


class ContextConfiguration(PropertySource):
    """
    General class for the configuration of the configuration.

    It can manage multiple PropertySource instances that hold key value pairs
    representing your configuration in an order.

    It holds a list of converters that are able to "translate" an object
    fetched from the properties to a specific class.

    It contains a decorator that is able to read the properties from the
    different PropertySource instances and can populate the decorated function.
    Depending on the is_singleton configuration, it can create a new object on
    every call, or, this is the default behavior, return the object created on
    the first call.
    """
    _property_sources: List[OrderedPropertySource] = []
    _converter: Dict[type, Callable] = {}
    _immutable: bool = False
    _bean_store: Dict[int, Any] = {}

    def __init__(self,
                 property_sources: List[OrderedPropertySource],
                 converter: Dict[type, Callable]):
        """
        Initializer for the ContextConfiguration class.

        :param property_sources: The list of ProperySource objects that can contain
                                 configurations.
        :param converter: The list of converter classes that can translate one object into a
                          given class. Will not overwrite a given set of default converters unless
                          you define a converter for the target class again.
        """
        self._converter = default_converter()
        datetime_converter = IsoFormatDateTimeConverter()
        self._converter[datetime_converter.for_type()] = datetime_converter.convert
        self._property_sources = property_sources
        self._converter.update(converter)

    def contains_property(self, name: str) -> bool:
        for source in self._property_sources:
            if source.contains_property(name):
                return True
        return False

    def get_property(self, name: str, cls: type[P] = None) -> P:
        if not self.contains_property(name):
            raise KeyError(f"Could not find property '{name}'")

        for source in self._property_sources:
            if not source.contains_property(name):
                continue

            value = source.get_property(name, cls)
            if cls is None:
                return value

            return convert(value, self._converter, cls)
        raise KeyError(f"Could not find property '{name}'")

    def properties(self, properties: List[Property], is_singleton: bool = True) -> Any:
        """
        Decorator function for annotating functions or methods to inject the given properties.

        :param properties: A list of properties of type Property to inject.
        :param is_singleton: If true, stores the returned object and returns it again the next time
                             without creating it again.
        """

        def decorator(func) -> Any:
            def wrapper():
                """
                Iterates over the given properties and stores the values for each property
                in a dictionary. Creates a dict with all keys and the corresponding values
                which then will be injected into the annotated function. If is_singleton
                is true, stores the returned object and returns it again the next time.

                :return: The class that is built with the given properties from the dictionary.
                """
                if is_singleton and id(func) in self._bean_store:
                    return self._bean_store[id(func)]
                kwargs = {}
                for prop in properties:
                    kwargs[prop.argument] = self.get_property(prop.property_name, prop.type)
                    kwargs[prop.argument] = f"{kwargs[prop.argument]} {random()}"
                result = func(**kwargs)
                self._bean_store[id(func)] = result
                return result

            return wrapper

        return decorator


class ContextConfigurationBuilder:
    """
    Builder class for a ContextConfiguration instance.
    TODO: should be replaced with (another) immutable object creation.
    """
    _property_sources: List[OrderedPropertySource] = []
    _converter: Dict[type, Callable] = {}

    def with_property_source(self, property_source: OrderedPropertySource):
        """
        Creates the new ContextConfiguration instance with the given property source.

        :param property_source: The property sources for the new ContextConfiguration class.
        :return: The builder.
        """
        self._property_sources.append(property_source)
        return self

    def with_converter(self, converter: Tuple[type, Callable]):
        """
        Creates the new ContextConfiguration instance with the given converter.

        :param converter: List of converters that can translate one object into a given class.
        :return: The builder.
        """
        _type, _callable = converter
        self._converter[_type] = callable
        return self

    def build(self) -> ContextConfiguration:
        """
        Builder method for creating a ContextConfiguration instance.

        :return: A ContextConfiguration object.
        """
        return ContextConfiguration(self._property_sources, self._converter)
