from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey


class Projects(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=2048)
    type = models.CharField(max_length=255)
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Contributors(models.Model):
    
    CHOICES =(
    ("1", "Author"),
    ("2", "Contributor"),
    ("3", "Other"),
    )
  
    user_id = models.ManyToManyField(User)
    project_id = models.ManyToManyField(Projects)
    permission = models.CharField(choices=CHOICES, max_length=3)
    role = models.CharField(max_length=255)


class Issues(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=2048)
    tag = models.CharField(max_length=50)
    priority = models.CharField(max_length=50)
    project_id = models.ForeignKey(Projects, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    author_user_id = models.ForeignKey(User, related_name='author', on_delete=models.DO_NOTHING)
    assignee_user_id = models.ForeignKey(User, related_name='assignee', on_delete=models.DO_NOTHING)
    created_time = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    description = models.CharField(max_length=2048)
    author_user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    issue_id = models.ForeignKey(Issues, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)