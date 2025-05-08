from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.html import mark_safe
from django_multitenant.models import TenantModel, TenantManager
from clientes.models import Cliente
from encrypted_model_fields.fields import EncryptedCharField
import datetime

class Profissional(TenantModel):
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

    SIM_NAO_CHOICES = [
        (True, 'Sim'),
        (False, 'Não'),
    ]

    PROFISSAO_CHOICES = [
        ('', '---------'),  
        ('PROFISSIONAIS DA SAÚDE', (
            ('fisioterapeuta', 'Fisioterapeuta'),
            ('fonoaudiologo', 'Fonoaudiólogo'),
            ('musicoterapeuta', 'Musicoterapeuta'),
            ('neurologista', 'Neurologista'),
            ('neuropsicólogo', 'Neuropsicólogo'),
            ('psicologo', 'Psicólogo Clínico'),
            ('psiquiatra', 'Psiquiatra'),
            ('terapeuta', 'Terapeuta Ocupacional'),
        )),
        ('PROFISSIONAIS DA EDUCAÇÃO', (
            ('assistente_social', 'Assistente Social'),
            ('educador_especial', 'Educador Especial (AEE)'),
            ('neuropsicopedagogo', 'Neuropsicopedagogo'),
            ('pedagogo', 'Pedagogo'),
            ('psicopedagogo', 'Psicopedagogo'),
        )),
    ]

    # Relacionamento com User do Django
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profissional',
        verbose_name='Usuário'
    )

    # Dados Pessoais
    foto_perfil = models.ImageField(
        'Foto de Perfil',
        upload_to='profissionais_app/fotos/',
        blank=True,
        null=True
    )
    celular = EncryptedCharField(
        'Celular/WhatsApp',
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\(\d{2}\) \d{5}-\d{4}$',
                message='Formato inválido. Use (XX) XXXXX-XXXX'
            )
        ],
        help_text='Digite apenas os números. A formatação será aplicada automaticamente.'
    )
    data_nascimento = models.DateField('Data de Nascimento', blank=True, null=True)
    genero = models.CharField('Gênero', max_length=1, choices=GENDER_CHOICES)

    # Qualificação Profissional
    profissao = models.CharField(
        'Profissão',
        max_length=50,
        choices=PROFISSAO_CHOICES,
        blank=True
    )
    especialidade = models.CharField(
        'Especialidade',
        max_length=100,
        blank=True,
        help_text='Detalhe suas especializações'
    )
    registro_profissional = EncryptedCharField(
        'Nº do Registro Profissional',
        max_length=50,
        blank=True
    )
    estado_registro = models.CharField(
        'Estado de Registro',
        max_length=2,
        choices=ESTADOS_CHOICES,
        blank=True,
        null=True
    )
    formacao = models.TextField(
        'Formação',
        blank=True,
        help_text='Descreva sua formação acadêmica'
    )
    experiencia_neurodiversidade = models.BooleanField(
        'Experiência em neurodiversidade',
        choices=SIM_NAO_CHOICES,
        default=False
    )

    # Endereço
    cep = EncryptedCharField(
        'CEP',
        max_length=9,
        validators=[
            RegexValidator(
                regex=r'^\d{5}-\d{3}$',
                message='CEP inválido. Use o formato XXXXX-XXX'
            )
        ],
        blank=True,
        null=True
    )
    endereco = EncryptedCharField('Endereço', max_length=200, blank=True, null=True)
    numero = EncryptedCharField('Número', max_length=10, blank=True, null=True)
    complemento = EncryptedCharField('Complemento', max_length=100, blank=True, null=True)
    bairro = EncryptedCharField('Bairro', max_length=100, blank=True, null=True)
    cidade = EncryptedCharField('Cidade', max_length=100, blank=True, null=True)
    estado = EncryptedCharField('Estado', max_length=2, blank=True, null=True)

    # Outros
    biografia = models.TextField(
        'Biografia',
        blank=True,
        help_text='Uma breve apresentação sobre você'
    )
    facebook = models.URLField(
        'Facebook',
        blank=True,
        help_text='Link do seu perfil no Facebook'
    )
    instagram = models.URLField(
        'Instagram',
        blank=True,
        help_text='Link do seu perfil no Instagram'
    )

    # Campos de controle
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TenantManager()

    class Meta:
        verbose_name = 'Profissional'
        verbose_name_plural = 'Profissionais'
        ordering = ['user__first_name', 'user__last_name']

    def __str__(self):
        return self.user.get_full_name()

    def foto_preview(self):
        if self.foto_perfil:
            return mark_safe(
                f'<img src="{self.foto_perfil.url}" width="150" alt="Foto de perfil" />'
            )
        return "Sem foto"
    foto_preview.short_description = 'Visualização da Foto'

    def clean(self):
        # Validação da data de nascimento
        if self.data_nascimento:
            hoje = datetime.date.today()
            idade = hoje.year - self.data_nascimento.year - (
                (hoje.month, hoje.day) < 
                (self.data_nascimento.month, self.data_nascimento.day)
            )
            if idade < 18:
                raise ValidationError({
                    'data_nascimento': 'O profissional deve ter pelo menos 18 anos.'
                })

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