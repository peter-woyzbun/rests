from typing import Type, List

from django.db import models
from django.core.exceptions import FieldDoesNotExist
from rest_framework import serializers
from rest_framework.fields import empty

from rests.core.utils.model_inspector import ModelInspector
from rests.typescript.type_transpiler import TypeTranspiler
from rests.typescript.utils.render_object import render_object, Literal
from rests.typescript.accessors import PropertyAccessors


# =================================
# Typescript Model Field
# ---------------------------------

class Field(object):

    def __init__(self, name: str, model: Type[models.Model], model_pool: List[Type[models.Model]],
                 model_field: models.Field = None, serializer: serializers.Field = None):
        self.name = name
        self.serializer = serializer
        self.model = model
        self.model_pool = model_pool
        self._model_field: models.Field = model_field if model_field is not None else None

        self._get_model_field()

    def _get_model_field(self):
        """
        Try getting the Model field of this `Field` - serializer fields do not always
        have a corresponding field for the Model: `SerializerMethodField`'s, for
        example.

        """
        if self._model_field is None:
            try:
                self._model_field = self.model._meta.get_field(self.name)
            except FieldDoesNotExist:
                pass

    @property
    def schema(self):
        return render_object({
            'fieldName': self.name,
            'fieldType': Literal("FieldType." + self._model_field.__class__.__name__),
            'nullable': self.serializer.allow_null,
            'isReadOnly': self.serializer.read_only,
            'description': self._schema_description,
            'defaultValue': self._schema_default_value,
            'relatedModel': self._schema_related_model,
            'choices': self._choices
        })

    @property
    def _schema_related_model(self):
        if self.related_model is None:
            return Literal("undefined")
        if self.related_model not in self.model_pool:
            return Literal("undefined")
        return Literal("() => " + self.related_model_name)

    @property
    def _schema_default_value(self):
        if self.serializer.default == empty:
            return "undefined"
        return self.serializer.default

    @property
    def schema_key(self):
        if self.is_many_to_many:
            return None
        return self.name

    @property
    def _schema_description(self):
        if self.serializer.help_text:
            return str(self.serializer.help_text)
        return Literal("undefined")

    @property
    def _choices(self):
        if hasattr(self._model_field, 'choices'):
            choices = [c[0] for c in self._model_field.choices]
            if len(choices) > 0:
                return choices
        return Literal("undefined")

    def names(self) -> List[str]:
        """
        Return the list of names for this field. This is plural because ForeignKey
        and OneToOne fields have two names: one for the related instance, and one
        for the `id` of the related instance.

        """
        names = list()
        if not self.is_declared:
            return names
        names.append(self.name)
        if self.is_relational:
            names.append(self.fk_id_name)
        return names

    def interface_type_declarations(self):
        """
        Return the `interface` type declarations for this field. This will be used
        to generate the `<model_name>Data` TypeScript interface.


        """
        type_declarations = list()
        if not self.is_declared:
            return type_declarations
        type_declarations.append(self.base_interface_type_declaration)
        # If this field is a ForeignKey, add an extra declaration for its
        # `id` lookup.
        if isinstance(self._model_field, models.ForeignKey):
            type_declarations.append(self.fk_id_type_declaration)
        return type_declarations

    def cls_type_declarations(self):
        """
        Return the class property declarations for this field. This will be used
        to declare the names/types for this field for its TypeScript Model class.

        """
        type_declarations = list()
        if not self.is_declared:
            return type_declarations
        type_declarations.append(self.base_cls_type_declaration)
        # If this field is a ForeignKey, add an extra declaration for its
        # `id` lookup.
        if isinstance(self._model_field, models.ForeignKey):
            type_declarations.append(self.fk_id_type_declaration)
        return type_declarations

    @property
    def base_interface_type_declaration(self):
        type_dec = self.name + "?" * self.is_optional + " : " + TypeTranspiler.transpile(self._model_field)
        return type_dec

    @property
    def base_cls_type_declaration(self):
        type_dec = self.name + "?" * self.is_optional + " : " + TypeTranspiler.transpile(self._model_field)
        if self.is_relational:
            return f"@foreignKeyField(() => {self.related_model_name}) " + type_dec
        return type_dec

    @property
    def fk_id_type_declaration(self):
        return self.fk_id_name + "?" * self.is_optional + " : number"

    @property
    def fk_id_name(self):
        return self.name + "_id"

    @property
    def is_derived(self):
        """
        Return True if this field is 'derived' - it has no corresponding Model field.

        """
        return self._model_field is None

    @property
    def is_optional(self) -> bool:
        return self.serializer.allow_null

    @property
    def is_relational(self):
        return isinstance(self._model_field, (models.ForeignKey, models.OneToOneField, models.ManyToManyField))

    @property
    def is_many_to_many(self):
        return isinstance(self._model_field, models.ManyToManyField)

    @property
    def is_reverse_relation(self):
        return isinstance(self._model_field, models.ManyToOneRel)

    @property
    def is_concrete(self):
        return not self.is_relational and not self.is_reverse_relation

    @property
    def related_model(self):
        if self.is_concrete:
            return None
        return self._model_field.related_model

    @property
    def related_model_name(self):
        if self.is_concrete:
            return None
        return self._model_field.related_model.__name__

    @property
    def is_declared(self):
        """
        Return whether or not this Field is 'declared'.

        """
        if isinstance(self.serializer, serializers.HiddenField):
            return False
        # Dont declare ManyToManyField's - this functionality needs to be added.
        if isinstance(self._model_field, models.ManyToManyField):
            return False
        # Reverse relations are not declared.
        if self.is_reverse_relation:
            return False
        # If this field is relational, and its related model is not in the model pool,
        # it is not declared.
        if self.is_relational and self.related_model not in self.model_pool:
            return False
        return True

    @property
    def reverse_lookup_key(self):
        inspector = ModelInspector(model=self._model_field.related_model)
        return inspector.fk_field_to_model(model=self._model_field.model).name + '__id'

