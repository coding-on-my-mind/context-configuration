"""
Converter for dataclass objects.
TODO check the different possibilities how dataclass objects
can be created and if this class covers all of them.
"""
import inspect
import typing

from dataclasses import dataclass, is_dataclass

from ..protocol import Converter, T


class DataclassConverter(Converter[T]):
    """
    Converter for dataclass objects.

    This converter reads all properties needed for the instantiation of
    such a class from the __init__ method.
    """

    def __init__(self, cls: T):
        if not is_dataclass(cls):
            raise ValueError(f"Expecting class '{cls}' of type dataclass.")
        self._cls = cls

    def for_type(self) -> dataclass:
        return self._cls

    def convert(self, properties) -> dataclass:
        if not isinstance(properties, dict):
            raise ValueError("Given value must be a dict, cannot convert to a dataclass.")

        sig = inspect.signature(self._cls)

        kw_arguments = {}
        for param in sig.parameters.values():
            kw_arguments[param.name] = None
            if param.name not in properties:
                if param.default != inspect.Parameter.empty:
                    properties[param.name] = param.default
                    continue
                if self._is_optional_field(param):
                    continue
                raise ValueError(f"Required key '{param.name}' not found "
                                 f"in configuration parameters.")
            if not isinstance(properties[param.name], param.annotation):
                raise ValueError(f"Required key '{param.name}' is of wrong type "
                                 f"(expected: '{param.annotation}', "
                                 f"given: '{type(properties[param.name])}'.")
            kw_arguments[param.name] = properties[param.name]
        try:
            return self._cls(**kw_arguments)
        except ValueError as e:
            raise ValueError(f"Could not convert '{properties}' to dataclass of "
                             f"type '{self._cls}'.") from e

    def _is_optional_field(self, param: inspect.Parameter) -> bool:
        if param.annotation == typing.Optional[str]:
            return True
        if param.annotation == typing.Optional[int]:
            return True
        return param.annotation == typing.Optional[float]
