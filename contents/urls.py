from django.urls import re_path

from contents.views import (
    WantedContentAPIView,
    WantedContentDetailsAPIView,
    WantedUrlAPIView,
    WantedUrlDetailsAPIView,
    WantedDataAPIView,
    WantedDataDetailsAPIView,
    NaverContentAPIView,
    NaverContentDetailsAPIView,
    NaverDataAPIView,
    NaverDataDetailsAPIView,
)

urlpatterns = [
    re_path(r'^job_contents/$', WantedContentAPIView.as_view(), name='job-contents'),
    re_path(r'^job_contents/(?P<pk>[\w.@+-]+)/$', WantedContentDetailsAPIView.as_view(), name='job-contents-details'),
    re_path(r'^wanted_url/$', WantedUrlAPIView.as_view(), name='wanted-url'),
    re_path(r'^wanted_url/(?P<pk>[\w.@+-]+)/$', WantedUrlDetailsAPIView.as_view(), name='wanted-url-details'),
    re_path(r'^wanted_data/$', WantedDataAPIView.as_view(), name='wanted-data'),
    re_path(r'^wanted_data/(?P<pk>[\w.@+-]+)/$', WantedDataDetailsAPIView.as_view(), name='wanted-data-details'),
    re_path(r'^naver_contents/$', NaverContentAPIView.as_view(), name='naver-contents'),
    re_path(r'^naver_contents/(?P<pk>[\w.@+-]+)/$', NaverContentDetailsAPIView.as_view(), name='naver-contents-details'),
    re_path(r'^naver_data/$', NaverDataAPIView.as_view(), name='naver-data'),
    re_path(r'^naver_data/(?P<pk>[\w.@+-]+)/$', NaverDataDetailsAPIView.as_view(), name='naver-data-details'),
]
