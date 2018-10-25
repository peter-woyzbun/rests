from typing import Union, List
import datetime
import inspect

from django.db import models
from django.db.models import lookups
from django.db.models.fields import related_lookups
from django.contrib.postgres.fields import JSONField, ArrayField

from rests.core.utils.typing_inspect import get_origin, get_args
from rests.typescript import types


# =================================
# Type Transpiler
# ---------------------------------

class TypeTranspiler(object):

    # Rendering for "atomic" types - types that don't "contain"
    # other types.
    ATOMIC_TYPES = {
        # Built-in types
        str: types.STRING,
        int: types.NUMBER,
        float: types.NUMBER,
        bool: types.BOOLEAN,
        dict: types.OBJECT,
        None: types.NULL,
        datetime.datetime: types.DATE,
        # Typescript types
        types.Undefined: types.UNDEFINED,
        # Model field types
        JSONField: types.OBJECT,
        models.CharField: types.STRING,
        models.TextField: types.STRING,
        models.UUIDField: types.STRING,
        models.SlugField: types.STRING,
        models.SmallIntegerField: types.STRING,
        models.BigIntegerField: types.NUMBER,
        models.EmailField: types.STRING,
        models.URLField: types.STRING,
        models.IntegerField: types.NUMBER,
        models.PositiveIntegerField: types.NUMBER,
        models.PositiveSmallIntegerField: types.NUMBER,
        models.DecimalField: types.NUMBER,
        models.FloatField: types.NUMBER,
        models.AutoField: types.NUMBER,
        models.BigAutoField: types.NUMBER,
        models.BooleanField: types.BOOLEAN,
        models.NullBooleanField: f"{types.BOOLEAN} | {types.NULL}",
        models.DateTimeField: types.DATE,
        models.DateField: types.DATE,
        models.ForeignKey: lambda x: x.related_model.__name__,
        models.OneToOneField: lambda x: x.related_model.__name__,
        models.ManyToManyField: lambda x: x.related_model.__name__,
        models.ManyToOneRel: lambda x: x.related_model.__name__,
        ArrayField: lambda x: TypeTranspiler.transpile(x.base_field) + "[]",
        # Model type
        models.Model: lambda x: x.__name__,
    }

    # Rendering for "container" types - types that can "contain" a
    # single other type.
    CONTAINER_TYPES = {
        List: lambda x: f"{types.ARRAY}<{x}>",
        types.Promise: lambda x: f"{types.PROMISE}<{x}>",
        lookups.In: lambda x: f'{x}[]',
        related_lookups.RelatedIn: lambda x: f'{x}[]',
        lookups.Range: lambda x: f'[{x}, {x}]',
    }

    # Rendering for "composite" types - types that can "contain" one or
    # more other types.
    COMPOSITE_TYPES = {
        tuple: lambda x: ", ".join(x),
        Union: lambda x: " | ".join(x)
    }

    @classmethod
    def transpile(cls, type_):
        origin_type = get_origin(type_)
        child_types = get_args(type_)
        if not origin_type:
            return cls.render_atomic_type(type_)
        return cls._transpile((origin_type, child_types))

    @classmethod
    def render_atomic_type(cls, type_):
        # Todo: catch exceptions/errors here.
        base_type = type_
        if not inspect.isclass(type_):
            base_type = type(type_)
        if issubclass(base_type, models.Model):
            base_type = models.Model
        if base_type not in cls.ATOMIC_TYPES:
            return cls.render_atomic_type(type_=base_type.__bases__[0])
        if hasattr(cls.ATOMIC_TYPES[base_type], "__call__"):
            return cls.ATOMIC_TYPES[base_type](type_)
        return cls.ATOMIC_TYPES[base_type]

    @classmethod
    def _transpile(cls, type_):

        if not isinstance(type_, tuple):
            return cls.render_atomic_type(type_)
        if isinstance(type_[0], tuple):
            return cls._transpile(type_[0])
        if type_[0] in cls.COMPOSITE_TYPES:
            return cls.COMPOSITE_TYPES[type_[0]]([cls._transpile(child_type) for child_type in type_[1]])
        if type_[0] in cls.CONTAINER_TYPES:
            return cls.CONTAINER_TYPES[type_[0]](cls._transpile(type_[1]))
        if len(type_) == 1:
            try:
                return cls.render_atomic_type(type_[0])
            except KeyError:
                return cls.render_atomic_type(type_[0].__class__)



