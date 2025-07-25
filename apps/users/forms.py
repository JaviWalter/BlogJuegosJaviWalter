from django import forms
from .models import User
from django.db import transaction
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm

class RegisterUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'nombre', 'apellido', 'fecha_nacimiento', 'email', 'imagen']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_superuser = False
        user.is_staff = False
        user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(label='Nombre de usuario')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(request, username = username, password = password)
        if user:
            login(request, user)
