from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth import login

from .serializers import LoginSerializer, RegisterSerializer


class LoginAPI(generics.CreateAPIView):
    '''
    View to login.

    * Requires token authentication.
    ** All users are able to access this view.
    '''
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer
    
    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data,
            context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)

        return Response(None, status=status.HTTP_202_ACCEPTED)


class RegisterUserAPI(generics.CreateAPIView):
    '''
    View to register new user.
    '''
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
