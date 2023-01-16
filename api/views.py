import random

from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth import login

from .serializers import LoginSerializer, RegisterSerializer, TodoSerializer
from todos.models import Todo


class LoginAPI(generics.CreateAPIView):
    '''
    User login.
    '''
    name = 'Login'
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer
    
    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data,
            context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        print(user)
        login(request, user)

        return Response(None, status=status.HTTP_202_ACCEPTED)


class RegisterUserAPI(generics.CreateAPIView):
    '''
    Register new user.
    '''
    name = 'Register'
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class TodoCreateAPI(generics.CreateAPIView):
    '''
    Create a new todo record for authenticated user.
    '''
    name = 'Add To-do Item'
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TodoSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TodoListAPI(generics.ListAPIView):
    '''
    List all todo records for authenticated user.
    '''
    name = 'To-do\'s'
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TodoSerializer

    def get_queryset(self):
        todos = Todo.objects.filter(user=self.request.user)
        return todos


class TodoDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    '''
    Get, edit or delete a specific todo record 
    of authenticated user.
    '''
    name = 'To-do Detail'
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TodoSerializer

    def get_queryset(self):
        todos = Todo.objects.filter(user=self.request.user)
        return todos


class RandomTodoDetailAPI(generics.RetrieveAPIView):
    '''
    Get a random todo record of authenticated user.
    '''
    name = 'Random To-do'
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TodoSerializer

    def get_object(self):
        todos = Todo.objects.filter(
            user=self.request.user).values_list('pk', flat=True)
        random_pk = random.choice(todos)
        random_todo = Todo.objects.get(pk=random_pk)
        return random_todo
