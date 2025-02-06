from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from ..models import Neurodivergente
from profissionais_app.models import Profissional

class RegistroEvolucao(models.Model):
    neurodivergente = models.ForeignKey(
        Neurodivergente,
        on_delete=models.CASCADE,
        related_name='registros_evolucao'
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
        verbose_name = 'Evolução'
        verbose_name_plural = 'Evolução'
        ordering = ['-data', '-created_at']

    def __str__(self):
        return f"Evolução de {self.neurodivergente} em {self.data}"

class Monitoramento(models.Model):
    neurodivergente = models.ForeignKey(
        Neurodivergente,
        on_delete=models.CASCADE,
        related_name='monitoramentos'
    )
    data = models.DateField('Data')
    meta = models.CharField('Meta/Habilidade', max_length=200)
    nivel = models.IntegerField(
        'Nível (%)',
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ],
        blank=True,
        null=True
    )
    observacoes = models.TextField('Observações', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'PEI'
        verbose_name_plural = 'PEI'
        ordering = ['-data']

    def __str__(self):
        return f"PEI de {self.neurodivergente} em {self.data}"