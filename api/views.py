from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework import views
from rest_framework.response import Response

from django.contrib.auth import login

from .serializers import LoginSerializer, RegisterSerializer, TodoSerializer
from todos.models import Todo


class LoginAPI(generics.CreateAPIView):
    '''
    View for user authentication.

    * Requires token authentication.
    ** All users are able to access this view.
    '''
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer
    # authentication_classes = ()
    
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
    View for register new user.
    '''
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class TodoCreateAPI(generics.CreateAPIView):
    '''
    View for add new todo item for authenticated user.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TodoSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TodoListAPI(generics.ListAPIView):
    '''
    View for list all todo items for authenticated user.
    '''
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TodoSerializer

    def get_queryset(self):
        todos = Todo.objects.filter(user=self.request.user)
        return todos


class TodoDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
