from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils.html import mark_safe
from django.core.exceptions import ValidationError
from datetime import date
from escola.models import Escola
from profissionais.models import Profissional

def validate_future_date(value):
    if value > date.today():
        raise ValidationError('A data não pode ser no futuro.')

class Neurodivergente(models.Model):
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
    cpf = models.CharField(
        'CPF',
        max_length=14,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
                message='CPF inválido. Use o formato XXX.XXX.XXX-XX'
            )
        ]
    )
    rg = models.CharField('RG', max_length=20, blank=True, null=True)
    
    # Localização
    estado_nascimento = models.CharField(
        'Estado de Nascimento',
        max_length=2,
        choices=ESTADOS_CHOICES
    )
    cidade_nascimento = models.CharField('Cidade de Nascimento', max_length=100)
    
    # Endereço
    cep = models.CharField(
        'CEP',
        max_length=9,
        validators=[
            RegexValidator(
                regex=r'^\d{5}-\d{3}$',
                message='CEP inválido. Use o formato XXXXX-XXX'
            )
        ]
    )
    endereco = models.CharField('Endereço', max_length=255)
    numero = models.CharField('Número', max_length=10)
    complemento = models.CharField(
        'Complemento',
        max_length=100,
        blank=True,
        null=True
    )
    bairro = models.CharField('Bairro', max_length=100)
    cidade = models.CharField('Cidade', max_length=100)
    estado = models.CharField('Estado', max_length=2, choices=ESTADOS_CHOICES)
    
    # Contato
    celular = models.CharField(
        'Celular/WhatsApp',
        max_length=15,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\(\d{2}\) \d{5}-\d{4}$',
                message='Formato inválido. Use (XX) XXXXX-XXXX'
            )
        ]
    )
    email = models.EmailField('E-mail', blank=True, null=True)
    
    # Foto
    foto_perfil = models.ImageField(
        'Foto de Perfil',
        upload_to='neurodivergentes/fotos/',
        blank=True,
        null=True
    )
    
    # Campos de controle
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
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
                
class GrupoFamiliar(models.Model):
    neurodivergente = models.ForeignKey(
        Neurodivergente,
        on_delete=models.CASCADE,
        related_name='grupo_familiar'
    )
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()