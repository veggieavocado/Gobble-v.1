from django.shortcuts import render
from rest_framework import permissions, generics
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from molecular.settings import PRODUCTION

from contents.models import (
    WantedContent,
    WantedUrl,
    WantedData,
    NaverContent,
    NaverData,
    KreditJobContent,
    GoogleTrendsContent,
    )

from contents.serializers import (
    WantedContentSerializer,
    WantedUrlSerializer,
    WantedDataSerializer,
    NaverDataSerializer,
    NaverContentSerializer,
    KreditJobContentSerializer,
    GoogleTrendsContentSerializer,
)

from utils.paginations import StandardResultPagination


# WantedContent view GET POST
class WantedContentAPIView(generics.ListCreateAPIView):
    queryset = WantedContent.objects.using('contents').all()
    serializer_class = WantedContentSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        if PRODUCTION == True:
            queryset = WantedContent.objects.using('contents').all().order_by('id')
        else:
            queryset = WantedContent.objects.all().order_by('id')
        title_by = self.request.GET.get('title')
        company_by = self.request.GET.get('company')
        loaction_by = self.request.GET.get('location')
        created_by = self.request.GET.get('created')

        if title_by:
            queryset = queryset.filter(title=title_by)
        if company_by:
            queryset = queryset.filter(company=company_by)
        if loaction_by:
            queryset = queryset.filter(location=loaction_by)
        if created_by:
            queryset = queryset.filter(location=created_by)
        return queryset

    def perform_create(self, serializer):
        # reference: https://stackoverflow.com/questions/44218424/django-rest-framework-how-to-post-when-using-listcreateapiview
        data = self.request.data
        data_inst = WantedContent(title=data['title'],
                                  company=data['company'],
                                  location=data['location'],
                                  url=data['url'],
                                  content=data['content'],)
        data_inst.save(using='contents')


# WantedContent view PUT DELETE
class WantedContentDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    if PRODUCTION == True:
        queryset = WantedContent.objects.using('contents').all()
    else:
        queryset = WantedContent.objects.all()
    serializer_class = WantedContentSerializer
    permission_classes = (permissions.AllowAny,)


# WantedUrl view GET POST
class WantedUrlAPIView(generics.ListCreateAPIView):
    if PRODUCTION == True:
        queryset = WantedUrl.objects.using('contents').all().order_by('id')
    else:
        queryset = WantedUrl.objects.all().order_by('id')
    serializer_class = WantedUrlSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def perform_create(self, serializer):
        # reference: https://stackoverflow.com/questions/44218424/django-rest-framework-how-to-post-when-using-listcreateapiview
        data = self.request.data
        data_inst = WantedUrl(urls=data['urls'])
        data_inst.save(using='contents')


# Wantedurl view PUT DELETE
class WantedUrlDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    if PRODUCTION == True:
        queryset = WantedUrl.objects.using('contents').all()
    else:
        queryset = WantedUrl.objects.all()
    serializer_class = WantedUrlSerializer
    permission_classes = (permissions.AllowAny,)

# WantedUrl view GET POST
class WantedDataAPIView(generics.ListCreateAPIView):
    if PRODUCTION == True:
        queryset = WantedData.objects.using('contents').all().order_by('id')
    else:
        queryset = WantedData.objects.all().order_by('id')
    serializer_class = WantedDataSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        if PRODUCTION == True:
            queryset = WantedData.objects.using('contents').all().order_by('id')
        else:
            queryset = WantedData.objects.all().order_by('id')
        data_by = self.request.GET.get('data_name')

        if data_by:
            queryset = queryset.filter(title=data_by)
        return queryset

    def perform_create(self, serializer):
        # reference: https://stackoverflow.com/questions/44218424/django-rest-framework-how-to-post-when-using-listcreateapiview
        data = self.request.data
        data_inst = WantedData(data_name=data['data_name'],
                               data=data['data'],)
        data_inst.save(using='contents')


# Wantedurl view PUT DELETE
class WantedDataDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    if PRODUCTION == True:
        queryset = WantedData.objects.using('contents').all()
    else:
        queryset = WantedData.objects.all()
    serializer_class = WantedDataSerializer
    permission_classes = (permissions.AllowAny,)


# WantedContent view GET POST
class NaverContentAPIView(generics.ListCreateAPIView):
    if PRODUCTION == True:
        queryset = NaverContent.objects.using('contents').all()
    else:
        queryset = NaverContent.objects.all()
    serializer_class = NaverContentSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        if PRODUCTION == True:
            queryset = NaverContent.objects.using('contents').all().order_by('id')
        else:
            queryset = NaverContent.objects.all().order_by('id')
        title_by = self.request.GET.get('title')
        media_by = self.request.GET.get('media')
        data_type_by = self.request.GET.get('data_type')
        if title_by:
            queryset = queryset.filter(title=title_by)
        if media_by:
            queryset = queryset.filter(media=media_by)
        if data_type_by:
            queryset = queryset.filter(data_type=data_type_by)
        return queryset

    def perform_create(self, serializer):
        # reference: https://stackoverflow.com/questions/44218424/django-rest-framework-how-to-post-when-using-listcreateapiview
        data = self.request.data
        data_inst = NaverContent(title=data['title'],
                                 media=data['media'],
                                 upload_time=data['upload_time'],
                                 url=data['url'],
                                 content=data['content'],
                                 data_type=data['data_type'],)
        data_inst.save(using='contents')


