from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import ContributorsViewset, IssuesViewset, ProjectsViewset, UserCreate, CommentsViewset
from rest_framework_nested import routers


projects_router = routers.SimpleRouter(trailing_slash=False)
projects_router.register(r"projects/?", ProjectsViewset, basename='projects')

users_router = routers.NestedSimpleRouter(projects_router, r"projects/?", lookup="projects", trailing_slash=False)
users_router.register(r"users/?", ContributorsViewset, basename='contributors')

issues_router = routers.NestedSimpleRouter(projects_router, r"projects/?", lookup="projects", trailing_slash=False)
issues_router.register(r"issues/?", IssuesViewset, basename='issues')

comments_router = routers.NestedSimpleRouter(issues_router, r"issues/?", lookup="issues", trailing_slash=False)
comments_router.register(r"comments/?", CommentsViewset, basename='comments')


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', UserCreate.as_view(), name='signup'),
    path('', include(projects_router.urls)),
    path('', include(users_router.urls)),
    path('', include(issues_router.urls)),
    path('', include(comments_router.urls)),
]
