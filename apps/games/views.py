from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Juego, ComentarioJuego
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from .forms import ComentarioJuegoForm

class JuegoListView(ListView):
    model = Juego
    template_name = 'games/juego_list.html'
    context_object_name = 'juegos'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_juegos'] = self.get_queryset().count()
        return context

    def get_queryset(self):
        return Juego.objects.filter(activo=True).order_by('-fecha_lanzamiento')

class JuegoDetailView(DetailView):
    model = Juego
    template_name = 'games/juego_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comentario_form'] = ComentarioJuegoForm()
        context['comentarios'] = self.object.comentarios.filter(aprobado=True)
        return context

    def get_queryset(self):
        return Juego.objects.filter(activo=True)

class JuegoCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Juego
    fields = ['titulo', 'descripcion', 'fecha_lanzamiento', 'desarrollador', 
            'editor', 'imagen_portada', 'video_trailer_url', 'plataformas', 'generos']
    template_name = 'games/juego_form.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.es_colaborador
    
    def form_valid(self, form):
        form.instance.agregado_por = self.request.user
        messages.success(self.request, 'Juego creado correctamente.')
        return super().form_valid(form)

class JuegoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Juego
    fields = ['titulo', 'descripcion', 'fecha_lanzamiento', 'desarrollador', 
            'editor', 'imagen_portada', 'video_trailer_url', 'plataformas', 'generos']
    template_name = 'games/juego_form.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.es_colaborador
    
    def form_valid(self, form):
        messages.success(self.request, 'Juego actualizado correctamente.')
        return super().form_valid(form)

class JuegoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Juego
    template_name = 'confirmar_eliminar.html'
    success_url = reverse_lazy('apps.games:lista_juegos')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.es_colaborador
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipo_objeto'] = 'juego'
        context['contenido_relacionado'] = {
            'comentarios': self.object.comentarios.count(),
            'puntuaciones': self.object.puntuacion_set.count()
        }
        return context
    

def aprobar_comentario(request, pk):
    comentario = get_object_or_404(ComentarioJuego, pk=pk)
    if request.user.has_perm('games.aprobar_comentario'):
        comentario.aprobado = True
        comentario.save()
        messages.success(request, 'Comentario aprobado.')
    else:
        messages.error(request, 'No tienes permisos para aprobar comentarios')
    return redirect('apps.games:detalle_juego', pk=comentario.juego.pk)

class ComentarioJuegoCreateView(LoginRequiredMixin, CreateView):
    model = ComentarioJuego
    form_class = ComentarioJuegoForm
    template_name = 'comentario_form.html'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.juego_id = self.kwargs['juego_id']
        if self.request.user.has_perm('games.aprobar_comentario'):
            form.instance.aprobado = True
            messages.success(self.request, 'Comentario publicado.')
        else:
            messages.success(self.request, 'Comentario enviado para aprobación.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('apps.games:detalle_juego', kwargs={'pk': self.kwargs['juego_id']})

class ComentarioJuegoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ComentarioJuego
    form_class = ComentarioJuegoForm
    template_name = 'comentario_form.html'

    def test_func(self):
        comentario = self.get_object()
        return self.request.user == comentario.usuario or self.request.user.has_perm('games.aprobar_comentario')
    
    def form_valid(self, form):
        messages.success(self.request, 'Comentario actualizado exitosamente.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('apps.games:detalle_juego', kwargs={'pk': self.object.juego.pk})

class ComentarioJuegoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ComentarioJuego
    template_name = 'confirmar_eliminar.html'

    def test_func(self):
        comentario = self.get_object()
        return self.request.user == comentario.usuario or self.request.user.has_perm('games.aprobar_comentario')
    
    def get_success_url(self):
        return reverse('apps.games:detalle_juego', kwargs={'pk': self.object.juego.pk})