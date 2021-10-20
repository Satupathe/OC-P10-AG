from rest_framework import serializers
from django.contrib import auth
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import AuthenticationFailed
from .models import Users



class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=Users.objects.all())]
            )
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = Users
        fields = ['first_name', 'last_name', 'email', 'password']

    def validate(self, attrs):
        first_name=attrs.get('first_name', '')
        last_name=attrs.get('last_name', '')

        if not first_name.isalnum():
            raise serializers.ValidationError('the first name should only contain alphanumerics characters') 
        
        elif not last_name.isalnum():
            raise serializers.ValidationError('the first name should only contain alphanumerics characters') 

        return attrs

    def create(self, validated_data):
        if validated_data['first_name'] is None:
            raise TypeError('Users should have a first_name')
        if validated_data['last_name'] is None:
            raise TypeError('Users should have a last_name')
        if validated_data['email'] is None:
            raise TypeError('Users should have a Email')
        user = super(RegisterSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = Users.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = Users
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = Users.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)

        if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens()
        }

        return super().validate(attrs)