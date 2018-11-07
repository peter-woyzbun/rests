from typing import Type, List, Iterable

from django.db import models
from rest_framework import serializers
from rest_framework.fields import empty

from rests.typescript.type_transpiler import TypeTranspiler
from rests.typescript.type_model.fields.base import Field
from rests.typescript.utils.render_object import render_object, Literal


# =================================
# Read Only Field
# ---------------------------------

class ReadOnlyField(Field):

    SERIALIZER_TYPE_MAP = {
        serializers.JSONField: 'object',
        serializers.CharField: 'string',
        serializers.IntegerField: 'number',
        serializers.FloatField: 'number',
        serializers.ListField: 'any[]',
        serializers.BooleanField: 'boolean',
        serializers.DictField: 'object'
    }

    def __init__(self, name: str, serializer: serializers.Field, model_field: models.Field = None):
        self.name = name
        self.serializer = serializer
        self.model_field = model_field

    def names(self):
        yield self.name

    def exposed_name(self):
        return self.name

    @property
    def type_dec(self):
        return "readonly " + self.name + ": " + self._type

    def interface_type_declarations(self):
        yield self.type_dec

    def cls_type_declarations(self):
        yield self.type_dec

    @property
    def _type(self):
        if self.model_field is not None:
            return TypeTranspiler.transpile(self.model_field)
        if type(self.serializer) in self.SERIALIZER_TYPE_MAP:
            return self.SERIALIZER_TYPE_MAP[type(self.serializer)]
        return "any"
