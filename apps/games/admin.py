from django.contrib import admin
from django.utils.html import format_html
from .models import Plataforma, Genero, Juego, Puntuacion, ComentarioJuego

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
    list_display = ('titulo', 'desarrollador', 'editor', 'fecha_lanzamiento', 'activo', 'promedio_puntuacion', 'imagen_preview')
    list_filter = ('activo', 'fecha_lanzamiento', 'plataformas', 'generos')
    search_fields = ('titulo', 'descripcion', 'desarrollador', 'editor')
    date_hierarchy = 'fecha_lanzamiento'
    filter_horizontal = ('plataformas', 'generos')
    readonly_fields = ('promedio_puntuacion', 'agregado_por', 'fecha_agregado')
    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'descripcion', 'fecha_lanzamiento')
        }),
        ('Desarrollo', {
            'fields': ('desarrollador', 'editor')
        }),
        ('Multimedia', {
            'fields': ('imagen_portada', 'video_trailer_url')
        }),
        ('Clasificación', {
            'fields': ('plataformas', 'generos')
        }),
        ('Estadísticas', {
            'fields': ('promedio_puntuacion', 'activo')
        }),
        ('Auditoría', {
            'fields': ('agregado_por', 'fecha_agregado'),
            'classes': ('collapse',)
        }),
    )

    def imagen_preview(self, obj):
        if obj.imagen_portada:
            return format_html('<img src="{}" style="max-height: 50px;" />', obj.imagen_portada.url)
        return "-"
    imagen_preview.short_description = 'Portada'

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Solo si es un nuevo objeto
            obj.agregado_por = request.user
        super().save_model(request, obj, form, change)

@admin.register(Puntuacion)
class PuntuacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'juego', 'usuario', 'valor', 'fecha_creacion')
    list_filter = ('valor', 'fecha_creacion') 
    search_fields = ('juego__titulo', 'usuario__username') # Buscar por título o nombre de usuario
    date_hierarchy = 'fecha_creacion'
    raw_id_fields = ('juego', 'usuario')# Útil para seleccionar juego y usuario por ID

@admin.register(ComentarioJuego)
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
