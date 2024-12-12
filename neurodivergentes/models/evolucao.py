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
        verbose_name = 'Registro de Evolução'
        verbose_name_plural = 'Registros de Evolução'
        ordering = ['-data']

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

class Frequencia(models.Model):
    MESES_CHOICES = [
        (1, 'Janeiro'),
        (2, 'Fevereiro'),
        (3, 'Março'),
        (4, 'Abril'),
        (5, 'Maio'),
        (6, 'Junho'),
        (7, 'Julho'),
        (8, 'Agosto'),
        (9, 'Setembro'),
        (10, 'Outubro'),
        (11, 'Novembro'),
        (12, 'Dezembro')
    ]

    neurodivergente = models.ForeignKey(
        Neurodivergente,
        on_delete=models.CASCADE,
        related_name='frequencias'
    )
    ano = models.IntegerField(
        'Ano',
        validators=[
            MinValueValidator(2000),
            MaxValueValidator(2050)
        ]
    )
    mes = models.IntegerField('Mês', choices=MESES_CHOICES)
    total_atendimentos = models.IntegerField(
        'Total de Atendimentos',
        validators=[MinValueValidator(0)]
    )
    observacoes = models.TextField('Observações', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Frequência'
        verbose_name_plural = 'Frequências'
        ordering = ['ano', 'mes']
        unique_together = ['neurodivergente', 'ano', 'mes']

    def __str__(self):
        return f"Frequência de {self.neurodivergente} - {self.get_mes_display()}/{self.ano}"

    def clean(self):
        # Validar ano
        ano_atual = timezone.now().year
        if self.ano > ano_atual:
            raise ValidationError({
                'ano': 'Não é possível registrar frequência para anos futuros.'
            })

        # Validar mês
        if self.ano == ano_atual:
            mes_atual = timezone.now().month
            if self.mes > mes_atual:
                raise ValidationError({
                    'mes': 'Não é possível registrar frequência para meses futuros.'
                })