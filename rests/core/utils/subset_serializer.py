from typing import Type, List
from collections import OrderedDict


from rest_framework import serializers


# =================================
# Subset Serializer
# ---------------------------------

def subset_serializer(select_fields: List[str],
                      serializer_cls: Type[serializers.ModelSerializer]) -> Type[serializers.ModelSerializer]:

    """
    Return a serializer class containing only fields specified in `fields` argument.

    """

    class Meta:
        fields = select_fields
        model = serializer_cls.Meta.model

    serializer = serializer_cls()
    attrs = dict(Meta=Meta)
    _declared_fields = OrderedDict()

    for k, v in serializer_cls._declared_fields.items():
        if k in select_fields:
            _declared_fields[k] = v
    for k, v in serializer.get_fields().items():
        if k in select_fields:
            attrs[k] = v

    attrs['_declared_fields'] = _declared_fields

    subset_serializer_cls = type('SubsetSerializer', (serializer_cls,), attrs)
    return subset_serializer_cls
