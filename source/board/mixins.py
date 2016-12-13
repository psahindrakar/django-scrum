from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import get_user_model

from rest_framework import authentication, permissions, filters
from rest_framework.response import Response


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

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)    

    def get_serializer_context(self):
        kwargs = {}
        param_key = 'fields'
        if param_key in self.request.query_params.keys():
            val = set(self.request.query_params[param_key].split(","))
            kwargs[param_key] = val
        return kwargs

    # def get_serializer_context(self):
    #     kwargs = {}                     # defining an empty set
    #     param_key = 'fields'
    #     if param_key in self.request.query_params.keys():
    #         val = set(self.request.query_params[param_key].split(","))
    #         kwargs[param_key] = val
    #     return kwargs


    maximum_page_size = 500
    default_page_size = 10
    default_page_no = 1
    page_size = default_page_size
    page_no = default_page_no
    total_pages = 0

    def paginate_queryset(self, queryset):
        request = self.request
        param_key = 'page_size'        
        if param_key in request.query_params.keys():
            val = request.query_params[param_key]
            try:
                self.page_size = int(val) if self.maximum_page_size > int(val) else self.maximum_page_size
            except ValueError:
                self.page_size = self.maximum_page_size            

        param_key = 'page_no'        
        if param_key in request.query_params.keys():
            val = request.query_params[param_key]
            try:
                self.page_no = int(val)
            except ValueError:
                self.page_no = self.default_page_no
                
        paginator = Paginator(queryset, self.page_size)

        emptyPage = False
        try:
            page = paginator.page(self.page_no)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results by paginator.page(paginator.num_pages)
            # or emply result can be returned
            emptyPage = True
            page = []

        self.total_pages = paginator.num_pages        
        return page

    
    def get_paginated_response(self, data):
        return Response({
            'current_count': len(data),
            'page_size': self.page_size,
            'page_no': self.page_no,
            'total_pages': self.total_pages,
            'list' : data 
        })
