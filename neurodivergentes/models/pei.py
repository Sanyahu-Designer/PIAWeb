from django.db import models
from django.utils import timezone
from encrypted_model_fields.fields import EncryptedTextField
from django_multitenant.models import TenantModel, TenantManager
from ..models import Neurodivergente
from profissionais_app.models import Profissional
from clientes.models import Cliente

class Monitoramento(TenantModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tenant_id = 'cliente_id'  # Define o campo tenant_id necessário para o django-multitenant
    
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
    observacoes = EncryptedTextField(
        'Planejamento',
        help_text='Descreva o planejamento para esta meta/habilidade',
        null=True,
        blank=True
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
    objects = TenantManager()

    class Meta:
        verbose_name = 'PAEE'
        verbose_name_plural = 'PAEE'
        ordering = ['-ano', '-mes']
        unique_together = ['neurodivergente', 'mes', 'ano']

    def __str__(self):
        return f"PEI de {self.neurodivergente} - {self.get_mes_display()}/{self.ano}"

class MonitoramentoMeta(TenantModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tenant_id = 'cliente_id'  # Define o campo tenant_id necessário para o django-multitenant
    
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
    objects = TenantManager()

    class Meta:
        db_table = 'neurodivergentes_monitoramento_metas'
        unique_together = ['monitoramento', 'meta']

    def __str__(self):
        return f"{self.monitoramento} - {self.meta}"
