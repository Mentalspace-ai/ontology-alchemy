from logging import getLogger

from rdflib import Literal, RDF
from six.moves.urllib.parse import urldefrag, urlparse

from ontology_alchemy.base import OntologyClass
from ontology_alchemy.schema import (
    is_label_predicate,
    is_type_predicate,
    rdf_iterator_sort_func,
)


class OntologyBuilder(object):

    def __init__(self, graph, base_uri=None):
        """
        Build the Python class hierarchy representing the ontology given
        its triplestore graph.

        :param graph - the populated `rdflib.Graph` instance for the Ontology
        :param base_uri - The base URI namespace for the Ontology. If not provided,
            will try to infer from ontology definition directly.
        """
        self.base_uri = base_uri or self._infer_base_uri(graph)
        self.graph = graph
        self.namespace = {}

        self.logger = getLogger(__name__)

    def populate(self):
        for s, p, o in sorted(self.graph, key=rdf_iterator_sort_func):
            # Iterate over all RDF statements describing ontology in a stable ordering
            # that guarantees type definitions and inheritance relationships are evaluated first.
            self.logger.debug("populate() - indexing triplet (s, p, o) = (%s, %s, %s)", s, p, o)
            if is_type_predicate(p):
                self._add_class(s)
            elif is_label_predicate(p):
                self._add_label(s, o)
            # else:
            #     print(s, p, o)

        return self.namespace

    def _add_class(self, class_uri):
        class_name = self._extract_name(class_uri)
        self.namespace[class_name] = type(
            class_name,
            (OntologyClass,),
            {
                "__uri__": class_uri,
            }
        )
        self.logger.debug("_add_class() - Added class: %s", class_name)

    def _add_label(self, class_uri, label, lang="en"):
        class_name = self._extract_name(class_uri)
        self.namespace[class_name].__labels__.append(
            Literal(label, lang=lang)
        )

    def _extract_name(self, uri):
        return uri.replace(self.base_uri, "")

    def _infer_base_uri(self, graph):
        """
        Attempt to infer automatically the base URI for the given ontology
        by looking at definitions.

        The simple heuristic employed is to URL-parse the subject of the first
        encountered triple with RDF.type as its predicate in the RDF graph and
        extract it's last path component.

        :param graph - `rdflib.Graph` instance populated with ontology
        :returns {str} the inferred base URI

        """
        for s, p, o in graph.triples((None, RDF.type, None)):
            parsed_url = urlparse(s)
            if parsed_url.fragment:
                return "{}#".format(urldefrag(s)[0])
