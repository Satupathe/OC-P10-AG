from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from rest_framework_simplejwt.tokens import RefreshToken


class Users(AbstractBaseUser, PermissionsMixin, BaseUserManager):
    username = None
    first_name = models.CharField(max_length=255, unique=True, db_index=True)
    last_name = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return self.email

    def create_user(self, first_name, last_name, email, password=None):
        if first_name is None:
            raise TypeError('Users should have a first_name')
        if last_name is None:
            raise TypeError('Users should have a last_name')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(first_name=first_name, last_name=last_name, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


class Projects(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=2048)
    type = models.CharField(max_length=255)
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = 'project_author', default='', on_delete=models.CASCADE)
    

class Contributors(models.Model):
    
    CHOICES =[
    ("1", "Author"),
    ("2", "Contributor"),
    ]
  
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='users',default='', on_delete=models.CASCADE)
    project_id = models.ForeignKey(Projects, related_name='contributor_project', default='', on_delete=models.CASCADE)
    permission = models.CharField(choices=CHOICES, max_length=2)
    role = models.CharField(max_length=255)


class Issues(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=2048)
    tag = models.CharField(max_length=50)
    priority = models.CharField(max_length=50)
    project_id = models.ForeignKey(Projects, default='', on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='author', default='', on_delete=models.DO_NOTHING)
    assignee_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='assignee', default='', on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    description = models.CharField(max_length=2048)
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comment_author', default='' ,on_delete=models.DO_NOTHING)
    issue_id = models.ForeignKey(Issues, default='', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)