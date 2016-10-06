"""Proxy objects."""


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

    def __call__(self, value):
        return value in self.values

    def __iadd__(self, value):
        if not self.is_valid(value):
            raise ValueError("Invalid assigment. property value must be of type {}, but got: {}"
                             .format(self.range, value))

        self.values.append(value)
        return self

    @classmethod
    def for_(cls, property_cls):
        return PropertyProxy(
            name=property_cls.__name__,
            domain=property_cls.__domain__,
            range=property_cls.__range__
        )

    def is_valid(self, value):
        if isinstance(value, self.range):
            return True
