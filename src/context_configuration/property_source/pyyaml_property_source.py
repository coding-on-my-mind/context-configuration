from pathlib import Path

import yaml

from .abstract_property_source import AbstractPropertySource


class PyYAMLPropertySource(AbstractPropertySource):
    """
    PropertySource class based on a YAML file read by the PyYAML library.
    """

    def __init__(self, filename: Path, order: int = 0) -> None:
        super().__init__(order)
        with open(filename, 'r') as file:
            self._properties = yaml.safe_load(file)
