from django.urls import path, include
from .views import RegisterUserView, UpdateUserView, list_users, CustomPasswordResetView, ProfileView
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'apps.users'

urlpatterns = [
    path('signup/', RegisterUserView.as_view(template_name='account/signup.html'), name='signup'),
    path('login/', LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='account/logout.html'), name='logout'),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('', include('allauth.urls')),
    path('update_user/<int:pk>', UpdateUserView.as_view(), name='update_user'),
    path('list_users', list_users, name='list_users'),
]