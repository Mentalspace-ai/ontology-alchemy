"""Base classes used in constructing ontologies."""
from six import text_type, with_metaclass


class OntologyClassMeta(type):

    def __new__(cls, name, parents, dct):
        dct.setdefault("__labels__", [])
        dct.setdefault("__uri__", None)

        return super(OntologyClassMeta, cls).__new__(cls, name, parents, dct)


class OntologyClass(with_metaclass(OntologyClassMeta)):
    """
    Base class for all dynamically-generated ontology classes.

    """

    def label(self, lang="en"):
        try:
            return text_type(
                next(
                    (label for label in self.__labels__ if label.language == lang)
                )
            )
        except StopIteration:
            raise KeyError("No label found for lang='{}'".format(lang))
