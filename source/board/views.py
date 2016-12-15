from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import get_user_model

from rest_framework import viewsets
from rest_framework.response import Response

from .models import Sprint, Task
from .serializers import SprintSerializer, TaskSerializer, UserSerializer
from .forms import TaskFilter, SprintFilter
from .mixins import DefaultsMixin

from .tasks import say_hi


User = get_user_model()

# class ProductFilter(django_filters.rest_framework.FilterSet):
#     min_price = django_filters.NumberFilter(name="price", lookup_expr='gte')
#     max_price = django_filters.NumberFilter(name="price", lookup_expr='lte')
#     class Meta:
#         model = Product
#         fields = ['category', 'in_stock', 'min_price', 'max_price']


class SprintViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Sprint.objects.order_by('end')
    serializer_class = SprintSerializer
    search_fields = ('name',)
    ordering_fields = ('end', 'name',)


class TaskViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer    
    search_fields = ('name', 'description',)
    ordering_fields = ('name', 'order', 'started', 'due', 'completed',)
    filter_fields = ('order', 'sprint',)
    # filter_class = TaskFilter
    ordering = ('name',)


class UserViewSet(DefaultsMixin, viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.order_by(User.USERNAME_FIELD)
    serializer_class = UserSerializer

    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD

    search_fields = (User.USERNAME_FIELD,)    