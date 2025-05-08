from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils.html import mark_safe
from django.core.exceptions import ValidationError
from datetime import date
from escola.models import Escola
from neurodivergentes.models.historico_escolar import SeriesCursadas
from profissionais.models import Profissional
from django_multitenant.models import TenantModel, TenantManager
from clientes.models import Cliente
from encrypted_model_fields.fields import EncryptedCharField, EncryptedEmailField

def validate_future_date(value):
    if value > date.today():
        raise ValidationError('A data não pode ser no futuro.')

class Neurodivergente(TenantModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tenant_id = 'cliente_id'  # Define o campo tenant_id necessário para o django-multitenant
    
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    ]
    
    ESTADOS_CHOICES = [
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'),
        ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
        ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
        ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins'),
    ]

    # Dados Pessoais
    primeiro_nome = models.CharField('Primeiro Nome', max_length=50)
    ultimo_nome = models.CharField('Último Nome', max_length=50)
    data_nascimento = models.DateField(
        'Data de Nascimento',
        validators=[validate_future_date]
    )
    genero = models.CharField('Gênero', max_length=1, choices=GENDER_CHOICES)
    cpf = EncryptedCharField(max_length=14)
    rg = EncryptedCharField(max_length=20, blank=True, null=True)
    
    # Localização
    estado_nascimento = models.CharField(
        'Estado de Nascimento',
        max_length=2,
        choices=ESTADOS_CHOICES
    )
    cidade_nascimento = models.CharField('Cidade de Nascimento', max_length=100)
    
    # Endereço
    cep = EncryptedCharField(max_length=9)
    endereco = EncryptedCharField(max_length=255)
    numero = EncryptedCharField(max_length=10)
    complemento = EncryptedCharField(max_length=100, blank=True, null=True)
    bairro = EncryptedCharField(max_length=100)
    cidade = EncryptedCharField(max_length=100)
    estado = EncryptedCharField(max_length=2, choices=ESTADOS_CHOICES)
    
    # Contato
    celular = EncryptedCharField(max_length=15, blank=True, null=True)
    email = EncryptedEmailField(blank=True, null=True)
    
    # Foto
    foto_perfil = models.ImageField(
        'Foto de Perfil',
        upload_to='neurodivergentes/fotos/',
        blank=True,
        null=True
    )

    # Escola e Ano Escolar
    escola = models.ForeignKey(
        Escola,
        verbose_name='Escola',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='alunos',
        db_column='escola_id'  # Garante que o Django use a coluna correta
    )
    ano_escolar = models.ForeignKey(
        SeriesCursadas,
        verbose_name='Ano Escolar',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='alunos',
        db_column='ano_escolar_id'  # Ajuste se o nome da coluna for diferente
    )
    ativo = models.BooleanField('Ativo', default=True)

    # Campos de controle
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    objects = TenantManager()

    class Meta:
        verbose_name = 'Aluno/Paciente'
        verbose_name_plural = 'Alunos/Pacientes'
        ordering = ['primeiro_nome', 'ultimo_nome']
        
    def __str__(self):
        return f"{self.primeiro_nome} {self.ultimo_nome}"

    @property
    def nome_completo(self):
        return f"{self.primeiro_nome} {self.ultimo_nome}"
        
    def get_nome_completo(self):
        return f"{self.primeiro_nome} {self.ultimo_nome}"
    
    def foto_preview(self):
        if self.foto_perfil:
            return mark_safe(
                f'<img src="{self.foto_perfil.url}" width="150" alt="Foto de perfil" />'
            )
        return "Sem foto"
    foto_preview.short_description = 'Visualização da Foto'
    
    def idade(self):
        hoje = date.today()
        return hoje.year - self.data_nascimento.year - (
            (hoje.month, hoje.day) < 
            (self.data_nascimento.month, self.data_nascimento.day)
        )
    idade.short_description = 'Idade'

    def clean(self):
        super().clean()
        
        # Formata o CEP
        if self.cep:
            cep = ''.join(filter(str.isdigit, self.cep))
            if len(cep) == 8:
                self.cep = f'{cep[:5]}-{cep[5:]}'
        
        # Formata o celular
        if self.celular:
            celular = ''.join(filter(str.isdigit, self.celular))
            if len(celular) == 11:
                self.celular = f'({celular[:2]}) {celular[2:7]}-{celular[7:]}'
                
class GrupoFamiliar(TenantModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tenant_id = 'cliente_id'  # Define o campo tenant_id necessário para o django-multitenant
    
    neurodivergente = models.ForeignKey(
        Neurodivergente,
        on_delete=models.CASCADE,
        related_name='grupo_familiar'
    )
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    # Documentos dos membros
    cpf = EncryptedCharField(max_length=14, blank=True, null=True)
    rg = EncryptedCharField(max_length=20, blank=True, null=True)
    # Endereço residencial
    cep = EncryptedCharField(max_length=9, blank=True, null=True)
    endereco = EncryptedCharField(max_length=255, blank=True, null=True)
    numero = EncryptedCharField(max_length=10, blank=True, null=True)
    complemento = EncryptedCharField(max_length=100, blank=True, null=True)
    bairro = EncryptedCharField(max_length=100, blank=True, null=True)
    cidade = EncryptedCharField(max_length=100, blank=True, null=True)
    estado = EncryptedCharField(max_length=2, blank=True, null=True)
    # Dados de contato pessoais
    celular = EncryptedCharField(max_length=15, blank=True, null=True)
    email = EncryptedEmailField(blank=True, null=True)
    objects = TenantManager()