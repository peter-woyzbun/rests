from typing import Type, Dict, Union, List

from django.db import models


# =================================
# Tree Type
# ---------------------------------


Tree = Union[List[Type[models.Model]], Dict[Type[models.Model], 'Tree']]


# =================================
# Lookup Tree
# ---------------------------------

class LookupTree(object):

    def __init__(self, tree: Tree):
        self.tree = tree

    def __contains__(self, item: Type[models.Model]):
        return item in self.root_models()

    def __add__(self, other: Type[models.Model]):
        if isinstance(self.tree, list):
            self.tree.append(other)
        if isinstance(self.tree, dict):
            self.tree[other] = []
        return self

    def root_models(self) -> List[Type[models.Model]]:
        if isinstance(self.tree, list):
            return self.tree
        if isinstance(self.tree, dict):
            return list(self.tree.keys())

    def sub_tree(self, root_model: Type[models.Model]):
        if isinstance(self.tree, list):
            return LookupTree(tree=[])
        if isinstance(self.tree, dict):
            return LookupTree(tree=self.tree[root_model])


