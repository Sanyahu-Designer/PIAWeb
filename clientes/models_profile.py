from django.db import models
from django.contrib.auth.models import User
from .models import Cliente

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name='Prefeitura/Cliente')

    def __str__(self):
        return f"Perfil de {self.user.username} ({self.cliente.nome})"
