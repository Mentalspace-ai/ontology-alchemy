"""Fixture data used by the unit-tests."""
from six import StringIO

from ontology_alchemy.ontology import Ontology


# Ontology serialized in Turtle, using RDFS vocabulary.
RDFS_TURTLE_ONTOLOGY = """
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
    @prefix exampleOntology: <http://example.com/namespace#> .

    exampleOntology:Thing a rdfs:Class;
        rdfs:label "Thing"@en;
        rdfs:comment "Base class for all things"@en;
        skos:exactMatch <http://schema.org/Thing>;
        .
    exampleOntology:Organization a rdfs:Class;
        rdfs:label "Organization"@en;
        rdfs:comment "An organization such as a school, NGO, corporation, club, etc."@en;
        rdfs:subClassOf exampleOntology:Thing;
        .
    exampleOntology:Corporation a rdfs:Class;
        rdfs:label "Corporation"@en;
        rdfs:comment "A business corporation."@en;
        rdfs:subClassOf exampleOntology:Organization;
        .
    exampleOntology:GovernmentOrganization a rdfs:Class;
        rdfs:label "Government Organization"@en;
        rdfs:comment "A governmental organization or agency."@en;
        rdfs:subClassOf exampleOntology:Organization;
        .
    exampleOntology:Person a rdfs:Class;
        rdfs:label "Person"@en;
        rdfs:subClassOf exampleOntology:Thing;
        .
    exampleOntology:naics a rdf:Property;
        rdfs:label "naics"@en;
        rdfs:domain exampleOntology:Organization;
        rdfs:range rdfs:Literal;
        rdfs:comment "The North American Industry Classification System (NAICS) code."
        .
    """


def create_ontology_file_object():
    return StringIO(RDFS_TURTLE_ONTOLOGY)


def create_ontology():
    return Ontology.load(create_ontology_file_object(), format="turtle")
