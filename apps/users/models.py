from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

# Create your models here.}
class User(AbstractUser):
    nombre = models.CharField(max_length=45, null=False, default='sin especificar')
    apellido = models.CharField(max_length=45, null=False, default='sin especificar')
    correo = models.EmailField(null=False, default='sin especificar')
    fecha_nacimiento = models.DateField('fecha_nacimiento', default='2000-1-1')
    es_colaborador = models.BooleanField('es_colaborador', default=False)
    imagen = models.ImageField(null=True, blank=True, upload_to='usuario', default='usuario/user-default.svg')

    class Meta:
        ordering = ('-nombre',)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('index')
