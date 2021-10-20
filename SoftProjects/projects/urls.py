from django.urls import path, include
from .views import UserCreate, LoginAPIView

urlpatterns = [
    path('signup/', UserCreate.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
]
