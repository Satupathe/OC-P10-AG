from rest_framework import serializers
from django.contrib import auth
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import AuthenticationFailed
from .models import Users, Projects, Contributors, Issues, Comments 



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


class ContributorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributors
        fields = ['user_id', 'permission']


class ProjectsDetailsSerializer(serializers.ModelSerializer):
    contributors = ContributorsSerializer(many=True)
    class Meta:
        model = Projects
        fields = ['title', 'id', 'author_user_id', 'type', 'description', 'contributors']