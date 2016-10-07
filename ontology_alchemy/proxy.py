"""Proxy objects."""
from rdflib import Literal
from six import string_types, text_type

from ontology_alchemy.constants import DEFAULT_LANGUAGE_TAG


class PropertyProxy(object):
    """
    A proxy class for accessing RDFS.Property instances as Python class instance attributes.
    It supports evaluating whether a given value assignment is valid based on the RDF definitions
    of domain and range.

    """

    def __init__(self, name=None, values=None, domain=None, range=None):
        self.name = name
        self.values = values or []
        self.domain = domain
        self.range = range

    def __call__(self, value=None):
        return value in self.values

    def __iadd__(self, value):
        if not self.is_valid(value):
            raise ValueError("Invalid assigment. property value must be of type {}, but got: {}"
                             .format(self.range, value))

        self.add_instance(value)
        return self

    @classmethod
    def for_(cls, property_cls):
        return PropertyProxy(
            name=property_cls.__name__,
            domain=property_cls.__domain__,
            range=property_cls.__range__
        )

    def add_instance(self, value):
        self.values.append(value)

    def is_valid(self, value):
        if isinstance(value, self.range):
            return True


class LiteralPropertyProxy(PropertyProxy):
    def __call__(self, lang=None):
        if lang:
            return [
                text_type(literal)
                for literal in self.values
                if literal.language == lang
            ] or None
        else:
            return self.values

    def add_instance(self, value):
        if not isinstance(value, Literal):
            if isinstance(value, string_types):
                value = Literal(value, lang=DEFAULT_LANGUAGE_TAG)

        self.values.append(value)

    def is_valid(self, value):
        if (isinstance(value, Literal) or
                isinstance(value, string_types)):
            return True
