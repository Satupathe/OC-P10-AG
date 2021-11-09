from django.db.models import Q
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from .serializers import (CommentsSerializer,
                          RegisterSerializer,
                          ProjectsDetailsSerializer,
                          ContributorsSerializer,
                          IssuesSerializer
                          )
from .models import Users, Projects, Contributors, Issues, Comments
from .permissions import (IsAuthenticatedProjectAuthor,
                          IsCommentAuthor,
                          IsIssueAuthorOrAssignee,
                          IsProjectAuthorOrContributor
                          )


class UserCreate(generics.GenericAPIView):
    """Registration class to save new users"""
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)


class ProjectsViewset(ModelViewSet):

    """
    Only authenticated users can access this view
    Allow to get project list or only one project related to the authenticated user
    If user is a project author, this view allow to manage this project
    """
    serializer_class = ProjectsDetailsSerializer
    permission_classes = [IsAuthenticatedProjectAuthor]

    @action(methods=['get'], detail=True)
    def get_queryset(self):
        return Projects.objects.filter(Q(author_user_id=self.request.user)
                                       | Q(contributor_project__user_id=self.request.user))

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["author_user_id"] = request.user.pk
        # request.data[] ?????????????????????????
        request.POST._mutable = False
        return super(ProjectsViewset, self).create(request, *args, *kwargs)

    @action(methods=['put'], detail=True)
    def modify(self, request, pk=None, *args, **kwargs):
        return super(ProjectsViewset, self).update(request, **args, **kwargs)

    @action(methods=['delete'], detail=True)
    def delete(self, request):
        return super(ProjectsViewset, self).delete()


class ContributorsViewset(ModelViewSet):
    """
    Only authenticated users and a project members can access this view
    Allow to get contributor list or only one contributor related to a specific project
    If user is a project author, this view allow to manage contributors
    """
    serializer_class = ContributorsSerializer
    permission_classes = [IsProjectAuthorOrContributor]

    @action(methods=['get'], detail=True)
    def get_queryset(self):
        try:
            contributors_list = Contributors.objects.filter(project_id=self.kwargs.get('projects_pk'))
            return contributors_list
        except :
            return ('This project number does not exist')

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["project_id"] = kwargs['projects_pk']
        request.POST._mutable = False
        return super(ContributorsViewset, self).create(request, *args, *kwargs)

    @action(methods=['delete'], detail=True)
    def delete(self, request):

        return super(ContributorsViewset, self).delete()

      
class IssuesViewset(ModelViewSet):
    """
    Only authenticated users and a project members can access this view
    Allow to get issues list or only one issue related to a specific project
    If user is a issue author, this view allow to manage this issue
    """
    serializer_class = IssuesSerializer
    permission_classes = [IsIssueAuthorOrAssignee]


    @action(methods=['get'], detail=True)
    def get_queryset(self):
        return Issues.objects.filter(project_id=self.kwargs.get('projects_pk'))

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["project_id"] = kwargs['projects_pk']
        request.data["author_user_id"] = request.user.pk
        request.data["assignee_user_id"] = Users.objects.get(id=request.data["assignee_user_id"]).pk
        request.POST._mutable = False
        return super(IssuesViewset, self).create(request, *args, *kwargs)


    @action(methods=['put'], detail=True)
    def modify(self, request, pk=None, *args, **kwargs):
        request.PUT._mutable = True
        request.data["assignee_user_id"] = Users.objects.get(id=request.data["assignee_user_id"]).pk
        request.PUT._mutable = False
        return super(IssuesViewset, self).update(request, **args, **kwargs)

    @action(methods=['delete'], detail=True)
    def delete(self, request):
        return super(IssuesViewset, self).delete()


class CommentsViewset(ModelViewSet):
    """
    Only authenticated users and an issue members can access this view
    Allow to get comments list or only one comment related to a specific issue
    If user is a comment author, this view allow to manage this comment
    """
    serializer_class = CommentsSerializer
    permission_classes = [IsCommentAuthor]

    @action(methods=['get'], detail=True)
    def get_queryset(self):
        return Comments.objects.filter(issue_id=self.kwargs.get('issues_pk'))

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["issue_id"] = kwargs['issues_pk']
        request.data["author_user_id"] = request.user.pk
        request.POST._mutable = False
        return super(CommentsViewset, self).create(request, *args, *kwargs)

    @action(methods=['put'], detail=True)
    def modify(self, request, pk=None, *args, **kwargs):

        return super(CommentsViewset, self).update(request, **args, **kwargs)

    @action(methods=['delete'], detail=True)
    def delete(self, request):
        return super(CommentsViewset, self).delete()
