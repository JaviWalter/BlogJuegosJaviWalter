from django import forms
from .models import User
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from allauth.account.forms import ResetPasswordForm

class RegisterUserForm(UserCreationForm):
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}), required=True)

    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2', 'nombre', 'apellido', 'fecha_nacimiento', 'imagen']
        widgets = {'imagen' : forms.ClearableFileInput(attrs={'class': 'form-control'}),}

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class UpdateUserForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['username', 'email', 'nombre', 'apellido', 'fecha_nacimiento', 'imagen']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type':'date'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class CustomPasswordResetForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ingresa tu email aquí.',
            })