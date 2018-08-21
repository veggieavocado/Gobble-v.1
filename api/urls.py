from django.urls import path

from api.views import (
    TaskAPIView,
    AlgorithmTestAPIView,
    TestAPIView,
)

urlpatterns = [
    path('test/', TestAPIView.as_view(), name='test'),
    path('algo_test/', AlgorithmTestAPIView.as_view(), name='task'),
    path('', TaskAPIView.as_view(), name='task'),
]
