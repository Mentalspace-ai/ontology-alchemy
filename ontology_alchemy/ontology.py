from rdflib import Graph
from rdflib.util import guess_format
from six import string_types


class Ontology(object):

    def __init__(self):
        pass

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
            if not format:
                format = guess_format(file_or_filename)
            parsed = graph.parse(file_or_filename, format=format)
        else:
            if not format:
                raise RuntimeError("Must supply format argument when not loading from a filename")
            parsed = graph.parse(file_or_filename, format=format)

        return cls()
