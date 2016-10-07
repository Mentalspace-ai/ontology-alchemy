"""Unit-tests for the core ontology module."""
from unittest import skip

from hamcrest import (
    assert_that,
    calling,
    contains_inanyorder,
    equal_to,
    instance_of,
    is_,
    raises,
)
from rdflib import Literal
from six import string_types, text_type

from ontology_alchemy.base import RDFS_Class, RDFS_Property
from ontology_alchemy.ontology import Ontology
from ontology_alchemy.tests.fixtures import create_ontology_file_object, create_ontology


def test_loading_from_file_stream_works():
    ontology = Ontology.load(create_ontology_file_object(), format="turtle")

    assert_that(ontology, is_(instance_of(Ontology)))


def test_rdfs_class_hierarchy_is_valid():
    ontology = create_ontology()

    # XXX See the fixture ontology for the definitions of these types

    assert_that(ontology.Thing, is_(instance_of(type)))
    assert_that(ontology.Thing.__bases__, contains_inanyorder(
        RDFS_Class,
    ))

    assert_that(ontology.Organization, is_(instance_of(type)))
    assert_that(ontology.Organization.__name__, is_("Organization"))
    assert_that(ontology.Organization.__bases__, contains_inanyorder(
        ontology.Thing,
    ))
    assert_that(ontology.Organization.__subclasses__(), contains_inanyorder(
        ontology.Corporation,
        ontology.GovernmentOrganization,
    ))
    assert_that(text_type(ontology.Organization.__uri__), is_(equal_to(
        "{}{}".format(ontology.__uri__, ontology.Organization.__name__)
    )))
    assert_that(ontology.Organization.label(lang="en"), contains_inanyorder(
        "Organization"
    ))

    assert_that(ontology.naics, is_(instance_of(type)))
    assert_that(ontology.naics.__name__, is_("naics"))
    assert_that(ontology.naics.__bases__, contains_inanyorder(
        RDFS_Property,
    ))
    assert_that(ontology.naics.__uri__, is_(instance_of(string_types)))
    assert_that(ontology.naics.label(lang="en"), contains_inanyorder(
        "naics"
    ))
