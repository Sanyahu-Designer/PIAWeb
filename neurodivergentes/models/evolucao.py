from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from ..models import Neurodivergente
from profissionais_app.models import Profissional

class RegistroEvolucao(models.Model):
    neurodivergente = models.ForeignKey(
        Neurodivergente,
        on_delete=models.CASCADE,
        related_name='registros_evolucao',
        verbose_name='Aluno/Paciente'
    )
    data = models.DateField('Data')
    descricao = models.TextField('Descrição da Evolução')
    profissional = models.ForeignKey(
        Profissional,
        on_delete=models.PROTECT,
        related_name='registros_evolucao'
    )
    anexos = models.FileField(
        'Anexos',
        upload_to='neurodivergentes/evolucao/',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Histórico de Evolução'
        verbose_name_plural = 'Histórico de Evolução'
        ordering = ['-data', '-created_at']

    def __str__(self):
        return f"Evolução - {self.neurodivergente}"
