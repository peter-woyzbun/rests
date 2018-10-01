import inspect

from typing import Type, List, Union, Tuple

from django.db import models


# =================================
# Model Inspector
# ---------------------------------

class ModelInspector(object):

    def __init__(self, model: Type[models.Model]):
        self.model = model

    def model_fields(self) -> List[models.Field]:
        return self.model._meta.get_fields()

    def filter_fields(self,
                      keep_field_type: Union[Type[models.Field], Tuple[Type[models.Field]]]=None,
                      exclude_field_type: Union[Type[models.Field], Tuple[Type[models.Field]]]=None) -> List[models.Field]:
        if keep_field_type is not None:
            return [f for f in self.model_fields() if isinstance(f, keep_field_type)]
        return [f for f in self.model_fields() if not isinstance(f, exclude_field_type)]

    def concrete_fields(self):
        return [
            f for f in self.model_fields()
            if not isinstance(f, (models.ForeignKey, models.ManyToOneRel, models.OneToOneField))
        ]

    @property
    def model_name(self):
        if inspect.isclass(self.model):
            return self.model.__name__
        return type(self.model).__name__

    @property
    def pk_field_name(self) -> str:
        """
        Return the name of the primary key field of this `ModelInspector`'s
        model.

        """
        return self.pk_field.name

    @property
    def pk_field(self) -> models.Field:
        """
        Return the primary key field instance of this `ModelInspector`'s
        model.

        """
        return self.model._meta.pk

    def foreign_key_fields(self) -> List[models.Field]:
        return [f for f in self.model_fields() if isinstance(f, models.ForeignKey)]

    def fk_field_to_model(self, model: Type[models.Model]):
        """
        Return the field of the given model that is a `ForeignKey` field
        pointing to this inspector's model.

        """
        for field in self.foreign_key_fields():
            if field.related_model == model:
                return field

    def relation_tree(self):
        return self.model._meta._relation_tree
