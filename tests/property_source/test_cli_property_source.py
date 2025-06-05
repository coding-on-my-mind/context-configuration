import sys
from unittest.mock import patch

import pytest

from src.context_configuration.property_source.cli_property_source import CLIPropertySource


def test_should_return_double_dash_property():
    # When
    with  patch.object(sys, 'argv', ['script_name.py', '--abc=value']):
        property_source = CLIPropertySource()

    # Then
    assert property_source.get_property("abc", str) == "value"


def test_should_return_double_dash_property_with_equal_sign_in_value():
    # When
    with patch.object(sys, 'argv', ['script_name.py', '--abc=random$%=password']):
        property_source = CLIPropertySource()

    # Then
    assert property_source.get_property("abc", str) == "random$%=password"


def test_should_return_double_dash_property_in_two_arguments():
    # When
    with  patch.object(sys, 'argv', ['script_name.py', '--abc', 'value']):
        property_source = CLIPropertySource()

    # Then
    assert property_source.get_property("abc", str) == "value"


def test_should_return_single_dash_property():
    # When
    with  patch.object(sys, 'argv', ['script_name.py', '-abc', 'value']):
        property_source = CLIPropertySource()

    # Then
    assert property_source.get_property("abc", str)


def test_should_ignore_double_dash_property_without_assignment():
    # When
    with  patch.object(sys, 'argv', ['script_name.py', '--abc']):
        property_source = CLIPropertySource()

    # Then
    with pytest.raises(KeyError):
        property_source.get_property("abc", str)


def test_should_ignore_double_dash_property_without_assignment_but_following_args():
    # When
    with  patch.object(sys, 'argv', ['script_name.py', '--abc', '--bcd="some_value"']):
        property_source = CLIPropertySource()

    # Then
    with pytest.raises(KeyError):
        property_source.get_property("abc", str)
    assert property_source.get_property("bcd", str) == "some_value"


def test_should_ignore_single_dash_property_without_assignment():
    # When
    with  patch.object(sys, 'argv', ['script_name.py', '-abc']):
        property_source = CLIPropertySource()

    # Then
    with pytest.raises(KeyError):
        property_source.get_property("abc", str)


def test_should_ignore_single_dash_property_without_assignment_but_following_args():
    # When
    with  patch.object(sys, 'argv', ['script_name.py', '-abc', '-bcd', 'some_value']):
        property_source = CLIPropertySource()

    # Then
    with pytest.raises(KeyError):
        property_source.get_property("abc", str)
    assert property_source.get_property("bcd", str) == "some_value"


def test_should_ignore_invalid_double_dash_assignment():
    # When
    with  patch.object(sys, 'argv', ['script_name.py', '--=value']):
        property_source = CLIPropertySource()

    # Then
    with pytest.raises(KeyError):
        property_source.get_property("abc", str)
