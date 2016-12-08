from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import get_user_model

from rest_framework import viewsets, authentication, permissions, filters
from rest_framework.response import Response

from .models import Sprint, Task
from .serializers import SprintSerializer, TaskSerializer, UserSerializer
from .forms import TaskFilter, SprintFilter

User = get_user_model()


class DefaultsMixin(object):                                                  
    authentication_classes = ( 
        authentication.BasicAuthentication, 
        authentication.TokenAuthentication, 
    ) 
    permission_classes = ( 
        permissions.IsAuthenticated, 
    )
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

    def getFieldsInKwargs(self, request):
        kwargs = {}                     # defining an empty set
        param_key = 'fields'
        if param_key in request.query_params.keys():
            val = set(request.query_params[param_key].split(","))
            kwargs[param_key] = val
        return kwargs

    
    def getPaginatedResult(self, request):
        maximum_page_size = 500
        default_page_size = 10
        default_page_no = 1

        param_key = 'page_size'
        page_size = default_page_size
        if param_key in request.query_params.keys():
            val = request.query_params[param_key]
            try:
                page_size = int(val) if maximum_page_size > int(val) else maximum_page_size
            except ValueError:
                page_size = maximum_page_size            

        param_key = 'page_no'
        page_no = default_page_no
        if param_key in request.query_params.keys():
            val = request.query_params[param_key]
            try:
                page_no = int(val)
            except ValueError:
                page_no = default_page_no
                
        paginator = Paginator(self.queryset, page_size)

        emptyPage = False
        try:
            page = paginator.page(page_no)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results by paginator.page(paginator.num_pages)
            # or emply result can be returned
            emptyPage = True
            page = []

        pages = {
            "current_count" : 0 if emptyPage else len(page.object_list),
            "size" : page_size,
            "index" : page_no,
            "total_count" : paginator.num_pages,
            "page" : page
        }
        return pages


    def list(self, request, *args, **kwargs):
        kwargs = self.getFieldsInKwargs(request)
        pages = self.getPaginatedResult(request)
        
        serializer = TaskSerializer(pages["page"], many=True, **kwargs)
        res_data = {
            "current_count": pages["current_count"],
            "page_size": pages["size"],
            "page_no": pages["index"],
            "total_pages": pages["total_count"],
            "list" : serializer.data
        }
        return Response(res_data)


class UserViewSet(DefaultsMixin, viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.order_by(User.USERNAME_FIELD)
    serializer_class = UserSerializer

    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD

    search_fields = (User.USERNAME_FIELD,)    