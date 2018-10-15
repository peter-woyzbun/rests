from typing import Type, List, Union

from django.db import models

from rests.core.utils.model_inspector import ModelInspector
from rests.typescript.type_transpiler import TypeTranspiler


# =================================
# Typescript Queryset Lookups
# ---------------------------------

class QuerysetLookups(object):

    """
    Helper class for rendering "type declarations" for Queryset lookups.

    """

    def __init__(self, model: Type[models.Model], model_pool: List[Type[models.Model]],
                 parent: 'QuerysetLookups'=None, prefixes: List[str] = None, visited_models=None):
        self.model = model
        self.model_pool = model_pool
        self.parent = parent
        self.prefixes = prefixes if prefixes is not None else []
        self.visited_models = visited_models if visited_models is not None else []
        self.model_inspector = ModelInspector(model)

    def _lookup_key(self, suffixes: List[str]=None):
        if suffixes is None:
            suffixes = []
        return "__".join(self.prefixes + suffixes)

    def type_declarations(self):
        type_declarations = list()
        for field in self.model_inspector.model_fields():
            type_declarations += self._field_type_declarations(field=field)
        return type_declarations

    def _field_type_declarations(self, field: models.Field):
        type_declarations = list()
        # If the field is relational, check that it is in the `model_pool`, and that
        # it has not already been "visited" (to prevent an infinite cycle).
        if isinstance(field, (models.ForeignKey, models.OneToOneField, models.ManyToOneRel)):
            if (field.related_model in self.model_pool) and (field.related_model not in self.visited_models):
                child_queryset_lookups = QuerysetLookups(model=field.related_model,
                                                         model_pool=self.model_pool,
                                                         prefixes=self.prefixes + [field.name],
                                                         visited_models=self.visited_models + [self.model])
                type_declarations += child_queryset_lookups.type_declarations()
            else:
                return type_declarations
        if not isinstance(field, models.ManyToOneRel):

            # This is the base lookup for the field.
            type_declarations.append(
                self._lookup_key([field.name]) + "? : " + self._lookup_type(field, None)
            )

            for lookup_str, lookup_cls in field.get_lookups().items():
                type_declarations.append(
                    self._lookup_key([field.name, lookup_str]) + "? : " + self._lookup_type(field, lookup_cls)
                )
        return type_declarations

    @staticmethod
    def _lookup_type(field, lookup_cls) -> str:
        if lookup_cls in TypeTranspiler.CONTAINER_TYPES:
            return TypeTranspiler.CONTAINER_TYPES[lookup_cls](TypeTranspiler.transpile(field))
        return TypeTranspiler.transpile(field)


