from django.urls import path

from api import views

urlpatterns = [
    path('login/', views.LoginAPI.as_view()),
    path('register/', views.RegisterUserAPI.as_view()),
    path('todos/', views.TodoListAPI.as_view(), name='todos'),
    path('todos/add/', views.TodoCreateAPI.as_view()),
    path('todos/<int:pk>/', views.TodoDetailAPI.as_view()),
]