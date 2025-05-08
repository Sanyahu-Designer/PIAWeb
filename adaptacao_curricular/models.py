from django.db import models
from django_multitenant.models import TenantModel, TenantManager
from escola.models import Escola
from neurodivergentes.models import Neurodivergente
from profissionais_app.models import Profissional
from clientes.models import Cliente

class BNCCDisciplina(TenantModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tenant_id = 'cliente_id'  # Define o campo tenant_id necessário para o django-multitenant
    
    nome = models.CharField('Nome da Disciplina', max_length=100)
    objects = TenantManager()

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Disciplina BNCC'
        verbose_name_plural = 'Disciplinas BNCC'
        ordering = ['nome']

class BNCCHabilidade(TenantModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tenant_id = 'cliente_id'  # Define o campo tenant_id necessário para o django-multitenant
    
    ANOS_CHOICES = [
        ('1', '1º Ano'),
        ('2', '2º Ano'),
        ('3', '3º Ano'),
        ('4', '4º Ano'),
        ('5', '5º Ano'),
        ('6', '6º Ano'),
        ('7', '7º Ano'),
        ('8', '8º Ano'),
        ('9', '9º Ano'),
    ]
    
    TRIMESTRE_CHOICES = [
        ('1', '1º Trimestre'),
        ('2', '2º Trimestre'),
        ('3', '3º Trimestre'),
    ]

    disciplina = models.ForeignKey(BNCCDisciplina, on_delete=models.CASCADE, related_name='habilidades', verbose_name='Disciplina:')
    codigo = models.CharField('Código', max_length=20)
    objeto_conhecimento = models.TextField('Objetos do Conhecimento')
    descricao = models.TextField('Descrição da Habilidade')
    ano = models.CharField('Ano', max_length=1, choices=ANOS_CHOICES)
    trimestre = models.CharField('Trimestre', max_length=1, choices=TRIMESTRE_CHOICES)
    objects = TenantManager()

    def __str__(self):
        return f"{self.disciplina} - {self.codigo}"

    class Meta:
        verbose_name = 'Código BNCC'
        verbose_name_plural = 'Códigos BNCC'
        ordering = ['disciplina', 'ano', 'trimestre', 'codigo']

class AdaptacaoCurricularIndividualizada(TenantModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tenant_id = 'cliente_id'  # Define o campo tenant_id necessário para o django-multitenant
    
    MODALIDADE_CHOICES = [
        ('EI', 'Educação Infantil'),
        ('EF', 'Ensino Fundamental'),
        ('EM', 'Ensino Médio'),
    ]

    ANO_CHOICES = [
        ('Educação Infantil', (
            ('B1', 'Berçário I'),
            ('B2', 'Berçário II'),
            ('M1', 'Maternal I'),
            ('M2', 'Maternal II'),
            ('P1', 'Pré I'),
            ('P2', 'Pré II'),
        )),
        ('Ensino Fundamental', (
            ('1F', '1.º ano'),
            ('2F', '2.º ano'),
            ('3F', '3.º ano'),
            ('4F', '4.º ano'),
            ('5F', '5.º ano'),
            ('6F', '6.º ano'),
            ('7F', '7.º ano'),
            ('8F', '8.º ano'),
            ('9F', '9.º ano'),
        )),
        ('Ensino Médio', (
            ('1M', '1.º ano'),
            ('2M', '2.º ano'),
            ('3M', '3.º ano'),
        )),
    ]

    TRIMESTRE_CHOICES = [
        ('1', '1.º trimestre'),
        ('2', '2.º trimestre'),
        ('3', '3.º trimestre'),
        ('S1', '1.º Semestre'),
        ('S2', '2.º Semestre'),
    ]

    aluno = models.ForeignKey(Neurodivergente, on_delete=models.CASCADE, verbose_name='Aluno/Paciente')
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE)
    modalidade_ensino = models.CharField('Modalidade de Ensino', max_length=2, choices=MODALIDADE_CHOICES, default='EF')
    ano = models.CharField('Ano Escolar', max_length=2, choices=ANO_CHOICES, default='1F')
    trimestre = models.CharField('Trimestre', max_length=2, choices=TRIMESTRE_CHOICES, default='1')
    profissional_responsavel = models.ForeignKey(Profissional, on_delete=models.CASCADE)
    data_cadastro = models.DateField('Data do Cadastro', auto_now_add=True)
    objects = TenantManager()

    def __str__(self):
        return f"PEI - {self.aluno}"

    class Meta:
        verbose_name = 'PEI'
        verbose_name_plural = 'PEIs'
        ordering = ['-data_cadastro', 'aluno']

class AdaptacaoHabilidade(TenantModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tenant_id = 'cliente_id'  # Define o campo tenant_id necessário para o django-multitenant
    
    aci = models.ForeignKey(AdaptacaoCurricularIndividualizada, on_delete=models.CASCADE, related_name='adaptacoes')
    habilidade = models.ForeignKey(BNCCHabilidade, on_delete=models.PROTECT)
    descritivo_adaptacao = models.TextField('Descritivo da Adaptação Curricular')
    objects = TenantManager()

    def __str__(self):
        return f"Adaptação - {self.aci.aluno} - {self.habilidade.disciplina} - {self.habilidade.codigo}"

    class Meta:
        verbose_name = 'Habilidade'
        verbose_name_plural = 'Habilidades'
        ordering = ['aci', 'habilidade']
