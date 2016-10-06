from logging import getLogger

from rdflib import Literal, RDF, RDFS
from six.moves.urllib.parse import urldefrag, urlparse
from transitions import Machine, State

from ontology_alchemy.base import OntologyClass
from ontology_alchemy.schema import (
    is_type_predicate,
)


class BuilderState:
    PROCESS_TYPES = "process_types"
    PROCESS_LITERALS = "process_literals"
    PROCESS_RELATIONS = "process_relations"


class OntologyBuilder(object):

    # Define the ontology builder state machine states
    STATES = [
        State(BuilderState.PROCESS_TYPES, on_exit=["toposort_types"]),
        State(BuilderState.PROCESS_LITERALS),
        State(BuilderState.PROCESS_RELATIONS, on_exit=["assign_relational_properties"])
    ]

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

        self.state_machine = Machine(
            model=self,
            states=OntologyBuilder.STATES,
            initial=BuilderState.PROCESS_TYPES
        )

        self.state_machine.add_transition(
            "run_state_machine",
            BuilderState.PROCESS_TYPES,
            BuilderState.PROCESS_LITERALS,
            before="process_statement",
            conditions=["is_done_processing_types"],
        )

        self._properties_accumulator = {}

    def populate(self):
        """
        Iterate over all RDF statements describing ontology in a stable ordering
        that guarantees type definitions and inheritance relationships are evaluated first,
        and build the Python class hierarchy under a common namespace object.

        :returns {dict} namespace containing all the defined Python classes

        """
        def rdf_iterator_sort_func(statement):
            _, p, _ = statement
            try:
                return {
                    RDF.type: 0,
                    RDFS.subClassOf: 1
                }[p]
            except KeyError:
                return float("inf")

        for s, p, o in sorted(self.graph, key=rdf_iterator_sort_func):
            self.logger.debug("populate() - indexing triplet (s, p, o) = (%s, %s, %s)", s, p, o)
            if self.state == BuilderState.PROCESS_TYPES:
                self.process_type_statement((s, p, o))  # self.process_statement((s, p, o))

        return self.namespace

    def process_type_statement(self, statement):
        class_uri, _, _ = statement
        self.add_class(class_uri)

    def is_done_processing_types(self, statement):
        _, p, _ = statement
        return not is_type_predicate(p)

    def toposort_types(self, *args, **kwargs):
        return

    def add_class(self, class_uri):
        class_name = self._extract_name(class_uri)
        self.namespace[class_name] = type(
            class_name,
            (OntologyClass,),
            {"__uri__": class_uri}
        )
        self.logger.debug("_add_class() - Added class: %s", class_name)

    def add_comment(self, class_uri, comment, lang="en"):
        # XXX - For now we ignore language tags on comments and simply
        # assume a single comment is provided for a class and use it as
        # the class' __doc__.
        class_name = self._extract_name(class_uri)
        self.namespace[class_name].__doc__ = comment

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
