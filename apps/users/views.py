
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from .forms import RegisterUserForm
from .models import User


class RegisterUserView(CreateView):
    model = User
    template_name = 'registration/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('index')


def ListUsers(request):
    usuarios = User.objects.all()
    template_name = 'registration/list_users.html'
    context = {
        'usuarios' : usuarios
    }
    return render(request, template_name, context)


