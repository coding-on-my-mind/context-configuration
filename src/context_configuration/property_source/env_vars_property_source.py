"""
Implementation of a PropertySource class that is reading
the properties from environment variables.
"""
import os
from typing import Any

from .abstract_property_source import AbstractPropertySource


class EnvVarsPropertySource(AbstractPropertySource):
    """
    PropertySource class based on environment variables.
    """

    def _get(self, name: str) -> Any:
        if name not in os.environ:
            raise KeyError(f"Could not find property '{name}'")
        return os.environ[name]
