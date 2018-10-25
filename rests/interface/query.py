from typing import List
from functools import reduce
import operator

from django.db import models


# =================================
# Interface Query
# ---------------------------------

class Query(object):

    """
    Helper class for applying list view queries. These queries will be sent by
    `<ModelName>QuerySet` TypeScript class instances. The query structure is
    essentially a simple boolean algebra.

    """

    def __init__(self, filters: dict, exclude: dict, or_: list):
        """

        Parameters
        ----------
        filters :
            A dictionary containing key-values that should be valid keyword arguments
            for Django `QuerySet`'s `.filter()` method. E.g this should work:

                `queryset.filter(**filters)`

        exclude :
            A dictionary containing key-values that should be valid keyword arguments
            for Django `QuerySet`'s `.exclude()` method. E.g this should work:

                `queryset.exclude(**exclude)`
        or_ :
            An optional list whose values are the same as described here - recursive. They are
            to be used to create union of queries.
        """
        self.filters = filters
        self.exclude = exclude
        self.or_ = or_
        self.children: List['Query'] = list()

        self._make_children()

    @property
    def n_children(self):
        return len(self.children)

    def _make_children(self):
        for data in self.or_:
            self.children.append(Query(**data))

    def _q(self) -> models.Q:
        filter_q = models.Q(**self.filters)
        if not self.exclude:
            return filter_q
        return filter_q & ~models.Q(**self.exclude)

    def apply_to_queryset(self, queryset: models.QuerySet, use_q=False):
        if self.n_children == 0:
            if not use_q:
                queryset = queryset.filter(**self.filters)
                if self.exclude:
                    queryset = queryset.exclude(**self.exclude)
                return queryset
            return self._q()
        if use_q:
            return self._q()
        queries = [self._q()] + [c.apply_to_queryset(queryset=queryset, use_q=True) for c in self.children]
        return queryset.filter(reduce(operator.or_, queries))


