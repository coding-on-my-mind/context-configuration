# Context Configuration for Python

A simple, but powerful library to manage the configuration of your projects.

## What is the purpose of this library?

* Usually, the configuration of an application is done in an inconsistent way, e.g., by hard-coding some properties
  and passing some via environment variables.
* Often, the configuration changes for the different stages, on your local environment you want to use
  different settings than in production. These configuration changes will then be updated to the prod
  settings before the commit to the repository. This is cumbersome and error-prone.
* Do not hard code URLs, files, etc. Instead, move the configuration into configuration files.
* Hard-coding credentials is highly dangerous in many cases (see also [Binary secret scanning helped us prevent (what might have been) the worst supply chain attack you can imagine][Binary secret scanning helped us prevent (what might have been) the worst supply chain attack you can imagine]),
  and even forbidden for credentials when the code will be stored in a versioning system.
* Keeping track of the configuration gets messy when you want to deploy your software on different systems, or you 
  want it to work in your development environment as well as on production.

## Consistent configurations across different environments reduce "it works on my machine" issues.

This is an example for a workflow that is possible with this library: 
* Create a configuration for each stage: local development, production, QA (e.g. for automated tests), ...
* Start configuring your environment from prod, and overwrite only those values that deviate from this environment in 
  your test or local environment.
* Leave out the credentials from your configuration files, that are commited to a (Git) repository.
* Instead, define a configuration that is excluded from your repository, where you can define credentials and 
  overwrite some settings.

## How to start

The first step is to define one or more ```PropertySource``` classes, where each is a source for a single configuration.
With such a library you define a single point for your configuration.
You then can use this dedicated place to fetch the configuration every item.
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

[Binary secret scanning helped us prevent (what might have been) the worst supply chain attack you can imagine]: https://jfrog.com/blog/leaked-pypi-secret-token-revealed-in-binary-preventing-suppy-chain-attack/
  