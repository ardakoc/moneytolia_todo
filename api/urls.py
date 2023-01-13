from django.urls import path

from .views import LoginAPI, RegisterUserAPI

urlpatterns = [
    path('login/', LoginAPI.as_view()),
    path('register/', RegisterUserAPI.as_view()),
]