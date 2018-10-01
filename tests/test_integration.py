from rests.test import ava, IntegrationTestCase

from rests import interface
from .models import ThingSerializer, ThingChildSerializer, Thing, ThingChild


# =================================
# Interface
# ---------------------------------


class GenericObject(interface.Object):

    def __init__(self, name: str):
        self.name = name

    @interface.Object.endpoint()
    def get_name(self):
        return {'name': self.name}

    @interface.Object.endpoint()
    def func_with_arg(self, x: int):
        return {'val': x * 100}


class Interface(interface.Interface):
    things = interface.Type(serializer_cls=ThingSerializer)
    thing_children = interface.Type(serializer_cls=ThingChildSerializer)
    generic_object = GenericObject


urlpatterns = Interface.urlpatterns()


# =================================
# Integration Tests
# ---------------------------------

class IntegrationTests(IntegrationTestCase):

    ROOT_URL_CONF = __name__

    def test_get_thing_pk(self):
        thing = Thing.objects.create()
        self.assertAvaTestPassed(
            ava.Test('get-thing-pk')
                .async()
                .import_model(Thing).body("const obj = await Thing.objects.get({});".format(thing.id))
                .deep_equal('obj.pk()', thing.id)
        )

    def test_get_thing_name(self):
        thing = Thing.objects.create(name='abc')
        self.assertAvaTestPassed(
            ava.Test('get-thing-pk')
                .async()
                .import_model(Thing).body("const obj = await Thing.objects.get({});".format(thing.id))
                .deep_equal('obj.name', ava.literal('abc'))
        )

    def test_save_thing(self):
        thing = Thing.objects.create(name='abc')
        self.assertAvaTestPassed(
            ava.Test('update-thing')
                .async()
                .import_model(Thing).body("""
                const obj = await Thing.objects.get({});
                obj.name = 'abc123';
                await obj.save()
                """.format(thing.id))
                .deep_equal('obj.name', ava.literal('abc123'))
        )

        thing.refresh_from_db()
        self.assertEqual(thing.name, 'abc123')

    def test_update_thing(self):
        thing = Thing.objects.create(name='abc')
        self.assertAvaTestPassed(
            ava.Test('update-thing')
                .async()
                .import_model(Thing).body("""
                const obj = await Thing.objects.get({});
                await obj.update({{name: 'abc123'}})
                """.format(thing.id))
                .deep_equal('obj.name', ava.literal('abc123'))
        )

        thing.refresh_from_db()
        self.assertEqual(thing.name, 'abc123')

    def test_delete_thing(self):
        thing = Thing.objects.create(name='abc')
        self.assertAvaTestPassed(
            ava.Test('delete-thing')
                .async()
                .import_model(Thing).body("""
                        const obj = await Thing.objects.get({});
                        await obj.delete()
                        """.format(thing.id))
                .deep_equal('1', '1')
        )
        self.assertFalse(Thing.objects.filter(id=thing.id))

    def test_query_filter(self):
        thing_1 = Thing.objects.create(name='1')
        thing_2 = Thing.objects.create(name='2')
        self.assertAvaTestPassed(
            ava.Test('filter-things')
                .async()
                .import_model(Thing).body("""
                const objects = await Thing.objects.filter({name: '1'}).retrieve();
                const pks = objects.map((obj) => {return obj.pk()})
                """)
                .deep_equal('pks', [thing_1.id])
        )

    def test_query_filter_values(self):
        thing_1 = Thing.objects.create(name='1')
        thing_2 = Thing.objects.create(name='2')
        self.assertAvaTestPassed(
            ava.Test('filter-things')
                .async()
                .import_model(Thing).body("""
                const objects = await Thing.objects.filter({name: '1'}).values({}, 'name');
                """)
                .deep_equal('objects', [{'name': thing_1.name}])
        )

    def test_query_pagination(self):
        thing_1 = Thing.objects.create(name='1')
        thing_2 = Thing.objects.create(name='2')
        thing_3 = Thing.objects.create(name='3')
        self.assertAvaTestPassed(
            ava.Test('filter-things')
                .async()
                .import_model(Thing).body("""
                const page = await Thing.objects.filter({}).pageValues(1, 2, {}, 'name');
                """)
                .deep_equal('page.data.length', 2)
        )

    def test_query_filter_or(self):
        thing_1 = Thing.objects.create(name='1')
        thing_2 = Thing.objects.create(name='2')
        self.assertAvaTestPassed(
            ava.Test('filter-things')
                .async()
                .import_model(Thing).body("""
                const objects = await Thing.objects.filter({name: '1'}).or(Thing.objects.filter({name: '2'})).retrieve();
                const pks = objects.map((obj) => {return obj.pk()})
                """)
                .deep_equal('pks', [thing_1.id, thing_2.id])
        )

    def test_reverse_relation(self):
        thing_1 = Thing.objects.create(name='1')
        child_1 = ThingChild.objects.create(parent=thing_1)
        child_2 = ThingChild.objects.create(parent=thing_1)
        self.assertAvaTestPassed(
            ava.Test('filter-things')
                .async()
                .import_model(Thing).body("""
                        const obj = await Thing.objects.get({0});
                        const children = await obj.children().retrieve();
                        const pks = children.map((obj) => {{return obj.pk()}})
                        """.format(thing_1.id))
                .deep_equal('pks', [child_1.id, child_2.id])
        )

    def test_reverse_relation_filter(self):
        thing_1 = Thing.objects.create(name='1')
        child_1 = ThingChild.objects.create(parent=thing_1)
        child_2 = ThingChild.objects.create(parent=thing_1, name='a')
        self.assertAvaTestPassed(
            ava.Test('filter-things')
                .async()
                .import_model(Thing).body("""
                        const obj = await Thing.objects.get({0});
                        const children = await obj.children().filter({{name: 'a'}}).retrieve();
                        const pks = children.map((obj) => {{return obj.pk()}})
                        """.format(thing_1.id))
                .deep_equal('pks', [child_2.id])
        )

    def _test_object_endpoint(self):
        self.assertAvaTestPassed(
            ava.Test('get-object-name')
                .async()
                .import_object(GenericObject).body("""
                const obj = new GenericObject('a');
                const objName = await obj.getName({});
                                """)
                .deep_equal("objName['name']", ava.literal('a'))
        )

    def _test_object_endpoint_with_arg(self):
        self.assertAvaTestPassed(
            ava.Test('get-object-name')
                .async()
                .import_object(GenericObject).body("""
                const obj = new GenericObject('a');
                const data = await obj.funcWithArg({}, 10);
                                """)
                .deep_equal("data['val']", 1000)
        )


