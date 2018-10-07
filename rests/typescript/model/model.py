from typing import Type, List

from django.db import models
from jinja2 import Template

from rests.core.utils.model_inspector import ModelInspector
from rests.typescript.model.field import Field


# =================================
# Typescript Model
# ---------------------------------

class Model(object):

    """
    Class for rendering a TypeScript `rests` model.

    """

    TEMPLATE = """
    // -------------------------
    // {{ model.name }}
    //
    // -------------------------

    interface {{ model.interface_type_name }} {
    {% for type_dec in model.field_interface_type_declarations %}{{ type_dec }}, \n{% endfor %}
    }


    export class {{ model.name }} extends Model {

        static BASE_URL = '/{{ model.type_url }}';
        static PK_FIELD_NAME = '{{ model.pk_field_name }}';
        static FIELDS = [{{ model.literal_field_names }}];

        static objects = {{ model.queryset_cls_name }};
        static serverClient = serverClient;

        {% for type_dec in model.field_cls_type_declarations %}{{ type_dec }};\n{% endfor %}

        constructor({ {{ model.field_names|join(',') }} }: {{ model.interface_type_name }}){
        super({ {{ model.field_names|join(',') }} })
        }

        public async update(data: Partial<{{ model.interface_type_name }}>, responseHandlers: ResponseHandlers={}): Promise<{{ model.name }}>{
            Object.keys(data).map((fieldName) => {
            this[fieldName] = data[fieldName];
        });
        await this.save();
        return this;
        }

        {% for field in model.reverse_relation_fields %}
        public {{ field.name }}(lookups: {{ field.related_model_name }}Lookups = {}){
            return new {{ field.related_model_name }}Queryset({...lookups, ...{ {{ field.reverse_lookup_key }}: this.pk()}})
        }
        {% endfor %}

    }

    {{ model.queryset_cls_name }}.Model = {{ model.name }};

        """

    def __init__(self, model: Type[models.Model], model_pool: List[Type[models.Model]], type_url):
        self.model = model
        self.model_pool = model_pool
        self.type_url = type_url
        self.model_inspector = ModelInspector(model=model)
        self.fields = [Field(field) for field in self.model_inspector.model_fields()]

    @property
    def name(self):
        return self.model_inspector.model_name

    @property
    def pk_field_name(self):
        return self.model_inspector.pk_field_name

    @property
    def interface_type_name(self):
        """ Return the name given to the type interface for this model. """
        return self.name + "Data"

    @property
    def field_names(self):
        field_names = list()
        for field in self.fields:
            field_names += field.names()
        return field_names

    @property
    def literal_field_names(self):
        return ", ".join("'{}'".format(f) for f in self.field_names)

    @property
    def field_interface_type_declarations(self):
        type_declarations = list()
        for field in self.fields:
            type_declarations += field.interface_type_declarations()
        return type_declarations

    @property
    def field_cls_type_declarations(self):
        type_declarations = list()
        for field in self.fields:
            type_declarations += field.cls_type_declarations()
        return type_declarations

    @property
    def queryset_cls_name(self):
        return self.name + "Queryset"

    @property
    def reverse_relation_fields(self):
        return [f for f in self.fields if f.is_reverse_relation]

    def render(self):
        return Template(self.TEMPLATE).render(model=self)