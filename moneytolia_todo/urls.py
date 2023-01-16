from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
    path('', include_docs_urls(
        title='Moneytolia To-Do API',
        permission_classes=(AllowAny,))),
]
