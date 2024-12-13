from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from ..models import Neurodivergente
from profissionais_app.models import Profissional

class Medicacao(models.Model):
    anamnese = models.ForeignKey(
        'Anamnese',
        on_delete=models.CASCADE,
        related_name='medicacoes'
    )
    nome = models.CharField('Nome da Medicação', max_length=100)
    dosagem = models.CharField('Dosagem', max_length=50)
    frequencia = models.CharField('Frequência', max_length=100)
    
    class Meta:
        verbose_name = 'Medicação'
        verbose_name_plural = 'Medicações'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.dosagem}"

class RotinaAtividade(models.Model):
    anamnese = models.ForeignKey(
        'Anamnese',
        on_delete=models.CASCADE,
        related_name='rotinas'
    )
    horario = models.TimeField('Horário')
    atividade = models.CharField('Atividade', max_length=200)
    observacoes = models.TextField('Observações', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Atividade da Rotina'
        verbose_name_plural = 'Atividades da Rotina'
        ordering = ['horario']

    def __str__(self):
        return f"{self.horario.strftime('%H:%M')} - {self.atividade}"

class Anamnese(models.Model):
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

    # Relacionamento com Aluno/Paciente
    neurodivergente = models.OneToOneField(
        Neurodivergente,
        on_delete=models.CASCADE,
        related_name='anamnese',
        verbose_name='Aluno/Paciente'
    )

    # Profissional Responsável
    profissional_responsavel = models.ForeignKey(
        Profissional,
        on_delete=models.PROTECT,
        related_name='anamneses_responsavel',
        verbose_name='Profissional Responsável',
        null=True,  # Permitir nulo temporariamente
        blank=True  # Permitir formulários vazios temporariamente
    )

    # Nascimento e Primeira Infância
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
    observacoes_parto = models.TextField(
        'Observações sobre o Parto',
        blank=True
    )
    status_pais = models.CharField(
        'Status dos Pais',
        max_length=10,
        choices=STATUS_PAIS_CHOICES
    )

    # Informações Médicas
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

    # Histórico
    queixa_inicial = models.TextField('Queixa Inicial')
    historia_vida = models.TextField('História de Vida')

    comportamento_familiar = models.TextField(
    'Comportamento no Ambiente Familiar',
    blank=True  # Permite campo vazio no formulário
    )
    comportamento_social = models.TextField(
    'Comportamento no Ambiente Social e Escolar',
    blank=True
    )

    # Desenvolvimento
    autonomia = models.TextField('Autonomia')
    comunicacao = models.TextField('Comunicação')
    restricoes_alimentares = models.BooleanField(
        'Possui Restrições Alimentares',
        choices=SIM_NAO_CHOICES
    )
    descricao_restricoes = models.TextField(
        'Descrição das Restrições Alimentares',
        blank=True,
        null=True
    )

    # Percepção dos Responsáveis
    aspectos_cognitivos = models.TextField('Aspectos Cognitivos')
    aspectos_psicomotores = models.TextField('Aspectos Psicomotores')
    aspectos_emocionais = models.TextField('Aspectos Emocionais/Sociais')
    aspectos_sensoriais = models.TextField('Aspectos Sensoriais')

    # Campos de controle
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Anamnese'
        verbose_name_plural = 'Anamneses'

    def __str__(self):
        return f"Anamnese de {self.neurodivergente}"

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