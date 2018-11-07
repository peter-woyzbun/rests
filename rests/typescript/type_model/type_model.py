from typing import Type, List

from django.db import models
from django.core.exceptions import FieldDoesNotExist
from jinja2 import Template
from rest_framework import serializers

from rests import interface
from rests.core.utils.model_inspector import ModelInspector
from rests.typescript.type_model.fields import ConcreteField, RelationalField, ReadOnlyField, ReverseRelatedField
from rests.typescript.type_model.method import Method


# =================================
# Typescript Model
# ---------------------------------

class TypeModel(object):
    """
        Class for rendering a TypeScript `rests` model.

        """

    TEMPLATE = """
        // -------------------------
        // {{ model.name }}
        //
        // -------------------------

        export interface {{ model.interface_type_name }} {
        {% for type_dec in model.field_interface_type_declarations %}{{ type_dec }}, \n{% endfor %}
        }


        export class {{ model.name }} extends Model {

            public static BASE_URL = '/{{ model.type_url }}';
            public static PK_FIELD_NAME = '{{ model.pk_field_name }}';
            public static FIELDS = [{{ model.literal_field_names }}];
            public static FIELDS_SCHEMA = {
             {% for field in model.schema_fields %}{{ field.schema_key }}: {{ field.schema|safe }},\n{% endfor %}
            }
             

            public static objects = {{ model.queryset_cls_name }};
            public static serverClient = serverClient;

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
            
            public async partialUpdate(data: Partial<{{ model.interface_type_name }}>, responseHandlers: ResponseHandlers={}): Promise<{{ model.name }}>{
                let responseData = await this.serverClient().post(`${this.baseUrl()}/${ this.pk() }/update/`, data, responseHandlers)
                return new {{ model.name }}(responseData)
            }

            {% for field in model._reverse_relation_fields %}
            public {{ field.name }}(lookups: {{ field.related_model_name }}Lookups = {}){
                return new {{ field.related_model_name }}Queryset({...lookups, ...{ {{ field.reverse_lookup_key }}: this.pk()}})
            }
            {% endfor %}
            
            {% for method in model.methods %}
            public async {{ method.name }}({{ method.arg_signature }}responseHandlers: ResponseHandlers={}){
                const data = {{ method.arg_map }};
                const result = await this.serverClient().post(`${ {{ model.name }}.BASE_URL}/methods/{{ method.type_method.url_name }}/${this.pk()}/`, data, responseHandlers);
                return result
            }
            {% endfor %}
            
        
        }

        {{ model.queryset_cls_name }}.Model = {{ model.name }};

            """

    def __init__(self, interface_type: interface.Type, model_pool: List[Type[models.Model]]):
        self.interface_type = interface_type
        self.model_pool = model_pool
        self.model_inspector = ModelInspector(model=interface_type.model_cls)

        self._reverse_relation_fields: List[ReverseRelatedField] = list()
        self._relational_fields: List[RelationalField] = list()
        self._concrete_fields: List[ConcreteField] = list()
        self._readonly_fields: List[ReadOnlyField] = list()

        self.methods: List[Method] = list()
        self.static_methods: List[Method] = list()

        self._make_fields()
        self._make_methods()

    def _make_fields(self):
        serializer_fields = self.interface_type.serializer_cls().get_fields()
        for field_name, serializer in serializer_fields.items():
            model_field = self._get_serializer_model_field(field_name)
            if isinstance(serializer, serializers.HiddenField):
                continue
            if isinstance(model_field, models.ManyToManyField):
                continue
            if serializer.read_only:
                self._readonly_fields.append(ReadOnlyField(serializer=serializer, name=field_name))
                continue
            if isinstance(model_field, (models.ForeignKey, models.OneToOneField)):
                if model_field.related_model in self.model_pool:
                    self._relational_fields.append(RelationalField(
                        serializer=serializer,
                        model_field=model_field,
                        model_pool=self.model_pool,
                        model=self.interface_type.model_cls
                    ))
                continue
            if model_field is not None:
                self._concrete_fields.append(
                    ConcreteField(serializer=serializer, model_field=model_field,
                                  model=self.interface_type.model_cls, model_pool=self.model_pool)
                )
        for model_field in self.model_inspector.reverse_related_fields():
            if model_field.related_model in self.model_pool:
                self._reverse_relation_fields.append(
                    ReverseRelatedField(model_field=model_field)
                )

    def _make_methods(self):
        for interface_type_method in self.interface_type.methods + self.interface_type.static_methods:
            if interface_type_method.is_static:
                self.static_methods.append(Method(type_method=interface_type_method))
            else:
                self.methods.append(Method(type_method=interface_type_method))

    @property
    def declared_fields(self):
        return self._concrete_fields + self._relational_fields + self._readonly_fields

    def _get_serializer_model_field(self, field_name):
        try:
            return self.interface_type.model_cls._meta.get_field(field_name)
        except FieldDoesNotExist:
            return None

    @property
    def schema_fields(self):
        return self._concrete_fields + self._relational_fields

    @property
    def type_url(self):
        return self.interface_type.base_url

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
        for field in self.declared_fields:
            for name in field.names():
                field_names.append(name)
        return field_names

    @property
    def literal_field_names(self):
        return ", ".join("'{}'".format(f) for f in self.field_names)

    @property
    def field_interface_type_declarations(self):
        type_declarations = list()
        for field in self.declared_fields:
            type_declarations += field.interface_type_declarations()
        return type_declarations

    @property
    def field_cls_type_declarations(self):
        type_declarations = list()
        for field in self.declared_fields:
            type_declarations += field.cls_type_declarations()
        return type_declarations

    @property
    def queryset_cls_name(self):
        return self.name + "Queryset"

    def render(self):
        return Template(self.TEMPLATE).render(model=self)