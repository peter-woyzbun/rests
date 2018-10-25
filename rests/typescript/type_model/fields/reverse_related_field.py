from django.db import models

from rests.typescript.type_model.fields.base import Field
from rests.core.utils.model_inspector import ModelInspector


# =================================
# Reverse Related Field
# ---------------------------------

class ReverseRelatedField(Field):

    def __init__(self, model_field: models.ManyToOneRel):
        self.model_field = model_field

    @property
    def name(self):
        return self.model_field.name

    @property
    def related_model_name(self):
        return self.model_field.related_model.__name__

    @property
    def reverse_lookup_key(self):
        inspector = ModelInspector(model=self.model_field.related_model)
        return inspector.fk_field_to_model(model=self.model_field.model).name + '__id'
