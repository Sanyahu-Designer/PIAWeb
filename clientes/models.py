from django.db import models
from django_multitenant.models import TenantModel
from django.utils.html import mark_safe
from encrypted_model_fields.fields import EncryptedCharField, EncryptedEmailField

class Cliente(TenantModel):
    # Dados básicos da prefeitura (essenciais para nota fiscal)
    nome = models.CharField(max_length=200, verbose_name="Nome da Prefeitura ou Cliente")
    cnpj = models.CharField(max_length=18, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    inscricao_estadual = models.CharField(max_length=20, blank=True, null=True, verbose_name="Inscrição Estadual", help_text="Geralmente isento para prefeituras")
    
    # Dados de endereço (essenciais para nota fiscal)
    logradouro = models.CharField(max_length=255, blank=True, null=True, verbose_name="Logradouro")
    numero = models.CharField(max_length=10, blank=True, null=True, verbose_name="Número")
    complemento = models.CharField(max_length=100, blank=True, null=True, verbose_name="Complemento")
    bairro = models.CharField(max_length=100, blank=True, null=True, verbose_name="Bairro")
    cidade = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cidade")
    estado = models.CharField(max_length=2, blank=True, null=True, verbose_name="Estado")
    cep = models.CharField(max_length=9, blank=True, null=True, verbose_name="CEP")
    
    # Contato principal para nota fiscal
    telefone_principal = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone Principal")
    email_principal = models.EmailField(blank=True, null=True, verbose_name="E-mail Principal")
    
    # Contato Financeiro/Tesouraria (importante para faturamento)
    nome_responsavel_financeiro = models.CharField(max_length=200, blank=True, null=True, verbose_name="Nome do Responsável Financeiro")
    cargo_responsavel_financeiro = models.CharField(max_length=100, blank=True, null=True, verbose_name="Cargo do Responsável Financeiro")
    email_responsavel_financeiro = EncryptedEmailField(blank=True, null=True, verbose_name="E-mail do Responsável Financeiro")
    telefone_responsavel_financeiro = EncryptedCharField(max_length=20, blank=True, null=True, verbose_name="Telefone do Responsável Financeiro")
    
    # Usuário Administrador (pode ser um campo User ou referência externa)
    
    # Autoridades Municipais
    nome_prefeito = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nome do Prefeito(a)")
    nome_vice_prefeito = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nome do Vice-Prefeito(a)")
    nome_secretario_saude = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nome do Secretário de Saúde")
    nome_secretario_educacao = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nome do Secretário de Educação")
    email_secretario_saude = EncryptedEmailField(blank=True, null=True, verbose_name="E-mail Secretário de Saúde")
    telefone_secretario_saude = EncryptedCharField(max_length=20, blank=True, null=True, verbose_name="Telefone Secretário de Saúde")
    email_secretario_educacao = EncryptedEmailField(blank=True, null=True, verbose_name="E-mail Secretário de Educação")
    telefone_secretario_educacao = EncryptedCharField(max_length=20, blank=True, null=True, verbose_name="Telefone Secretário de Educação")
    
    # Informações para dimensionamento do serviço
    numero_habitantes = models.PositiveIntegerField(blank=True, null=True, verbose_name="Número de Habitantes")
    numero_escolas = models.PositiveIntegerField(blank=True, null=True, verbose_name="Número de Escolas Municipais")
    numero_alunos = models.PositiveIntegerField(blank=True, null=True, verbose_name="Número Aproximado de Alunos")
    
    # Campos de controle
    data_cadastro = models.DateTimeField(blank=True, null=True, verbose_name="Data de Cadastro")
    data_atualizacao = models.DateTimeField(blank=True, null=True, verbose_name="Última Atualização")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")

    tenant_id = 'id'  # Campo usado pelo django-multitenant para isolar os dados

    class Meta:
        verbose_name = "Cliente/Prefeitura"
        verbose_name_plural = "Clientes/Prefeituras"
        ordering = ['nome']

    def __str__(self):
        return self.nome
