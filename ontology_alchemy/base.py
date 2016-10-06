"""Base classes used in constructing ontologies."""
from collections import defaultdict

from rdflib import Literal
from six import string_types, text_type, with_metaclass

from ontology_alchemy.constants import DEFAULT_LANGUAGE_TAG
from ontology_alchemy.session import Session


class RDFS_ClassMeta(type):
    """
    Metaclass for the `RDFS_Class` class.

    This metaclass governs the creation of all classes which correspond
    to an RDFS.Class resource.

    """
    def __new__(meta_cls, name, bases, dct):
        dct.setdefault("__labels__", [])
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
        dct.setdefault("__domain__", [])
        dct.setdefault("__range__", [])

        return super(RDFS_PropertyMeta, cls).__new__(cls, name, parents, dct)


class RDFS_Class(with_metaclass(RDFS_ClassMeta)):
    """
    Base class for all dynamically-generated ontology classes corresponding
    to the RDFS.Class resource.

    """

    def __init__(self, label=None, comment=None, *args, **kwargs):
        self._literal_properties = defaultdict(set)

        if label:
            self.add_literal_property("label", label)
        if comment:
            self.add_literal_property("comment", comment)

        Session.get_current().register_instance(self)

    def add_literal_property(self, property_name, value):
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
