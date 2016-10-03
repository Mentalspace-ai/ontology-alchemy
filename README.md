# ontology-alchemy

ontology-alchemy makes using [RDF](https://en.wikipedia.org/wiki/Resource_Description_Framework) [ontology](https://en.wikipedia.org/wiki/Ontology_(information_science)) definitions to create Python class hierarchies easy.

[![CircleCI](https://circleci.com/gh/globality-corp/ontology-alchemy/tree/develop.svg?style=svg)](https://circleci.com/gh/globality-corp/ontology-alchemy/tree/develop)

## Overview

This project aims to make it easy to work programmatically with RDF Ontologies. RDF Ontologies are prelevant in the world of [Semantic Web](https://en.wikipedia.org/wiki/Semantic_Web). Notable projects using these include [schema.org](http://schema.org), which includes a general ontology that can be used by websites to describe their contents, and [DBPedia](http://wiki.dbpedia.org) which maintains a curated, multi-lingual structured knowledge graph based on Wikipedia.

Some of the main tasks made possible with this library include:

* Loading an existing RDF Ontology (e.g from a Turtle/N3 serialized format) into Python code, allowing introspection of the ontology. This is done via [rdflib](http://rdflib.readthedocs.io/en/stable/).
* Creating Pythonic class instances using the types defined in the ontology, including properties and relations, as well as native data types
* Validation on property value types based on ontology definitions
* Easy interfacing to persistence layer by a Session abstraction which exposes all instances created in an easy-to-use way

## Usage

The package is compatible with Python 2.7 or 3.x. To install from PyPI, simple as:

    pip install ontology-alchemy

Assuming an existing RDF ontology definition serialized in [Turtle](https://en.wikipedia.org/wiki/Turtle_(syntax)), you could then do:

    from ontology_alchemy import Ontology, Session

    # Load ontology definition, create all Python classes
    ontology = Ontology.load("my-ontology.ttl")

    # Can then define particular instances and assign properties and relations.
    country = ontology.Country(label="United States")
    language = ontology.Language(label="English")
    country.officialLanguage = language

    # Interfacing with a persistent backend is easy by using the `Session` object:

    # Get all programmatic class instances created since beginning of session
    print session.instances

    # Stream RDF statements capturing all class instances, properties and relations created
    for (subject, predicate, object) in session.rdf_statements():
        print(subject, predicate, object)

See the examples/ folder for a full example.

## Developing

To work on the package locally, create a [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/), and then install package using:

    pip install -e .

## Similar Projects

* [Owlready](http://pythonhosted.org/Owlready/index.html) - Exposes a simple interface to load OWL ontologies and create instances as Python classes. Also includes a reasoner engine (HermiT). Main limitation is that it only works with OWL and only supports OWL XML serialization format.