# WantedContent view PUT DELETE
class NaverContentDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    if PRODUCTION == True:
        queryset = NaverContent.objects.using('contents').all()
    else:
        queryset = NaverContent.objects.all()
    serializer_class = NaverContentSerializer
    permission_classes = (permissions.AllowAny,)


class NaverDataAPIView(generics.ListCreateAPIView):
    if PRODUCTION == True:
        queryset = NaverData.objects.using('contents').all().order_by('id')
    else:
        queryset = NaverData.objects.all().order_by('id')
    serializer_class = NaverDataSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def perform_create(self, serializer):
        # reference: https://stackoverflow.com/questions/44218424/django-rest-framework-how-to-post-when-using-listcreateapiview
        data = self.request.data
        data_inst = NaverData(data_name=data['data_name'],
                              data=data['data'])
        data_inst.save(using='contents')


# Wantedurl view PUT DELETE
class NaverDataDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    if PRODUCTION == True:
        queryset = NaverData.objects.using('contents').all()
    else:
        queryset = NaverData.objects.all()
    serializer_class = NaverDataSerializer
    permission_classes = (permissions.AllowAny,)


# KreditJobContent view GET POST
class KreditJobContentAPIView(generics.ListCreateAPIView):
    if PRODUCTION == True:
        queryset = KreditJobContent.objects.using('contents').all()
    else:
        queryset = KreditJobContent.objects.all()
    serializer_class = KreditJobContentSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        if PRODUCTION == True:
            queryset = KreditJobContent.objects.using('contents').all().order_by('id')
        else:
            queryset = KreditJobContent.objects.all().order_by('id')
        created_by = self.request.GET.get('created')
        company_by = self.request.GET.get('company')
        location_by = self.request.GET.get('location')

        if created_by:
            queryset = queryset.filter(title=created_by)
        if company_by:
            queryset = queryset.filter(media=company_by)
        if location_by:
            queryset = queryset.filter(media=location_by)
        return queryset

    def perform_create(self, serializer):
        # reference: https://stackoverflow.com/questions/44218424/django-rest-framework-how-to-post-when-using-listcreateapiview
        data = self.request.data
        data_inst = KreditJobContent(company=data['company'],
                                     industry=data['industry'],
                                     location=data['location'],
                                     starting_income=data['starting_income'],
                                     average_income=data['average_income']) # data.average_income과 같은 형식 적용 안 됨
        data_inst.save(using='contents')


# KreditJobContent view GET POST
class KreditJobContentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    if PRODUCTION == True:
        queryset = KreditJobContent.objects.using('contents').all()
    else:
        queryset = KreditJobContent.objects.all()
    serializer_class = KreditJobContentSerializer
    permission_classes = (permissions.AllowAny,)


# KreditJobContent view GET POST
class GoogleTrendsContentAPIView(generics.ListCreateAPIView):
    if PRODUCTION == True:
        queryset = GoogleTrendsContent.objects.using('contents').all()
    else:
        queryset = GoogleTrendsContent.objects.all()
    serializer_class = GoogleTrendsContentSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = StandardResultPagination
    filter_backends = [SearchFilter, OrderingFilter]

    def get_queryset(self, *args, **kwargs):
        if PRODUCTION == True:
            queryset = GoogleTrendsContent.objects.using('contents').all().order_by('id')
        else:
            queryset = GoogleTrendsContent.objects.all().order_by('id')
        created_by = self.request.GET.get('created')
        keyword_by = self.request.GET.get('keyword')

        if created_by:
            queryset = queryset.filter(title=created_by)
        if keyword_by:
            queryset = queryset.filter(media=keyword_by)
        return queryset

    def perform_create(self, serializer):
        # reference: https://stackoverflow.com/questions/44218424/django-rest-framework-how-to-post-when-using-listcreateapiview
        data = self.request.data
        data_inst = GoogleTrendsContent(keyword=data['keyword'],
                                        starting_date=data['starting_date'],
                                        end_date=data['end_date'],
                                        data=data['data'])
        data_inst.save(using='contents')


# KreditJobContent view GET POST
class GoogleTrendsContentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    if PRODUCTION == True:
        queryset = GoogleTrendsContent.objects.using('contents').all()
    else:
        queryset = GoogleTrendsContent.objects.all()
    serializer_class = GoogleTrendsContentSerializer
    permission_classes = (permissions.AllowAny,)
