"""Fixture data used by the unit-tests."""
from six import StringIO

from ontology_alchemy.ontology import Ontology


# Ontology serialized in Turtle, using RDFS vocabulary.
RDFS_TURTLE_ONTOLOGY = """
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
    @prefix exampleOntology: <http://example.com/namespace#> .

    exampleOntology:Thing a rdfs:Class;
        rdfs:label "Thing"@en;
        rdfs:comment "Base class for all things"@en;
        skos:exactMatch <http://schema.org/Thing>;
        .
    exampleOntology:Country a rdfs:Class;
        rdfs:label "Country"@en;
        rdfs:comment "a nation with its own government, occupying a particular territory."@en;
        rdfs:subClassOf exampleOntology:Thing;
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
    exampleOntology:currencyCode a rdf:Property;
        rdfs:label "currencyCode"@en;
        rdfs:domain exampleOntology:Country;
        rdfs:range xsd:string;
        rdfs:comment "Currency code of country's official currency.";
        .
    exampleOntology:naics a rdf:Property;
        rdfs:label "naics"@en;
        rdfs:domain exampleOntology:Organization;
        rdfs:range rdfs:Literal;
        rdfs:comment "The North American Industry Classification System (NAICS) code."
        .
    exampleOntology:numberOfEmployees a rdf:Property;
        rdfs:label "numberOfEmployees"@en;
        rdfs:domain exampleOntology:Organization;
        rdfs:range xsd:integer;
        rdfs:comment "The number of employees an organization employs.";
        skos:exactMatch <http://schema.org/numberOfEmployees>
        .
    exampleOntology:hasEmployee a rdf:Property;
        rdfs:label "hasEmployee"@en;
        rdfs:domain exampleOntology:Organization;
        rdfs:range exampleOntology:Person;
        rdfs:comment "Signify a given Organization has a given Person as an employee"
        .
    exampleOntology:hasExecutive a rdf:Property;
        rdfs:label "hasExecutive"@en;
        rdfs:subPropertyOf exampleOntology:hasEmployee;
        rdfs:comment "Signify a given Organization has a given Person as an executive"
        .
    """


def create_ontology_file_object():
    return StringIO(RDFS_TURTLE_ONTOLOGY)


def create_ontology():
    return Ontology.load(create_ontology_file_object(), format="turtle")
