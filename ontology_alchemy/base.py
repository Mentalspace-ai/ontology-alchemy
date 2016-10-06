"""Base classes used in constructing ontologies."""
from collections import defaultdict

from rdflib import Literal
from six import string_types, text_type, with_metaclass

from ontology_alchemy.constants import DEFAULT_LANGUAGE_TAG
from ontology_alchemy.proxy import PropertyProxy
from ontology_alchemy.session import Session


class RDFS_ClassMeta(type):
    """
    Metaclass for the `RDFS_Class` class.

    This metaclass governs the creation of all classes which correspond
    to an RDFS.Class resource.

    """
    def __new__(meta_cls, name, bases, dct):
        dct.setdefault("__labels__", [])
        dct.setdefault("__properties__", [])
        dct.setdefault("__uri__", None)

        return super(RDFS_ClassMeta, meta_cls).__new__(meta_cls, name, bases, dct)

    def __init__(cls, name, bases, dct):
        Session.get_current().register_class(cls)
        return super(RDFS_ClassMeta, cls).__init__(name, bases, dct)


class RDFS_PropertyMeta(RDFS_ClassMeta):
    """
    Metaclass for the `RDFS_Property` class.

    This metaclass governs the creation of all property classes which correspond
    to an RDFS.Property resource.

    """
    def __new__(cls, name, parents, dct):
        dct.setdefault("__domain__", None)
        dct.setdefault("__range__", None)

        return super(RDFS_PropertyMeta, cls).__new__(cls, name, parents, dct)


class RDFS_Class(with_metaclass(RDFS_ClassMeta)):
    """
    Base class for all dynamically-generated ontology classes corresponding
    to the RDFS.Class resource.

    """

    def __init__(self, label=None, comment=None, *args, **kwargs):
        # XXX Need to set the literal properties registry like this since it is used
        # for evaluating assigments in __setattr__ below.
        super(RDFS_Class, self).__setattr__("_literal_properties", defaultdict(set))

        if label:
            self.assign_literal_property("label", label)
        if comment:
            self.assign_literal_property("comment", comment)

        for property_class in self.__class__.__properties__:
            setattr(self, property_class.__name__, PropertyProxy.for_(property_class))

        Session.get_current().register_instance(self)

    def __setattr__(self, name, value):
        if name in self._literal_properties:
            # Is a known literal-valued property
            self.assign_literal_property(name, value)
        # elif getattr(self, name) and isinstance(getattr(self, name), PropertyProxy):
        #     self.assign_domain_property(name, value)
        else:
            super(RDFS_Class, self).__setattr__(name, value)

    def assign_domain_property(self, property_name, value):
        property_proxy = getattr(self, property_name)
        property_proxy.assign(value)

    def assign_literal_property(self, property_name, value):
        if isinstance(value, Literal):
            # Value already wrapped in rdflib.Literal, no-op
            pass
        elif isinstance(value, string_types):
            # Wrap string types with Literal and assign a default language tag
            value = Literal(value, lang=DEFAULT_LANGUAGE_TAG)

        self._literal_properties[property_name].add(value)

    def get_literal_property(self, property_name, lang=None):
        value_set = self._literal_properties[property_name]
        if lang:
            try:
                return text_type(
                    next(
                        (literal for literal in value_set if literal.language == lang)
                    )
                )
            except StopIteration:
                raise KeyError("No label found for lang='{}'".format(lang))
        else:
            return value_set[0]

    def label(self, lang=DEFAULT_LANGUAGE_TAG):
        return self.get_literal_property("label", lang=lang)

    def comment(self, lang=DEFAULT_LANGUAGE_TAG):
        return self.get_literal_property("comment", lang=lang)


class RDFS_Property(with_metaclass(RDFS_PropertyMeta, RDFS_Class)):
    """
    Base class for all dynamically-generated ontology property classes
    corresponding to the RDFS.Property resource.

    """

    def __init__(self, domain=None, range=None, *args, **kwargs):
        self.domain = domain
        self.range = range
        super(RDFS_Property, self).__init__(*args, **kwargs)
