from django.urls import path
from .views import RegisterUserView, UpdateUserView, list_users, CustomPasswordResetView
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'apps.users'

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('passwor_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('update_user/<int:pk>', UpdateUserView.as_view(), name='update_user'),
    path('list_users', list_users, name='list_users'),
]