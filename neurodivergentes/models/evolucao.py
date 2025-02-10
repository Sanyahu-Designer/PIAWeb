from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from ckeditor.fields import RichTextField
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
        verbose_name='Aluno/Paciente',
        on_delete=models.CASCADE,
        related_name='monitoramentos'
    )
    mes = models.IntegerField(
        'Mês',
        help_text='Selecione o mês do PEI',
        choices=[
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
        ],
        default=timezone.now().month
    )
    
    ano = models.IntegerField(
        'Ano',
        help_text='Selecione o ano do PEI',
        default=timezone.now().year
    )
    
    metas = models.ManyToManyField(
        'neurodivergentes.MetaHabilidade',
        through='MonitoramentoMeta',
        verbose_name='Metas/Habilidades',
        help_text='Selecione uma ou mais metas/habilidades para este planejamento'
    )
    
    observacoes = RichTextField(
        'Planejamento',
        help_text='Descreva o planejamento para esta meta/habilidade'
    )
    pedagogo_responsavel = models.ForeignKey(
        'profissionais_app.Profissional',
        verbose_name='Profissional Responosável',
        on_delete=models.PROTECT,
        related_name='monitoramentos',
        limit_choices_to={'profissao__in': ['assistente_social', 'educador_especial', 'neuropsicopedagogo', 'pedagogo', 'psicopedagogo']},
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'PEI'
        verbose_name_plural = 'PEI'
        ordering = ['-ano', '-mes']
        unique_together = ['neurodivergente', 'mes', 'ano']

    def __str__(self):
        return f"PEI de {self.neurodivergente} em {self.get_mes_display()}/{self.ano}"


class MonitoramentoMeta(models.Model):
    monitoramento = models.ForeignKey(
        'neurodivergentes.Monitoramento',
        on_delete=models.CASCADE,
        related_name='monitoramento_metas'
    )
    meta = models.ForeignKey(
        'neurodivergentes.MetaHabilidade',
        on_delete=models.CASCADE,
        related_name='monitoramento_metas'
    )

    class Meta:
        db_table = 'neurodivergentes_monitoramento_metas'
        unique_together = ['monitoramento', 'meta']

    def __str__(self):
        return f"{self.monitoramento} - {self.meta}"