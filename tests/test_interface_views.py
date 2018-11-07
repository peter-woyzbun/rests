import json

from django.test import TestCase
from django.urls import reverse
from django.test import override_settings
from rest_framework.test import APIClient
from rest_framework import status


from rests import interface
from .models import ThingSerializer, ThingChildSerializer, Thing, GenericModelSeriaizer, GenericModel


# =================================
# Interface
# ---------------------------------

class GenericObject(interface.Object):

    def __init__(self, name: str):
        self.name = name

    @interface.Object.endpoint()
    def get_name(self):
        return {'name': self.name}


class GenericModelType(interface.Type, serializer_cls=GenericModelSeriaizer):

    @interface.Type.method()
    def example_method(self: GenericModel):
        return {'name': self.name}

    @interface.Type.method()
    def example_method_args(self: GenericModel, append_to_name: str):
        return {'name': self.name + append_to_name}


class Interface(interface.Interface):
    things = interface.Type(serializer_cls=ThingSerializer)
    thing_children = interface.Type(serializer_cls=ThingChildSerializer)
    generic_object = GenericObject
    generic_models = GenericModelType.as_type()


urlpatterns = Interface.urlpatterns()


# =================================
# Type View Tests
# ---------------------------------

# Override settings to load urlpatterns from this module (defined above).
@override_settings(ROOT_URLCONF=__name__)
class TestInterfaceTypeViews(TestCase):

    client: APIClient

    def setUp(self):
        self.client = APIClient()

    def test_get_view(self):
        thing = Thing.objects.create(name='test')
        view_url = reverse('thing:get', kwargs={'pk': thing.id})
        response = self.client.get(view_url)
        self.assertEqual('test', response.data['name'])

    def test_create_view(self):
        data = {'name': 'test'}
        view_url = reverse('thing:create')
        response = self.client.post(view_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Thing.objects.filter(name='test').exists())

    def test_update_view(self):
        thing = Thing.objects.create()
        view_url = reverse('thing:update', kwargs={'pk': thing.id})
        data = {'name': 'new name'}
        response = self.client.post(view_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        thing.refresh_from_db()
        self.assertEqual(thing.name, 'new name')

    def test_delete_view(self):
        thing = Thing.objects.create()
        thing_id = thing.id
        view_url = reverse('thing:delete', kwargs={'pk': thing.id})
        response = self.client.delete(view_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Thing.objects.filter(id=thing_id).exists())

    def test_list_view_no_query(self):
        thing_1 = Thing.objects.create(name='1')
        thing_2 = Thing.objects.create(name='2')
        view_url = reverse('thing:list')
        response = self.client.get(view_url)
        self.assertEqual(len(response.data), 2)

    def test_list_view_query_filter(self):
        thing_1 = Thing.objects.create(name='1')
        thing_2 = Thing.objects.create(name='2')
        view_url = reverse('thing:list')
        query = {
            'filters': {'name__in': ['1']},
            'exclude': {},
            'or_': []
        }
        query_str = json.dumps(query)
        view_url += '?query=' + query_str
        response = self.client.get(view_url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], '1')

    def test_list_view_query_filter_or(self):
        thing_1 = Thing.objects.create(name='1')
        thing_2 = Thing.objects.create(name='2')
        view_url = reverse('thing:list')
        query = {
            'filters': {'name__in': ['1']},
            'exclude': {},
            'or_': [{
            'filters': {'name__in': ['2']},
            'exclude': {},
            'or_': []
        }]
        }
        query_str = json.dumps(query)
        view_url += '?query=' + query_str
        response = self.client.get(view_url)
        self.assertEqual(len(response.data), 2)

    def test_list_view_query_filter_exclude(self):
        thing_1 = Thing.objects.create(name='1')
        thing_2 = Thing.objects.create(name='2')
        view_url = reverse('thing:list')
        query = {
            'exclude': {'name__in': ['1']},
            'filters': {},
            'or_': []
        }
        query_str = json.dumps(query)
        view_url += '?query=' + query_str
        response = self.client.get(view_url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], '2')

    def test_list_view_field_subset(self):
        thing_1 = Thing.objects.create(name='1')
        thing_2 = Thing.objects.create(name='2')
        view_url = reverse('thing:list')
        query = {
            'exclude': {'name__in': ['1']},
            'filters': {},
            'or_': []
        }
        query_str = json.dumps(query)
        view_url += '?query=' + query_str + "&fields=" + json.dumps(['name'])
        response = self.client.get(view_url)
        self.assertEqual(set(response.data[0].keys()), {'name'})

    def test_list_view_paginated(self):
        thing_1 = Thing.objects.create(name='1')
        thing_2 = Thing.objects.create(name='2')
        view_url = reverse('thing:list')
        query = {
            'filters': {},
            'exclude': {},
            'or_': []
        }
        query_str = json.dumps(query)
        view_url += '?query=' + query_str + "&fields=" + json.dumps(['name']) + "&page=1&pagesize=1"
        response = self.client.get(view_url)
        self.assertEqual(response.data['num_results'], 2)
        self.assertEqual(response.data['num_pages'], 2)

        self.assertEqual(len(response.data['data']), 1)

    def test_method(self):
        generic_model = GenericModel.objects.create(name='abc')
        view_url = reverse('generic_model:list')
        view_url += f'methods/example-method/{generic_model.id}/'=
        response = self.client.post(view_url)
        self.assertEqual(response.data['name'], 'abc')

    def test_method_args(self):
        generic_model = GenericModel.objects.create(name='abc')
        view_url = reverse('generic_model:list')
        view_url += f'methods/example-method-args/{generic_model.id}/'
        response = self.client.post(view_url, data={'append_to_name': '_x'}, format='json')
        self.assertEqual(response.data['name'], 'abc_x')



# =================================
# Object View Tests
# ---------------------------------

# Override settings to load urlpatterns from this module (defined above).
@override_settings(ROOT_URLCONF=__name__)
class TestInterfaceObjectViews(TestCase):

    client: APIClient

    def setUp(self):
        self.client = APIClient()

    def test_object_endpoint(self):
        view_url = reverse('generic_object:get_name')
        data = {'__init__': {'name': 'a'}}
        response = self.client.post(view_url, data=data, format='json')
        self.assertEqual(response.data['name'], 'a')