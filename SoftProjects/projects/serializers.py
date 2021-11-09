from rest_framework import serializers
from rest_framework.validators import UniqueValidator
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
        first_name = attrs.get('first_name', '')
        last_name = attrs.get('last_name', '')

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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['first_name', 'last_name']


class ContributorsSerializer(serializers.ModelSerializer):
    CHOICES = [("1", "Author"),
               ("2", "Contributor"),
               ]
    permission = serializers.MultipleChoiceField(choices=CHOICES)


class ContributorsSerializer(serializers.ModelSerializer):
    CHOICES =[
    ("1", "Author"),
    ("2", "Contributor"),
    ]
    permission = serializers.MultipleChoiceField(choices=CHOICES)
    class Meta:
        model = Contributors
        fields = ['id', 'permission', 'role', 'user_id', 'project_id']


class ProjectsDetailsSerializer(serializers.ModelSerializer):

    contributors = ContributorsSerializer(source='contributor_project',
                                          required=False,
                                          allow_null=True,
                                          many=True
                                          )

    class Meta:
        model = Projects
        fields = ['title', 'id', 'author_user_id', 'type', 'description', 'contributors']


class IssuesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issues
        fields = ['title',
                  'project_id',
                  'author_user_id',
                  'tag',
                  'priority',
                  'status',
                  'assignee_user_id',
                  'description',
                  'created_time'
                  ]


class CommentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = ['description', 'issue_id', 'author_user_id', 'created_time']
