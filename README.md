# Context Configuration for Python

A simple, but powerful library to manage the configuration of your projects.

## What is the purpose of this library?

Usually, the configuration of an application is done in an inconsistent way, e.g., by hard-coding properties or passing them via environment variables.
Hard-coding variables is not recommended in many cases, and even forbidden for credentials when the code will be stored in a versioning system.
Keeping track of the configuration gets messy when you want to deploy your software on different systems, or you want it to work in your development environment as well as on production.

## How to start

The first step is to define a ```PropertySource``` class, which is a source for a single configuration

With this library you define a single point for your configuration.

You then can use this dedicated place to fetch the configuration for every item.

This example shows you how it can be used:

```python
from dataclasses import dataclass

from context_configuration import Property
from context_configuration.context_configuration import ContextConfigurationBuilder
from context_configuration.converter.dataclass_converter import DataclassConverter
from context_configuration.property_source.env_vars_property_source import EnvVarsPropertySource


@dataclass
class Policy:
    name: str
    description: str


dataclass_converter = DataclassConverter(Policy)

conf = (ContextConfigurationBuilder()
            .with_property_source(EnvVarsPropertySource())
            .with_converter((dataclass_converter.for_type(), dataclass_converter.convert))
            .build())


@conf.properties(properties=[
Property("name", "name", str),
Property("description", "description", str),
])
def get_policy_as_singleton(name, description):
    return Policy(name, description)


@conf.properties(properties=[
Property("name", "a", str),
Property("description", "b", str),
], is_singleton=False)
def get_new_policy_on_every_call(name, description):
    return Policy(name, description)


def main():
    print(get_policy_as_singleton())
    print(get_new_policy_on_every_call())
    # Returns the same object on every call
    print(id(get_policy_as_singleton()))
    print(id(get_policy_as_singleton()))
    # Returns a new object on every call
    print(id(get_new_policy_on_every_call()))
    print(id(get_new_policy_on_every_call()))

if __name__ == '__main__':
    main()
  
# ~/context-configuration/> name=the_name description="a description" a=another_name b=another_description .env/bin/python src/example.py
# Policy(name='the_name', description='a description')
# Policy(name='another_name', description='another_description')
# 140188272692432
# 140188272692432
# 140188272692432
# 140188272691520
```
