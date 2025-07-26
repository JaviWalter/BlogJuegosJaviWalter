
from django.http import Http404
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from .forms import RegisterUserForm
from .models import User


class RegisterUserView(CreateView):
    model = User
    template_name = 'registration/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('index')


def list_users(request):
    usuarios = User.objects.all()
    template_name = 'registration/list_users.html'
    context = {
        'usuarios' : usuarios
    }
    return render(request, template_name, context)

class UpdateUserView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['nombre', 'apellido', 'correo', 'fecha_nacimiento', 'imagen']
    template_name = 'registration/register.html'
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        user_id = self.kwargs.get('pk')
        if str(user_id) != str(request.user.pk):
            return Http404('No tienes los permisos necesarios para actualizar este usuario.')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, 'Perfil actualizado correctamente.')
        return super().form_valid(form)