from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django_multitenant.models import TenantModel, TenantManager
from ..models import Neurodivergente
from profissionais_app.models import Profissional
from clientes.models import Cliente
from encrypted_model_fields.fields import EncryptedTextField

class Medicacao(TenantModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    anamnese = models.ForeignKey(
        'Anamnese',
        on_delete=models.CASCADE,
        related_name='medicacoes'
    )
    nome = models.CharField('Nome da Medicação', max_length=100)
    dosagem = models.CharField('Dosagem', max_length=50)
    frequencia = models.CharField('Frequência', max_length=100)
    objects = TenantManager()
    
    class Meta:
        verbose_name = 'Medicação'
        verbose_name_plural = 'Medicações'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.dosagem}"

class RotinaAtividade(TenantModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    anamnese = models.ForeignKey(
        'Anamnese',
        on_delete=models.CASCADE,
        related_name='rotinas'
    )
    horario = models.TimeField('Horário')
    atividade = models.CharField('Atividade', max_length=200)
    observacoes = EncryptedTextField('Observações', blank=True, null=True)
    objects = TenantManager()
    
    class Meta:
        verbose_name = 'Atividade da Rotina'
        verbose_name_plural = 'Atividades da Rotina'
        ordering = ['horario']

    def __str__(self):
        return f"{self.horario.strftime('%H:%M')} - {self.atividade}"

class Anamnese(TenantModel):
    TIPO_PARTO_CHOICES = [
        ('normal', 'Normal'),
        ('cesarea', 'Cesárea')
    ]
    
    STATUS_PAIS_CHOICES = [
        ('casados', 'Casados'),
        ('separados', 'Separados'),
        ('outros', 'Outros')
    ]
    
    SIM_NAO_CHOICES = [
        (True, 'Sim'),
        (False, 'Não')
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tenant_id = 'cliente_id'  # Define o campo tenant_id necessário para o django-multitenant
    
    neurodivergente = models.OneToOneField(
        Neurodivergente,
        on_delete=models.CASCADE,
        related_name='anamnese',
        verbose_name='Aluno/Paciente'
    )

    profissional_responsavel = models.ForeignKey(
        Profissional,
        on_delete=models.PROTECT,
        related_name='anamneses_responsavel',
        verbose_name='Profissional Responsável',
        null=True,  # Permitir nulo temporariamente
        blank=True  # Permitir formulários vazios temporariamente
    )

    tipo_parto = models.CharField(
        'Tipo de Parto',
        max_length=10,
        choices=TIPO_PARTO_CHOICES
    )
    tempo_gestacao = models.IntegerField(
        'Tempo de Gestação (semanas)',
        validators=[
            MinValueValidator(20),
            MaxValueValidator(45)
        ]
    )
    prematuridade = models.BooleanField(
        'Prematuridade',
        choices=SIM_NAO_CHOICES
    )
    tempo_prematuridade = models.IntegerField(
        'Tempo de Prematuridade (semanas)',
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(20)
        ]
    )
    observacoes_parto = EncryptedTextField(
        'Observações sobre o Parto',
        blank=True
    )
    status_pais = models.CharField(
        'Status dos Pais',
        max_length=10,
        choices=STATUS_PAIS_CHOICES
    )

    beneficios_sociais = models.CharField(
        'Benefícios Sociais',
        max_length=100,
        blank=True
    )
    convenio_medico = models.BooleanField(
        'Possui Convênio Médico',
        choices=SIM_NAO_CHOICES
    )
    nome_convenio = models.CharField(
        'Nome do Convênio',
        max_length=100,
        blank=True,
        null=True
    )

    queixa_inicial = EncryptedTextField('Queixa Inicial')
    historia_vida = EncryptedTextField('História de Vida')

    comportamento_familiar = EncryptedTextField(
        'Comportamento no Ambiente Familiar',
        blank=True
    )
    comportamento_social = EncryptedTextField(
        'Comportamento no Ambiente Social e Escolar',
        blank=True
    )

    autonomia = EncryptedTextField('Autonomia')
    comunicacao = EncryptedTextField('Comunicação')
    restricoes_alimentares = models.BooleanField(
        'Possui Restrições Alimentares',
        choices=SIM_NAO_CHOICES
    )
    descricao_restricoes = EncryptedTextField(
        'Descrição das Restrições Alimentares',
        blank=True,
        null=True
    )

    aspectos_cognitivos = EncryptedTextField('Aspectos Cognitivos')
    aspectos_psicomotores = EncryptedTextField('Aspectos Psicomotores')
    aspectos_emocionais = EncryptedTextField('Aspectos Emocionais/Sociais')
    aspectos_sensoriais = EncryptedTextField('Aspectos Sensoriais')

    anexos = models.FileField(
        'Anexos',
        upload_to='neurodivergentes/anamnese/',
        blank=True,
        null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TenantManager()
    
    class Meta:
        verbose_name = 'Anamnese'
        verbose_name_plural = 'Anamneses'

    def __str__(self):
        return f"Anamnese - {self.neurodivergente}"

    def clean(self):
        if self.prematuridade and not self.tempo_prematuridade:
            raise ValidationError({
                'tempo_prematuridade': 'Informe o tempo de prematuridade.'
            })
            
        if self.convenio_medico and not self.nome_convenio:
            raise ValidationError({
                'nome_convenio': 'Informe o nome do convênio médico.'
            })
            
        if self.restricoes_alimentares and not self.descricao_restricoes:
            raise ValidationError({
                'descricao_restricoes': 'Descreva as restrições alimentares.'
            })