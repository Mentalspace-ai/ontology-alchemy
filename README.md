# ontology-alchemy

ontology-alchemy makes using [RDF](https://en.wikipedia.org/wiki/Resource_Description_Framework) [ontology](https://en.wikipedia.org/wiki/Ontology_(information_science)) definitions to create Python class hierarchies easy.

[![CircleCI](https://circleci.com/gh/globality-corp/ontology-alchemy/tree/develop.svg?style=svg)](https://circleci.com/gh/globality-corp/ontology-alchemy/tree/develop)

# Overview

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

# Developing

To work on the package locally, create a [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/), and then install package using:

    pip install -e .

# Similar Projects

* [Owlready](http://pythonhosted.org/Owlready/index.html) - Exposes a simple interface to load OWL ontologies and create instances as Python classes. Also includes a reasoner engine (HermiT). Main limitation is that it only works with OWL and only supports OWL XML serialization format.
