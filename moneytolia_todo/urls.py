from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
    path('', include_docs_urls(title='Moneytolia To-Do API'))
]
