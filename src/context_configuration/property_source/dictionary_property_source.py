"""
Implementation of a PropertySource class based on a dictionary.
"""
from typing import Dict

from .abstract_property_source import AbstractPropertySource


class DictionaryPropertySource(AbstractPropertySource):
    """
    PropertySource class based on simple dictionaries.
    """

    def __init__(self, properties: Dict[str, any], order: int = 0):
        super().__init__(order)
        self._properties = properties
