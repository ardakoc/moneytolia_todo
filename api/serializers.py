from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

from todos.models import Todo


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        label='Username',
        help_text='Username',
        write_only=True
    )
    password = serializers.CharField(
        label='Password',
        help_text='Password',
        write_only=True,
        trim_whitespace=False,
        style={'input_type': 'password'}
    )
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                username=username, password=password)

            if not user:
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Username and password are required.'
            raise serializers.ValidationError(msg, code='authorization')
        
        attrs['user'] = user
        return attrs


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        help_text='Registration email',
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        help_text='Set a password',
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        help_text='Confirm your password',
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 
            'email', 'first_name', 'last_name'
        )
        extra_kwargs = {
            'first_name': {'required': True, 'help_text': 'Your first name'},
            'last_name': {'required': True, 'help_text': 'Your last name'}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': 'Password fields didn\'t match.'}
            )

        return attrs

    def create(self, validated_data):
        # validated_data['password'] = make_password(
        #     validated_data.get('password'))
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class TodoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Todo
        exclude = ('user',)
