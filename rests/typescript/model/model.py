import os
from typing import Type, List

from django.db import models
from jinja2 import Template

from rests.core.utils.model_inspector import ModelInspector
from rests.typescript.type_transpiler import TypeTranspiler
from rests.typescript import code_generators as ts
from rests.core.utils.dir_classes import find_classes_in_dir
from rests.typescript.model.field import Field
from rests.typescript.model import methods
from rests.typescript.model.method import ModelMethod


# =================================
# Methods
# ---------------------------------

METHODS_DIR = os.path.join(os.path.dirname(__file__), 'methods')


# =================================
# Typescript Model
# ---------------------------------

class Model(object):

    TEMPLATE = """
    // -------------------------
    // {{ model.name }}
    //
    // -------------------------

    {{ model.fields_type_interface }}
    
    type {{ model.name }}FieldName = {{ model.literal_field_names|join(" | ") }}
    
    {{ model.field_name_type }}

    {{ model.klass }}
    

    """

    def __init__(self, model: Type[models.Model], model_pool: List[Type[models.Model]], type_url):
        self.model = model
        self.model_pool = model_pool
        self.type_url = type_url
        self.model_inspector = ModelInspector(model=model)
        self.fields = [Field(field) for field in self.model_inspector.model_fields()]

    def render(self):
        return Template(self.TEMPLATE).render(model=self)

    def methods(self):
        methods_ = list()
        for MethodCls in find_classes_in_dir(METHODS_DIR, methods.__package__, ModelMethod).values():
            methods_.append(MethodCls(model=self).generator())
        return methods_

    @property
    def pk_field_name(self):
        return self.model_inspector.pk_field_name

    @property
    def pk_field_type(self):
        return TypeTranspiler.transpile(self.model_inspector.pk_field)

    @property
    def name(self):
        return self.model_inspector.model_name

    def field_type_declarations(self):
        type_declarations = list()
        for field in self.fields:
            type_declarations += field.type_declarations()
        return type_declarations

    @property
    def fields_type_interface_name(self):
        return self.name + "Data"

    @property
    def fields_type_interface(self):
        return ts.TypeInterface(name=self.fields_type_interface_name, type_declarations=self.field_type_declarations())

    @property
    def field_name_type(self):
        return ""

    @property
    def literal_field_names(self):
        return ['"' + td.var_name + '"' for td in self.field_type_declarations()]

    @property
    def _literal_field_names_lis(self):
        return ", ".join(self.literal_field_names)

    @property
    def field_names(self):
        return [td.var_name for td in self.field_type_declarations()]

    @property
    def klass(self):

        data_type_dec = ts.TypeDeclaration(var_name=ts.Destructuring(self.field_names), type_=self.fields_type_interface_name)

        constructor_sig = ts.CallSignature(data_type_dec)
        return ts.export + ts.Klass(name=self.name,
                        constructor_signature=constructor_sig,
                        type_declarations=self.field_type_declarations())(
            *self.methods() + self._field_methods + [
                f"public static objects = { self.model_inspector.model_name }QuerySet;",
                f"public static readonly FIELDS = [{self._literal_field_names_lis}];"
            ]
        )

    @property
    def _field_methods(self):
        field_methods = list()
        for field in self.fields:
            field_methods.append(str(field.public_getter_method))
            field_methods.append(str(field.private_getter_method))
            field_methods.append(str(field.setter_method))
            field_methods.append(str(field.reverse_relation_getter))
        return field_methods

