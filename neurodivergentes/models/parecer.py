from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django_multitenant.models import TenantModel, TenantManager
from encrypted_model_fields.fields import EncryptedTextField
from ..models import Neurodivergente
from escola.models import Escola
from profissionais_app.models import Profissional
from clientes.models import Cliente

class ParecerAvaliativo(TenantModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tenant_id = 'cliente_id'  # Define o campo tenant_id necessário para o django-multitenant
    
    neurodivergente = models.ForeignKey(
        Neurodivergente,
        on_delete=models.CASCADE,
        related_name='pareceres',
        verbose_name='Aluno/Paciente'
    )
    escola = models.ForeignKey(
        Escola,
        on_delete=models.PROTECT,
        related_name='pareceres'
    )
    evolucao = EncryptedTextField('Parecer Descritivo', blank=True, null=True)
    data_avaliacao = models.DateField('Data do Parecer')
    profissional_responsavel = models.ForeignKey(
        Profissional,
        on_delete=models.PROTECT,
        related_name='pareceres_responsavel',
        verbose_name='Profissional Responsável',
        limit_choices_to={'profissao__in': ['educador_especial', 'pedagogo', 'psicopedagogo', 'neuropsicopedagogo']},
        null=True,
        blank=True
    )
    anexos = models.FileField(
        'Anexos',
        upload_to='neurodivergentes/pareceres/',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    grafico_data_inicio = models.DateField('Data Inicial do Gráfico', null=True, blank=True)
    grafico_data_fim = models.DateField('Data Final do Gráfico', null=True, blank=True)
    grafico_frequencia = models.ImageField(
        'Gráfico de Frequência', 
        upload_to='neurodivergentes/pareceres/graficos/', 
        blank=True, 
        null=True
    )
    grafico_monitoramento = models.ImageField(
        'Gráfico de Monitoramento', 
        upload_to='neurodivergentes/pareceres/graficos/', 
        blank=True, 
        null=True
    )
    objects = TenantManager()

    class Meta:
        verbose_name = 'Parecer'
        verbose_name_plural = 'Pareceres'
        ordering = ['-data_avaliacao']

    def __str__(self):
        return f"Parecer - {self.neurodivergente}"

    @property
    def idade(self):
        """Calcula a idade do neurodivergente na data do parecer"""
        if self.neurodivergente and self.neurodivergente.data_nascimento:
            nascimento = self.neurodivergente.data_nascimento
            data_ref = timezone.localdate()
            idade = data_ref.year - nascimento.year
            # Ajusta a idade se ainda não fez aniversário no ano
            if data_ref.month < nascimento.month or \
               (data_ref.month == nascimento.month and data_ref.day < nascimento.day):
                idade -= 1
            return idade
        return None

    idade.fget.short_description = 'Idade'

    def clean(self):
        # Verificar se a escola está ativa
        if not self.escola.ativo:
            raise ValidationError({
                'escola': 'A escola selecionada não está ativa.'
            })