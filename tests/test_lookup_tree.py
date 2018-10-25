from django.test import TestCase

from rests.interface.lookup_tree import LookupTree
from .models import Thing, ThingChild, ThingChildChild, ThingChildChildChild


# =================================
# Test Lookup Tree
# ---------------------------------

class TestLookupTree(TestCase):

    def test_get_root_models_list(self):
        lookup_tree = LookupTree(tree=[ThingChild])
        self.assertEqual(lookup_tree.root_models(), [ThingChild])

    def test_get_root_models_dict(self):
        lookup_tree = LookupTree(tree={ThingChild: [ThingChildChild]})
        self.assertEqual(lookup_tree.root_models(), [ThingChild])

    def test_get_root_models_nested_subtree(self):
        lookup_tree = LookupTree(tree={ThingChild: {ThingChildChild: [ThingChildChildChild]}})
        self.assertEqual(lookup_tree.root_models(), [ThingChild])
        subtree = lookup_tree.sub_tree(ThingChild)
        self.assertEqual(subtree.root_models(), [ThingChildChild])
        subtree = subtree.sub_tree(ThingChildChild)
        self.assertEqual(subtree.root_models(), [ThingChildChildChild])

    def test_get_subtree(self):
        lookup_tree = LookupTree(tree={ThingChild: [ThingChildChild]})
        subtree = lookup_tree.sub_tree(root_model=ThingChild)
        self.assertEqual(subtree.root_models(), [ThingChildChild])


