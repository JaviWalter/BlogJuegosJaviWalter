from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User
from django.contrib import messages

# Register your models here.


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'nombre', 'apellido', 'es_colaborador', 'is_superuser', 'imagen_preview', 'fecha_nacimiento')
    list_filter = ('es_colaborador', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'nombre', 'apellido')
    ordering = ('-date_joined',)
    filter_horizontal = ('groups', 'user_permissions',)
    actions = ['agregar_colaborador', 'quitar_colaborador']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {
            'fields': ('nombre', 'apellido', 'email', 'fecha_nacimiento', 'imagen')
        }),
        ('Permisos', {
            'fields': ('is_active', 'is_superuser', 'es_colaborador', 'groups', 'user_permissions'),
        }),
        ('Fechas importantes', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('username', 'email', 'password1', 'password2', 'nombre', 'apellido', 'fecha_nacimiento'),
        }),
    )

    def agregar_colaborador(self, request, queryset):
        """Convierte usuarios seleccionados en colaboradores."""
        updated = queryset.update(es_colaborador=True)
        self.message_user(
            request,
            f"{updated} usuario(s) marcado(s) como colaborador(es).",
            messages.SUCCESS
        )
    agregar_colaborador.short_description = 'Agregar colaborador'

    def quitar_colaborador(self, request, queryset):
        """Remueve el estado de colaborador de los usuarios seleccionados."""
        updated = queryset.update(es_colaborador=False)
        self.message_user(
            request,
            f"{updated} usuario(s) ya no son colaborador(es).",
            messages.SUCCESS
        )
    quitar_colaborador.short_description = 'Quitar colaborador'
    
    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; border-radius: 50%;" />', obj.imagen.url)
        return "Sin imagen"
    imagen_preview.short_description = 'Foto'
    
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(self.readonly_fields)
    
        if obj:  
            readonly_fields.extend(['last_login', 'date_joined'])
            
            
        if obj == request.user:
            readonly_fields.extend(['is_superuser', 'es_colaborador', 'is_staff'])
            
            
            if request.user.es_colaborador and not request.user.is_superuser:
                readonly_fields.extend(['is_superuser', 'es_colaborador', 'is_staff'])
        
        return readonly_fields