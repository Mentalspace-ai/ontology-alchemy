"""Unit-tests for the core ontology module."""
from hamcrest import (
    assert_that,
    contains_inanyorder,
    empty,
    is_,
)

from ontology_alchemy.session import Session, session_context
from ontology_alchemy.tests.fixtures import create_ontology


def assert_session_matches_expected(session, ontology):
    assert_that(session.classes, contains_inanyorder(
        ontology.Corporation,
        ontology.Country,
        ontology.Thing,
        ontology.GovernmentOrganization,
        ontology.Organization,
        ontology.Person,
        ontology.hasEmployee,
        ontology.hasExecutive,
        ontology.naics,
    ))


def assert_session_is_empty(session):
    assert_that(session.classes, is_(empty()))
    assert_that(session.instances, is_(empty()))


def test_default_session_registered_ontology_classes():
    default_session = Session.get_current()
    default_session.clear()

    ontology = create_ontology()

    assert_session_matches_expected(default_session, ontology)


def test_session_context_manager_registers_ontology_classes_properly():
    default_session = Session.get_current()
    default_session.clear()

    with session_context() as session:
        ontology = create_ontology()
        assert_session_matches_expected(session, ontology)

    assert_session_is_empty(default_session)


def test_session_decorator_registers_ontology_classes_properly():
    default_session = Session.get_current()
    default_session.clear()

    @session_context()
    def _create_ontology():
        ontology = create_ontology()
        assert_session_matches_expected(Session.get_current(), ontology)

    _create_ontology()

    assert_session_is_empty(default_session)
