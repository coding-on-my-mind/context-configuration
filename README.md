# Context Configuration for Python

*This lib is considered to be in an early alpha state*

A simple, but powerful library to manage the configuration of your projects.

## What is the purpose of this library?

Python does not come with an out-of-the-box solution for a seamless configuration handling, 
which might lead to the following problems:

* The configuration of an application is often done in an inconsistent way, e.g., by hard-coding some properties
  and passing some via environment variables.
* The configuration also often changes for the different stages.
  Usually, you want to use different settings in your local environment compared to those in production.
* For testing purposes, credentials are hard-coded into the code, which is highly dangerous in some cases (see also [Binary secret scanning helped us prevent (what might have been) the worst supply chain attack you can imagine][Binary secret scanning helped us prevent (what might have been) the worst supply chain attack you can imagine]).
  These manual configuration changes will then be reversed before the commit to the repository.
  This process can be cumbersome and error-prone.
* Keeping track of the configuration gets messy when you want to deploy your software on different systems, or you 
  want it to work in your development environment as well as on production.

This is where this library wants to help.

## Consistent configurations across different environments reduce "it works on my machine" issues.

This is an example for a workflow that is possible with this library: 
* Create a configuration for each stage: local development, production, QA (e.g. for automated tests), ...
* Start configuring your environment from prod, and overwrite only those values that deviate from this environment in 
  your test or local environment.
* Leave out the credentials from your configuration files, that are commited to a (Git) repository.
* Instead, define a configuration that is excluded from your repository, where you can define credentials and 
  overwrite some settings for the different environments.

## How to start

The first step is to define one or more ```PropertySource``` classes, where each is a source for a single configuration.
You then can create a ```ContextConfiguration``` object that manages your ```PropertySource``` classes.
With such a library, you define a single point for your configuration.
You then can use this dedicated place to fetch the configuration for every property.
This example shows you how it can be used:

```python
from dataclasses import dataclass

from context_configuration import Property
from context_configuration import ContextConfigurationBuilder
from context_configuration import DataclassConverter
from context_configuration import EnvVarsPropertySource


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
# 140188272664753
# 140188272691520
```

# Todos

* implement more converter, e.g., for Durations according to ISO8106
* check the PropertySource for CLI arguments, this might not be fully implemented and not tested on Windows
* Add documentation how to include other configuration classes, e.g., for Spring Cloud Config server, Cloudfoundry configuration, etc.

[Binary secret scanning helped us prevent (what might have been) the worst supply chain attack you can imagine]: https://jfrog.com/blog/leaked-pypi-secret-token-revealed-in-binary-preventing-suppy-chain-attack/
  