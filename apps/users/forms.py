from .models import User
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import ResetPasswordForm

class RegisterUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2', 'nombre', 'apellido', 'fecha_nacimiento', 'imagen']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_superuser = False
        user.is_staff = False
        user.save()
        return user



class CustomPasswordResetForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})