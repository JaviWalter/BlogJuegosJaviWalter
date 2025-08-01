from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

# Create your models here.}
class User(AbstractUser):
    nombre = models.CharField(max_length=45, default='sin especificar')
    apellido = models.CharField(max_length=45, default='sin especificar')
    email = models.EmailField(null=False, unique=True, default='tu_correo@example.com')
    fecha_nacimiento = models.DateField('fecha_nacimiento', default='2000-1-1')
    es_colaborador = models.BooleanField('es_colaborador', default=False)
    imagen = models.ImageField(null=True, blank=True, upload_to='usuario', default='usuario/user-default.svg')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ('-nombre',)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    def get_absolute_url(self):
        return reverse('index')
