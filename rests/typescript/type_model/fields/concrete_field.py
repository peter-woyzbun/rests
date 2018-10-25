from typing import Type, List, Iterable

from django.db import models
from rest_framework import serializers
from rest_framework.fields import empty

from rests.typescript.type_transpiler import TypeTranspiler
from rests.typescript.type_model.fields.base import Field
from rests.typescript.utils.render_object import render_object, Literal


# =================================
# Concrete Field
# ---------------------------------

class ConcreteField(Field):

    def __init__(self, serializer: serializers.Field, model_field: models.Field,
                 model: Type[models.Model], model_pool: List[Type[models.Model]]):
        self.serializer = serializer
        self.model_field = model_field
        self.model = model
        self.model_pool = model_pool

    @property
    def name(self):
        return self.model_field.name

    def names(self) -> Iterable[str]:
        yield self.name

    @property
    def is_optional(self) -> bool:
        return self.serializer.allow_null

    def interface_type_declarations(self) -> Iterable[str]:
        """
        Return the `interface` type declarations for this field. This will be used
        to generate the `<model_name>Data` TypeScript interface.


        """
        yield self.base_interface_type_declaration

    def cls_type_declarations(self) -> Iterable[str]:
        """
        Return the class property declarations for this field. This will be used
        to declare the names/types for this field for its TypeScript Model class.

        """
        yield self.base_cls_type_declaration

    @property
    def base_interface_type_declaration(self):
        type_dec = self.name + "?" * self.is_optional + " : " + TypeTranspiler.transpile(self.model_field)
        return type_dec

    @property
    def base_cls_type_declaration(self):
        type_dec = self.name + "?" * self.is_optional + " : " + TypeTranspiler.transpile(self.model_field)
        return type_dec

    @property
    def related_model(self):
        return None

    @property
    def schema(self):
        return render_object({
            'fieldName': self.name,
            'fieldType': Literal("FieldType." + self.model_field.__class__.__name__),
            'nullable': self.serializer.allow_null,
            'isReadOnly': self.serializer.read_only,
            'description': self._schema_description,
            'defaultValue': self._schema_default_value,
            'relatedModel': self._schema_related_model,
            'choices': self._choices
        })

    @property
    def _schema_related_model(self):
        return Literal("undefined")

    @property
    def _schema_default_value(self):
        if self.serializer.default == empty:
            return "undefined"
        return self.serializer.default

    @property
    def schema_key(self):
        return self.name

    @property
    def _schema_description(self):
        if self.serializer.help_text:
            return str(self.serializer.help_text)
        return Literal("undefined")

    @property
    def _choices(self):
        if hasattr(self.model_field, 'choices'):
            choices = [c[0] for c in self.model_field.choices]
            if len(choices) > 0:
                return choices
        return Literal("undefined")
