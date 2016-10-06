from rdflib import Graph
from rdflib.util import guess_format
from six import string_types

from ontology_alchemy.builder import OntologyBuilder


class Ontology(object):

    def __init__(self, namespace, **kwargs):
        """
        Initialize an ontology given a namespace.
        A namespace encapsulates the full hierarchy of types and inheritance relations
        described by the ontology.

        """
        self.namespace = namespace

    def __getattr__(self, name):
        return self.namespace[name]

    @classmethod
    def load(cls, file_or_filename, format=None):
        """
        Materialize ontology into Python class hierarchy from a given
        file-like object or a filename.

        :param file_or_filename - file-like object or local filesystem path to file
            containing ontology definition in one of the supported formats.
        :param format - the format ontology is serialized in.
            For list of currently supported formats (based on RDFlib which is used under the hood)
            see: http://rdflib.readthedocs.io/en/565/plugin_parsers.html
        :returns instance of the `Ontology` object which encompasses the ontology namespace
            for all created objects and types.

        """
        graph = Graph()
        if isinstance(file_or_filename, string_types):
            # Load from given filename
            if not format:
                format = guess_format(file_or_filename)
            graph.parse(file_or_filename, format=format)
        else:
            # Load from file-like buffer
            if not format:
                raise RuntimeError("Must supply format argument when not loading from a filename")
            graph.parse(file_or_filename, format=format)

        namespace = OntologyBuilder(graph).build_namespace()

        return cls(namespace)
