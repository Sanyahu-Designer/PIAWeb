from django.db import models
from django.core.validators import RegexValidator
from profissionais_app.models import Profissional

class ModalidadeEnsino(models.Model):
    nome = models.CharField('Nome', max_length=100)
    descricao = models.TextField('Descrição')
    idade_minima = models.IntegerField('Idade Mínima', null=True, blank=True)
    idade_maxima = models.IntegerField('Idade Máxima', null=True, blank=True)
    ativo = models.BooleanField('Ativo', default=True)

    class Meta:
        verbose_name = 'Modalidade de Ensino'
        verbose_name_plural = 'Modalidades de Ensino'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def clean(self):
        if self.idade_minima and self.idade_maxima:
            if self.idade_minima > self.idade_maxima:
                raise ValidationError({
                    'idade_minima': 'A idade mínima não pode ser maior que a idade máxima.'
                })

class ProgramaEducacional(models.Model):
    TIPOS_PROGRAMA = [
        ('inclusao', 'Inclusão'),
        ('reforco', 'Reforço Escolar Adaptado'),
        ('comportamental', 'Intervenção Comportamental'),
        ('metodologias', 'Metodologias Pedagógicas Adaptadas'),
    ]

    nome = models.CharField('Nome', max_length=100)
    tipo = models.CharField('Tipo', max_length=20, choices=TIPOS_PROGRAMA)
    descricao = models.TextField('Descrição')
    ativo = models.BooleanField('Ativo', default=True)

    class Meta:
        verbose_name = 'Programa Educacional'
        verbose_name_plural = 'Programas Educacionais'

    def __str__(self):
        return self.nome

class Recurso(models.Model):
    TIPOS_RECURSO = [
        ('sensorial', 'Salas Sensoriais'),
        ('tecnologia', 'Tecnologias Assistivas'),
        ('material', 'Materiais Adaptados'),
        ('acessibilidade', 'Dispositivos de Acessibilidade'),
        ('fisica', 'Acessibilidade Física'),
    ]

    nome = models.CharField('Nome', max_length=100)
    tipo = models.CharField('Tipo', max_length=20, choices=TIPOS_RECURSO)
    descricao = models.TextField('Descrição')
    ativo = models.BooleanField('Ativo', default=True)

    class Meta:
        verbose_name = 'Recurso'
        verbose_name_plural = 'Recursos'

    def __str__(self):
        return self.nome

class Escola(models.Model):
    TIPOS_ESCOLA = [
        ('publica', 'Pública'),
        ('privada', 'Privada'),
        ('especial', 'Escola Especial'),
    ]

    TURNOS = [
        ('manha', 'Manhã'),
        ('tarde', 'Tarde'),
        ('diurno', 'Diurno'),
        ('noite', 'Noturno'),
        ('integral', 'Integral'),
    ]

    ESTADOS = [
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

    # Informações Básicas
    nome = models.CharField('Nome', max_length=200)
    codigo_inep = models.CharField(
        'Código INEP',
        max_length=8,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{8}$',
                message='O código INEP deve conter exatamente 8 dígitos numéricos.'
            )
        ]
    )

    # Contato
    telefone = models.CharField(
        'Telefone',
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\(\d{2}\) \d{5}-\d{4}$',
                message='O telefone deve estar no formato (XX) XXXXX-XXXX'
            )
        ]
    )
    email = models.EmailField('E-mail')
    diretor = models.CharField('Diretor(a)', max_length=100)

    # Endereço
    cep = models.CharField(
        'CEP',
        max_length=9,
        validators=[
            RegexValidator(
                regex=r'^\d{5}-\d{3}$',
                message='O CEP deve estar no formato XXXXX-XXX'
            )
        ]
    )
    endereco = models.CharField('Endereço', max_length=200)
    numero = models.CharField('Número', max_length=10)
    complemento = models.CharField('Complemento', max_length=100, blank=True)
    bairro = models.CharField('Bairro', max_length=100)
    cidade = models.CharField('Cidade', max_length=100)
    estado = models.CharField('Estado', max_length=2, choices=ESTADOS)

    # Classificação
    tipo = models.CharField('Tipo', max_length=10, choices=TIPOS_ESCOLA)
    modalidades = models.ManyToManyField(
        ModalidadeEnsino,
        verbose_name='Modalidades de Ensino',
        blank=True  # Tornando o campo opcional
    )
    turnos = models.CharField('Turnos', max_length=10, choices=TURNOS)

    # Campos Associativos
    capacidade_atendimento = models.IntegerField('Capacidade de Atendimento')
    programas_educacionais = models.ManyToManyField(
        ProgramaEducacional,
        verbose_name='Programas Educacionais',
        blank=True
    )
    recursos_disponiveis = models.ManyToManyField(
        Recurso,
        verbose_name='Recursos Disponíveis',
        blank=True
    )

    # Equipe Multiprofissional
    profissionais_educacao = models.ManyToManyField(
        Profissional,
        verbose_name='Profissionais da Educação',
        related_name='escolas_educacao',
        limit_choices_to={
            'profissao__in': [
                'educador_especial',
                'neuropsicopedagogo',
                'pedagogo',
                'psicopedagogo',
                'assistente_social'
            ]
        },
        blank=True
    )

    profissionais_saude = models.ManyToManyField(
        Profissional,
        verbose_name='Profissionais da Saúde',
        related_name='escolas_saude',
        limit_choices_to={
            'profissao__in': [
                'fisioterapeuta',
                'fonoaudiologo',
                'musicoterapeuta',
                'neurologista',
                'neuropsicólogo',
                'psicologo',
                'psiquiatra',
                'terapeuta'
            ]
        },
        blank=True
    )

    # Controle
    ativo = models.BooleanField('Ativo', default=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Escola'
        verbose_name_plural = 'Escolas'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def clean(self):
        # Validação personalizada pode ser adicionada aqui
        pass

class AnoEscolar(models.Model):
    nome = models.CharField('Ano Escolar', max_length=50)
    ativo = models.BooleanField('Ativo', default=True)

    class Meta:
        verbose_name = 'Ano Escolar'
        verbose_name_plural = 'Anos Escolares'
        ordering = ['nome']

    def __str__(self):
        return self.nome