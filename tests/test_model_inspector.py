from django.test import TestCase

from rests.core.utils.model_inspector import ModelInspector

from .models import Thing, ThingChild


# =================================
# Test Model Inspector
# ---------------------------------

class TestModelInspector(TestCase):

    def test_get_pk_field(self):
        inspector = ModelInspector(Thing)
        self.assertEqual(inspector.pk_field_name, 'id')

    def test_get_fk_field_to_model(self):
        inspector = ModelInspector(ThingChild)
        self.assertEqual(inspector.fk_field_to_model(Thing).name, 'parent')

    def _test_get_fk_fields(self):
        inspector = ModelInspector(ThingChild)
        self.assertEqual(inspector.foreign_key_fields(), [ThingChild.parent])
