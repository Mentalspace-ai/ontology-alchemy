"""Base classes used in constructing ontologies."""
from six import text_type, with_metaclass


class OntologyClassMeta(type):
    """
    Metaclass for the `OntologyClass`.
    This metaclass governs the creation of all classes which correspond to Ontology classes.

    """
    def __new__(cls, name, parents, dct):
        dct.setdefault("__labels__", [])
        dct.setdefault("__uri__", None)

        return super(OntologyClassMeta, cls).__new__(cls, name, parents, dct)


class OntologyClass(with_metaclass(OntologyClassMeta)):
    """
    Base class for all dynamically-generated ontology classes.

    """

    def __init__(self, labels=None, *args, **kwargs):
        self.labels = labels or []

    def label(self, lang="en"):
        try:
            return text_type(
                next(
                    (label for label in self.labels if label.language == lang)
                )
            )
        except StopIteration:
            raise KeyError("No label found for lang='{}'".format(lang))
