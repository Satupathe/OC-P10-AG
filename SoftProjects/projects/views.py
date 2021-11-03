from django.http.request import QueryDict
from rest_framework import status, generics, permissions, filters, mixins, viewsets
from rest_framework.permissions import OR, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from .serializers import CommentsSerializer, RegisterSerializer, ProjectsDetailsSerializer, ContributorsSerializer, IssuesSerializer
from .models import Users, Projects, Contributors, Issues, Comments 
from .permissions import IsAuthor, IsContributor


class UserCreate(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        return Response(user_data, status=status.HTTP_201_CREATED)


class ProjectsViewset(ModelViewSet):
    serializer_class = ProjectsDetailsSerializer
    permission_classes = [IsAuthor]
    
    @action(methods=['get'], detail=True)
    def get_queryset(self):
        return Projects.objects.filter(author_user_id=self.request.user)
        #Supprimer le lien direct entre projects et user et passer par contributor pour l'auteur
        #instaurer correctement le choix multiple des permissions dans Contributors
        #Définir les permissions de permissions.py
    
    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["author_user_id"] = request.user.pk
        # request.data[] ?????????????????????????
        request.POST._mutable = False
        return super(ProjectsViewset, self).create(request, *args, *kwargs) # vérifier l'utilisation des étoiles

    @action(methods=['put'], detail=True)
    def modify(self, request, pk=None, *args, **kwargs):
        print('essai')
        print(request.user.pk)
        return super(ProjectsViewset, self).update(request, **args, **kwargs)

    @action(methods=['delete'], detail=True)
    def delete(self, request):
        print('essai')
        return super(ProjectsViewset, self).delete()


class ContributorsViewset(ModelViewSet):
    serializer_class = ContributorsSerializer
    permission_classes = [IsAuthor]

    @action(methods=['get'], detail=True)
    def get_queryset(self):
        print(self.kwargs)
        return Contributors.objects.filter(project_id=self.kwargs.get('projects_pk'))

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["project_id"] = kwargs['projects_pk']
        request.POST._mutable = False
        return super(ContributorsViewset, self).create(request, *args, *kwargs) # vérifier l'utilisation des étoiles

    @action(methods=['delete'], detail=True)
    def delete(self, request):
        print('essai')
        return super(ContributorsViewset, self).delete()


class IssuesViewset(ModelViewSet):
    serializer_class = IssuesSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=['get'], detail=True)
    def get_queryset(self):
        return Issues.objects.filter(project_id=self.kwargs.get('projects_pk'))

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["project_id"] = kwargs['projects_pk']
        request.data["author_user_id"] = request.user.pk
        request.data["assignee_user_id"] = Users.objects.get(id=request.data["assignee_user_id"]).pk
        request.POST._mutable = False
        return super(IssuesViewset, self).create(request, *args, *kwargs) # vérifier l'utilisation des étoiles

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
    serializer_class = CommentsSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=['get'], detail=True)
    def get_queryset(self):
        print(self.kwargs)
        return Comments.objects.filter(issue_id=self.kwargs.get('issues_pk'))

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["issue_id"] = kwargs['issues_pk']
        request.data["author_user_id"] = request.user.pk
        request.POST._mutable = False
        return super(CommentsViewset, self).create(request, *args, *kwargs) # vérifier l'utilisation des étoiles

    @action(methods=['put'], detail=True)
    def modify(self, request, pk=None, *args, **kwargs):
        print('essai')
        print(request.user.pk)
        return super(CommentsViewset, self).update(request, **args, **kwargs)

    @action(methods=['delete'], detail=True)
    def delete(self, request):
        print('essai')
        return super(CommentsViewset, self).delete()