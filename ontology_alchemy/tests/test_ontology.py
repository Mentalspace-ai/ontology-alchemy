"""Unit-tests for the core ontology module."""
from hamcrest import (
    assert_that,
    instance_of,
    is_,
)
from six import StringIO

from ontology_alchemy.ontology import Ontology
from ontology_alchemy.tests.fixtures import RDFS_TURTLE_ONTOLOGY


def test_loading_from_file_stream_works():
    file_object = StringIO(RDFS_TURTLE_ONTOLOGY)
    ontology = Ontology.load(file_object, format="turtle")

    assert_that(ontology, is_(instance_of(Ontology)))
