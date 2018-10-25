from typing import Type, List, Iterable

from django.db import models
from django.core.exceptions import FieldDoesNotExist
from rest_framework import serializers


class Field(object):

    def names(self) -> Iterable[str]:
        raise NotImplementedError

    def interface_type_declarations(self) -> Iterable[str]:
        """
        Return the `interface` type declarations for this field. This will be used
        to generate the `<model_name>Data` TypeScript interface.


        """
        raise NotImplementedError

    def cls_type_declarations(self) -> Iterable[str]:
        """
        Return the class property declarations for this field. This will be used
        to declare the names/types for this field for its TypeScript Model class.

        """
        raise NotImplementedError