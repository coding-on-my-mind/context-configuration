"""
Implementation of a PropertySource class based on the
PyYAML class.

Please check the PyYAML documentation for more information.
"""
from pathlib import Path

import yaml

from .abstract_property_source import AbstractPropertySource


class PyYAMLPropertySource(AbstractPropertySource):
    """
    PropertySource class based on a YAML file read by the PyYAML library.
    """

    def __init__(self, filename: Path, encoding: str, order: int = 0) -> None:
        super().__init__(order)
        with open(filename, 'r', encoding=encoding) as file:
            self._properties = yaml.safe_load(file)
