"""Unit-tests for the core ontology module."""
from hamcrest import (
    assert_that,
    calling,
    contains,
    instance_of,
    is_,
    raises,
)
from rdflib import Literal
from six import StringIO, string_types

from ontology_alchemy.ontology import Ontology
from ontology_alchemy.tests.fixtures import RDFS_TURTLE_ONTOLOGY


def create_ontology_file_object():
    return StringIO(RDFS_TURTLE_ONTOLOGY)


def create_ontology():
    return Ontology.load(create_ontology_file_object(), format="turtle")


def test_loading_from_file_stream_works():
    ontology = Ontology.load(create_ontology_file_object(), format="turtle")

    assert_that(ontology, is_(instance_of(Ontology)))


def test_ontology_class_base_properties_are_valid():
    ontology = create_ontology()

    assert_that(ontology.Organization, is_(instance_of(type)))
    assert_that(ontology.Organization.__name__, is_("Organization"))
    assert_that(ontology.Organization.__uri__, is_(instance_of(string_types)))
    assert_that(ontology.Organization.__labels__, contains(
        Literal("Organization", lang="en")
    ))


def test_nonexistant_label_language_raises_key_error():
    ontology = create_ontology()
    label = "Acme Inc."
    instance = ontology.Organization(label=label)

    assert_that(calling(instance.label).with_args(lang="foo"), raises(KeyError))
