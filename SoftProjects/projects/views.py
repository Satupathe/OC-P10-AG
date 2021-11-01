from rest_framework import status, generics, permissions, filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from .serializers import RegisterSerializer, ProjectsDetailsSerializer
from .models import Users, Projects, Contributors, Issues, Comments 
from .permissions import IsOwner


"""class MultiSerializerViewSetMixin(object):
    def get_serializer_class(self):
        Look for serializer class in self.serializer_action_classes, which
        should be a dict mapping action name (key) to serializer class (value),
        i.e.:

        class MyViewSet(MultiSerializerViewSetMixin, ViewSet):
            serializer_class = MyDefaultSerializer
            serializer_action_classes = {
               'list': MyListSerializer,
               'my_action': MyActionSerializer,
            }

            @action
            def my_action:
                ...

        If there's no entry for that action then just fallback to the regular
        get_serializer_class lookup: self.serializer_class, DefaultSerializer.

        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(MultiSerializerViewSetMixin, self).get_serializer_class()"""


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
    queryset = Projects.objects.all()
    serializer_class = ProjectsDetailsSerializer
    detail_serializer_class = ProjectsDetailsSerializer
    permission_classes = [IsAuthenticated] #is author, contributor
    
    @action(methods=['get'], detail=True)
    def get_queryset(self):
        return Projects.objects.filter(author_user_id=self.request.user)
    
    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["author_user_id"] = request.user.pk
        request.POST._mutable = False
        return super(ProjectsViewset, self).create(request, *args, *kwargs) # vérifier l'utilisation des étoiles

    @action(methods=['put'], detail=True)
    def modify(self, request, pk=None, *args, **kwargs):
        print('essai')
        print(request.user.pk)
        return super(ProjectsViewset, self).update(request, **args, **kwargs)

    @action(methods=['delete'], detail=True)
    def delete(self, request, pk=None):
        print('essai')
        print(request.user.pk)
        return super(ProjectsViewset, self).delete()
