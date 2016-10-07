"""Base classes used in constructing ontologies."""
from collections import defaultdict

from rdflib import Literal
from six import string_types, text_type, with_metaclass

from ontology_alchemy.constants import DEFAULT_LANGUAGE_TAG
from ontology_alchemy.proxy import LiteralPropertyProxy, PropertyProxy
from ontology_alchemy.session import Session


class RDFS_ClassMeta(type):
    """
    Metaclass for the `RDFS_Class` class.

    This metaclass governs the creation of all classes which correspond
    to an RDFS.Class resource.

    """
    def __new__(meta_cls, name, bases, dct):
        dct.setdefault("__properties__", [])
        dct.setdefault("__uri__", None)

        dct.setdefault("label", LiteralPropertyProxy(name="label"))
        dct.setdefault("comment", LiteralPropertyProxy(name="comment"))

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

    def __init__(self, **kwargs):
        # Define proxies for the core RDFS properties as defined in the RDF Schema specification
        self.label = LiteralPropertyProxy(name="label")
        self.comment = LiteralPropertyProxy(name="comment")
        self.seeAlso = PropertyProxy(name="seeAlso")
        self.isDefinedBy = PropertyProxy(name="isDefinedBy")
        self.value = PropertyProxy(name="value")

        for property_class in self.__class__.__properties__:
            setattr(self, property_class.__name__, PropertyProxy.for_(property_class))

        for k, v in kwargs.items():
            property_proxy = getattr(self, k)
            property_proxy += v

        Session.get_current().register_instance(self)


class RDFS_Property(with_metaclass(RDFS_PropertyMeta, RDFS_Class)):
    """
    Base class for all dynamically-generated ontology property classes
    corresponding to the RDFS.Property resource.

    """

    def __init__(self, domain=None, range=None, *args, **kwargs):
        self.domain = domain
        self.range = range
        super(RDFS_Property, self).__init__(*args, **kwargs)
