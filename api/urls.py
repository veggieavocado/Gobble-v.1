from django.urls import path

from api.views import (
    TaskAPIView,
    AlgorithmTestAPIView,
    TestAPIView,
    WantedPageDataAPIView,
)

urlpatterns = [
    path('test/', TestAPIView.as_view(), name='test'),
    path('algo_test/', AlgorithmTestAPIView.as_view(), name='algo_test'),
    path('', TaskAPIView.as_view(), name='task'),
    path('wanted_page_data', WantedPageDataAPIView.as_view(), name='wanted_page_data'),
]
