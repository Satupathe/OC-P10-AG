from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import ContributorsViewset, ProjectsViewset, UserCreate#, ProjectsDetailsView
from rest_framework_nested import routers


projects_router = routers.SimpleRouter(trailing_slash=False)
projects_router.register(r"projects/?", ProjectsViewset, basename='projects')

users_router = routers.NestedSimpleRouter(projects_router, r"projects/?", lookup="projects", trailing_slash=False)
users_router.register(r"users/?", ContributorsViewset, basename='contributors')


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', UserCreate.as_view(), name='signup'),
    path('', include(projects_router.urls)),
    path('', include(users_router.urls)),
    
]
