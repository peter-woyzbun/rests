import os
from typing import Type, List

from django.db import models
from jinja2 import Template

from rests.core.utils.model_inspector import ModelInspector
from rests.typescript.queryset.lookups import QuerysetLookups


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
    
    interface {{ queryset.lookups_type_name }} {
    {% for type_dec in queryset.lookup_declarations %}{{ type_dec }},\n{% endfor %}
    }

    export class {{ queryset.name }} extends Queryset{
    
        public static Model: typeof {{ queryset.model_name }};
        public static serverClient = serverClient;
    
        protected lookups: {{ queryset.lookups_type_name }};
        protected excludedLookups: {{ queryset.lookups_type_name }};
        protected _or: {{ queryset.name }}[];
    
        constructor(lookups: {{ queryset.lookups_type_name }} = {}, excludedLookups: {{ queryset.lookups_type_name }} = {}){
            super(lookups, excludedLookups)
        }
        
        public static filter(lookups: {{ queryset.lookups_type_name }}): {{ queryset.name }} {
        return new {{ queryset.name }}(lookups)       
    }
    
    public static async get(primaryKey: string | number, responseHandlers: ResponseHandlers={} ): Promise< {{ queryset.model_name }} | undefined>{
        let responseData = await this.serverClient.get(`${this.Model.BASE_URL}/${primaryKey}/get/`, responseHandlers);

        if (responseData){return new this.Model(responseData)}
        return undefined
    }
    
    
    }

    """

    def __init__(self, model: Type[models.Model], model_pool: List[Type[models.Model]], type_url):
        self.model = model
        self.model_pool = model_pool
        self.type_url = type_url
        self.model_inspector = ModelInspector(model=model)
        self.queryset_lookups = QuerysetLookups(model=model, model_pool=model_pool)

    @property
    def name(self):
        return self.model_name + "Queryset"

    @property
    def model_name(self):
        return self.model_inspector.model_name

    @property
    def lookups_type_name(self):
        return self.model_inspector.model_name + "Lookups"

    @property
    def lookup_declarations(self):
        return self.queryset_lookups.type_declarations()

    def render(self):
        return Template(self.TEMPLATE).render(queryset=self)


