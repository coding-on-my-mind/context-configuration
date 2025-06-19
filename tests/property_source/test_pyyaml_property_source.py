import os
from pathlib import Path

from src.context_configuration.property_source.pyyaml_property_source import PyYAMLPropertySource

PYYAML_TEST_FILE = Path(os.path.dirname(__file__)).joinpath('data').joinpath('pyyaml_test_properties.yaml')


def test_should_return_correct_value_from_property_without_conversion():
    # Given
    property_source = PyYAMLPropertySource(PYYAML_TEST_FILE)

    # When
    value = property_source.get_property("key_1.key_2")

    # Then
    assert value == "the value"
