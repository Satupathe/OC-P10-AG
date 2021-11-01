from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import ProjectsViewset, UserCreate#, ProjectsDetailsView
from rest_framework import routers


projects_router = routers.SimpleRouter(trailing_slash=False)
projects_router.register(r"projects/?", ProjectsViewset, basename='projects')


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', UserCreate.as_view(), name='signup'),
    path('', include(projects_router.urls)),
    
]
