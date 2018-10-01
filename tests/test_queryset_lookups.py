from django.test import TestCase

from rests.core.utils.model_inspector import ModelInspector
from rests.typescript.queryset.lookups import QuerysetLookups
from rests.typescript.queryset.queryset import Queryset
from rests.typescript.model.model import Model

from .models import Thing, ThingChild


# =================================
# Test Model Inspector
# ---------------------------------

class TestModelInspector(TestCase):

    def test(self):
        queryset_lookups = QuerysetLookups(model=ThingChild, model_pool=[ThingChild, Thing])
        for type_dec in queryset_lookups.type_declarations():
            pass
            # print(str(type_dec))

    def test_2(self):
        queryset = Queryset(model=Thing, model_pool=[ThingChild, Thing], type_url='abc')
        print(queryset.render())

    def test_3(self):
        model = Model(model=Thing, model_pool=[ThingChild, Thing], type_url='abc')
        print(model.render())