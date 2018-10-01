import typing
import re
import json

from django.db import models
from django.urls import path
from django.core.paginator import Paginator
from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rests.core.utils.subset_serializer import subset_serializer
from rests.interface.query import Query


# =================================
# Types
# ---------------------------------

# Predefine this type so we don't make a mess of the init signature.
PermissionClasses = typing.Optional[typing.Tuple[typing.Type[BasePermission]]]


# =================================
# Type
# ---------------------------------

class Type(object):

    """
    Class for representing an interface 'Type' - a single Django Model.

    """

    def __init__(self, serializer_cls: typing.Type[serializers.ModelSerializer],
                 create_permissions: PermissionClasses=None, get_permissions: PermissionClasses=None,
                 delete_permissions: PermissionClasses=None, update_permissions: PermissionClasses=None):
        """


        Parameters
        ----------
        serializer_cls :
            The `rest_framework` `ModelSerializer` for this interface Type.
        create_permissions :
            An optional tuple of `rest_framework` permission classes to use for the
            `create` view of this Type.
        get_permissions :
            An optional tuple of `rest_framework` permission classes to use for the
            `get` and `list` view of this Type.
        delete_permissions :
            An optional tuple of `rest_framework` permission classes to use for the
            `delete` view of this Type.
        update_permissions :
            An optional tuple of `rest_framework` permission classes to use for the
            `update` view of this Type.
        """
        self.serializer_cls = serializer_cls
        self.create_permissions = create_permissions
        self.get_permissions = get_permissions
        self.delete_permissions = delete_permissions
        self.update_permissions = update_permissions

    def urlpatterns(self):
        """
        Create the Django URL patterns for this interface Type.

        :return:
        """
        urlpatterns = [
            path('', self._list_view(), name='list'),
            path('<pk>/get/', self._get_view(), name='get'),
            path('<pk>/update/', self._update_view(), name='update'),
            path('<pk>/delete/', self._delete_view(), name='delete'),
            path('create/', self._create_view(), name='create'),
        ]
        return urlpatterns

    def _get_view(self):
        """
        Make and return view function for retrieving data.

        """

        def get_view(request, pk):
            instance = self.model_cls.objects.get(pk=pk)
            serializer = self._get_serializer(instance)
            return Response(serializer.data)
        if self.get_permissions:
            get_view.permission_classes = self.get_permissions

        return api_view(['GET'])(get_view)

    def _create_view(self):
        """
        Make and return view function for creating object of this Type.

        """

        def create_view(request):
            serializer = self._get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if self.create_permissions:
            create_view.permission_classes = self.create_permissions

        return api_view(['POST'])(create_view)

    def _update_view(self):
        """
        Make and return view function for updating object of this Type.

        """
        def update_view(request, pk):
            instance = self.model_cls.objects.get(pk=pk)
            serializer = self._get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.update(instance=instance, validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if self.update_permissions:
            update_view.permission_classes = self.update_permissions

        return api_view(['POST'])(update_view)

    def _list_view(self):
        """
        Make and return list view function for retrieving/filtering lists of
        model instances. The view itself accepts a url parameter - `query=...`
        containing a JSON serialized query. If provided, this is handled by the
        `interface.Query` class.

        """
        def list_view(request: Request):
            query_json = request.query_params.get('query')
            fields_json = request.query_params.get('fields')
            page_num = request.query_params.get('page')
            page_size = request.query_params.get('pagesize', 25)
            queryset = self.queryset()

            # If no query is provided, all objects will be returned.
            if query_json:
                # Todo: find root cause of this.
                query_json = query_json.replace(u'\ufeff', '')
                query_data = json.loads(query_json)
                query = Query(**query_data)
                queryset = query.apply_to_queryset(queryset=queryset)

            # If fields are provided, subset the serializer fields accordingly.

            if page_num:
                paginator = Paginator(queryset, page_size)
                num_results = paginator.count
                num_pages = paginator.num_pages
                queryset = paginator.get_page(number=page_num)

            if fields_json:
                fields = json.loads(fields_json)
                serializer_cls = subset_serializer(select_fields=fields, serializer_cls=self.serializer_cls)
                serializer = serializer_cls(queryset, many=True)
            else:
                serializer = self._get_serializer(queryset, many=True)

            if page_num:
                return Response({
                    'num_results': num_results,
                    'num_pages': num_pages,
                    'data': serializer.data
                })

            return Response(serializer.data, status=status.HTTP_200_OK)

        # 'Get' permissions are treated as equivalent to 'list' permissions.
        if self.get_permissions:
            list_view.permission_classes = self.get_permissions

        return api_view(['GET'])(list_view)

    def _delete_view(self):
        """
        Make and return the delete view function.

        """
        def delete_view(request, pk):
            instance = self.model_cls.objects.get(pk=pk)
            instance.delete()
            return Response({}, status=status.HTTP_200_OK)

        if self.delete_permissions:
            delete_view.permission_classes = self.delete_permissions

        return api_view(['DELETE'])(delete_view)

    @property
    def model_cls(self):
        return self.serializer_cls.Meta.model

    def queryset(self) -> models.QuerySet:
        return self.model_cls.objects.all()

    @property
    def model_name(self):
        return self.model_cls.__name__

    @property
    def base_url(self):
        """
        Return the 'base url' for this interface `Type`. For a model `CamelCase`,
        this will return `camel-case`.

        """
        matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', self.model_name)
        return "-".join([m.group(0).lower() for m in matches])

    def _get_serializer(self, *args, **kwargs):
        return self.serializer_cls(*args, **kwargs)