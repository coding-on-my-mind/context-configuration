import os
from unittest import mock

from src.context_configuration.property_source.env_vars_property_source import EnvVarsPropertySource


def test_should_return_property_from_environment():
    # Given
    property_source = EnvVarsPropertySource()

    # When
    with mock.patch.dict(os.environ, {"env_var": "the value"}):
        value = property_source.get_property("env_var", str)

    # Then
    assert value == "the value"
