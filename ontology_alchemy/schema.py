"""
Common schema definition types that should be mapped to corresponding Python objects.

Some of the primary mappings of interest include:

* the rdfs:Class type which should be mapped to Python class
* the rdfs:subClassOf property type which should be mapped to an inheritance relation

"""
from rdflib import RDF, RDFS, OWL


def is_class_predicate(predicate):
    return predicate in (
        RDFS.Class,
        OWL.Class,
    )


def is_label_predicate(predicate):
    return predicate in (
        RDFS.label,
    )


def is_type_predicate(predicate):
    return predicate == RDF.type


def rdf_iterator_sort_func(statement):
    s, p, o = statement
    try:
        return {
            RDF.type: 0,
            RDFS.subClassOf: 1
        }[p]
    except KeyError:
        return float("inf")
