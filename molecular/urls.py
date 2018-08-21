from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # API URL
    path('gobble/api/v1/', include('api.urls')),

    # 컨텐츠 URL
    path('gobble/api/v1/contents/', include('contents.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
