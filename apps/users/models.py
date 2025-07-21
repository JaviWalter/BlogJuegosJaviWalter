from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

# Create your models here.}
class User(AbstractUser):
    imagen = models.ImageField(null=True, blank=True, upload_to='usuario', default='usuario/user-default.svg')

    def get_absolute_url(self):
        return reverse('index')
