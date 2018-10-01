import os
from typing import Type, List

from django.db import models
from jinja2 import Template

from rests.core.utils.model_inspector import ModelInspector
from rests.typescript.queryset.lookups import QuerysetLookups
from rests.typescript.type_transpiler import TypeTranspiler
from rests.typescript import code_generators as ts
from rests.core.utils.dir_classes import find_classes_in_dir
from rests.typescript.queryset import methods
from rests.typescript.queryset.method import QuerysetMethod


# =================================
# Methods
# ---------------------------------

METHODS_DIR = os.path.join(os.path.dirname(__file__), 'methods')


# =================================
# Typescript Queryset
# ---------------------------------

class Queryset(object):

    TEMPLATE = """
    // -------------------------
    // {{ queryset.model_name }} QuerySet
    //
    // -------------------------

    {{ queryset.lookups_type_interface }}

    {{ queryset.klass }}

    """

    def __init__(self, model: Type[models.Model], model_pool: List[Type[models.Model]], type_url):
        self.model = model
        self.model_pool = model_pool
        self.type_url = type_url
        self.model_inspector = ModelInspector(model=model)
        self.queryset_lookups = QuerysetLookups(model=model, model_pool=model_pool)

    def methods(self):
        methods_ = list()
        for MethodCls in find_classes_in_dir(METHODS_DIR, methods.__package__, QuerysetMethod).values():
            methods_.append(MethodCls(queryset=self).generator())
        return methods_

    @property
    def pk_field_name(self):
        return self.model_inspector.pk_field_name

    @property
    def pk_field_type(self):
        return TypeTranspiler.transpile(self.model_inspector.pk_field)

    @property
    def model_name(self):
        return self.model_inspector.model_name

    @property
    def class_name(self):
        return self.model_inspector.model_name + 'QuerySet'

    @property
    def lookups_type_interface(self):
        val = ts.export + ts.TypeInterface(name=self.lookups_type_name, type_declarations=self.queryset_lookups.type_declarations())
        return str(val)

    @property
    def lookups_type_name(self):
        return self.model_inspector.model_name + "Lookups"

    @property
    def lookups_type_dec(self):
        return ts.TypeDeclaration(var_name='lookups', type_=self.lookups_type_name)

    @property
    def get_url(self):
        return "`/{type_url}/${pk_field}/get/`".format(type_url=self.type_url,
                                                       pk_field="{" + self.model_inspector.pk_field_name + "}")

    @property
    def create_url(self):
        return "`/{type_url}/create/`".format(type_url=self.type_url,
                                              pk_field="{" + self.model_inspector.pk_field_name + "}")

    @property
    def list_url(self):
        return "`/{type_url}/`".format(type_url=self.type_url)

    @property
    def klass(self):
        excl_lookups_type_dec = ts.TypeDeclaration(var_name='excludedLookups', type_=self.lookups_type_name)
        or_queryset_dec = ts.TypeDeclaration(var_name='_or', type_=self.class_name + '[]')
        constructor_sig = ts.CallSignature(
            kwargs={
                self.lookups_type_dec: "{}",
                excl_lookups_type_dec: "{}",
                or_queryset_dec: "[]"
            }
        )
        return ts.export + ts.Klass(name=self.class_name,
                        constructor_signature=constructor_sig,
                        type_declarations=[
                            self.lookups_type_dec.protected(),
                            excl_lookups_type_dec.protected(),
                            or_queryset_dec.protected()
                        ])(
            *self.methods()
        )

    def render(self):
        return Template(self.TEMPLATE).render(queryset=self)