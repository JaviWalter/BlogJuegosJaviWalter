from django.contrib import admin
from .models import Plataforma, Genero, Juego, Puntuacion, Comentario

# Register your models here.

@admin.register(Plataforma)
class PlataformaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')  # Columnas a mostrar en la lista
    search_fields = ('nombre',)  # Campo por el que se puede buscar

@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(Juego)
class JuegoAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'fecha_lanzamiento', 'desarrollador', 'editor', 'activo', 'fecha_agregado', 'agregado_por', 'promedio_puntuacion')
    list_filter = ('activo', 'fecha_lanzamiento','plataformas', 'generos')  # Filtros laterales
    search_fields = ('titulo', 'descripcion', 'desarrollador', 'editor')  # Campos de búsqueda
    date_hierarchy = 'fecha_lanzamiento'  # Navegación por fecha
    filter_horizontal = ('plataformas', 'generos')

@admin.register(Puntuacion)
class PuntuacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'juego', 'usuario', 'valor', 'fecha_creacion')
    list_filter = ('valor', 'fecha_creacion') 
    search_fields = ('juego__titulo', 'usuario__username') # Buscar por título o nombre de usuario
    date_hierarchy = 'fecha_creacion'
    raw_id_fields = ('juego', 'usuario')# Útil para seleccionar juego y usuario por ID

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'juego', 'usuario', 'fecha_creacion', 'aprobado')
    list_filter = ('aprobado', 'fecha_creacion')
    search_fields = ('juego__titulo', 'usuario__username', 'texto')
    date_hierarchy = 'fecha_creacion'
    raw_id_fields = ('juego', 'usuario')
    actions = ['aprobar_comentarios', 'desaprobar_comentarios']# Acciones personalizadas

    def aprobar_comentarios(self, request, queryset):
            queryset.update(aprobado=True)
            self.message_user(request, "Comentarios seleccionados aprobados con éxito.")
    aprobar_comentarios.short_description = "Aprobar comentarios seleccionados"

    def desaprobar_comentarios(self, request, queryset):
            queryset.update(aprobado=False)
            self.message_user(
                request, "Comentarios seleccionados desaprobados con éxito.")
    desaprobar_comentarios.short_description = "Desaprobar comentarios seleccionados"
