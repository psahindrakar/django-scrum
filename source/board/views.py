from django.contrib.auth import get_user_model
from rest_framework import viewsets, authentication, permissions, filters

from rest_framework.pagination import PageNumberPagination

from .models import Sprint, Task
from .serializers import SprintSerializer, TaskSerializer, UserSerializer
from .forms import TaskFilter, SprintFilter

User = get_user_model()

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100                         # Default page size for pagination
    page_size_query_param = 'page_size'     # A query parameter variable name for page page_size
    max_page_size = 1000                    # Maximum page size which is to be allowed on a list view


class DefaultsMixin(object):                                                  
    authentication_classes = ( 
        authentication.BasicAuthentication, 
        authentication.TokenAuthentication, 
    ) 
    permission_classes = ( 
        permissions.IsAuthenticated, 
    ) 
    paginate_by = 25  
    paginate_by_param = 'page_size'  
    max_paginate_by = 100
    filter_backends = (
        filters.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )


class SprintViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Sprint.objects.order_by('end')
    serializer_class = SprintSerializer
    # filter_class = SprintFilter
    search_fields = ('name',)
    ordering_fields = ('end', 'name',)


class TaskViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # filter_class = TaskFilter
    search_fields = ('name', 'description',)
    ordering_fields = ('name', 'order', 'started', 'due', 'completed',)
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        kwargs = {}                                                 # defining an empty set for fields
        param_key = 'fields'
        if param_key in request.query_params.keys():
            val = set(request.query_params[param_key].split(","))
            kwargs[param_key] = val

        serializer = TaskSerializer(many=True, **kwargs)


class UserViewSet(DefaultsMixin, viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.order_by(User.USERNAME_FIELD)
    serializer_class = UserSerializer

    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD

    search_fields = (User.USERNAME_FIELD,)    