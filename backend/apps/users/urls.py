"""
URL patterns for the users app.
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, LogoutView, UserProfileView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', UserProfileView.as_view(), name='profile'),
]
