from collections import defaultdict
from logging import getLogger

from rdflib import Literal, RDF, RDFS
from six.moves.urllib.parse import urldefrag, urlparse
from toposort import toposort

from ontology_alchemy.base import RDFSClass, RDFSProperty
from ontology_alchemy.schema import (
    is_a_property,
    is_comment_predicate,
    is_domain_predicate,
    is_label_predicate,
    is_range_predicate,
    is_sub_class_predicate,
    is_type_predicate,
)


class OntologyBuilder(object):

    def __init__(self, graph, base_uri=None):
        """
        Build the Python class hierarchy representing the ontology given
        its triplestore graph.

        The supported vocabulary of asserted statements consists of the
        RDF Schema classes and properties as defined in https://www.w3.org/TR/rdf-schema/

        :param graph - the populated `rdflib.Graph` instance for the Ontology
        :param base_uri - The base URI namespace for the Ontology. If not provided,
            will try to infer from ontology definition directly.
        """
        self.base_uri = base_uri or self._infer_base_uri(graph)
        self.graph = graph
        self.namespace = {}
        self.logger = getLogger(__name__)

        self._type_graph = {}
        self._sub_class_graph = defaultdict(set)
        self._asserted_statements = set()

    def build_namespace(self):
        """
        Iterate over all RDF statements describing ontology in a stable ordering
        that guarantees type definitions and inheritance relationships are evaluated first,
        and build the Python class hierarchy under a common namespace object.

        :returns {dict} namespace containing all the defined Python classes

        """
        for s, p, o in self.graph:
            if is_type_predicate(p):
                self._type_graph[s] = o
            elif is_sub_class_predicate(p):
                self._sub_class_graph[s].add(o)
            else:
                self._asserted_statements.add((s, p, o))

        self._build_class_hierarchy()

        return self.namespace

    def add_class(self, class_uri, base_class_uris=None, is_property=False):
        class_name = self._extract_name(class_uri)

        base_classes = (RDFSProperty,) if is_property else (RDFSClass,)
        if base_class_uris:
            base_classes = tuple(
                self.namespace[self._extract_name(base_class_uri)]
                for base_class_uri in base_class_uris
            )

        self.namespace[class_name] = type(
            class_name,
            base_classes,
            {"__uri__": class_uri}
        )
        self.logger.debug("_add_class() - Added class: %s", class_name)

    def add_comment(self, class_uri, comment, lang="en"):
        # XXX - For now we ignore language tags on comments and simply
        # assume a single comment is provided for a class and use it as
        # the class' __doc__.
        class_name = self._extract_name(class_uri)
        self.namespace[class_name].__doc__ = comment

    def add_property_domain(self, property_uri, domain_uri):
        property_name = self._extract_name(property_uri)
        self.namespace[property_name].__domain__.append(
            domain_uri
        )

    def add_property_range(self, property_uri, range_uri):
        property_name = self._extract_name(property_uri)
        self.namespace[property_name].__range__.append(
            range_uri
        )

    def add_label(self, class_uri, label, lang="en"):
        class_name = self._extract_name(class_uri)
        self.namespace[class_name].__labels__.append(
            Literal(label, lang=lang)
        )

    def add_property(self, property_uri):
        property_name = self._extract_name(property_uri)
        self.namespace[property_name] = {}

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

    def _build_class_hierarchy(self):
        """
        Given the graphs of rdf:type and rdfs:subClassOf relations,
        build the class hierarchy.
        We use topological sort to build the hierarchy in order of
        dependencies and to identify any circular dependencies.

        For reference on the logic rules governing type and subClassOf relations
        see the diagrams here: http://liris.cnrs.fr/~pchampin/2001/rdf-tutorial/node14.html

        """
        for uri in self._type_graph:
            if uri not in self._sub_class_graph:
                # Make sure all types are represented in the sub class graph by adding self links.
                self._sub_class_graph[uri].add(uri)

        for classes in toposort(self._sub_class_graph):
            for class_uri in classes:
                is_property = is_a_property(self._type_graph[class_uri])
                self.add_class(
                    class_uri,
                    base_class_uris=self._sub_class_graph[class_uri],
                    is_property=is_property
                )

        for s, p, o in self._asserted_statements:
            if is_label_predicate(p):
                self.add_label(s, o)
            elif is_comment_predicate(p):
                self.add_comment(s, o)
            elif is_domain_predicate(p):
                self.add_property_domain(s, o)
            elif is_range_predicate(p):
                self.add_property_range(s, o)
