# Generated by Django 5.1.2 on 2025-04-27 22:44

import django.core.validators
import django.db.models.deletion
import django_multitenant.mixins
import django_multitenant.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clientes', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profissional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto_perfil', models.ImageField(blank=True, null=True, upload_to='profissionais_app/fotos/', verbose_name='Foto de Perfil')),
                ('celular', models.CharField(help_text='Digite apenas os números. A formatação será aplicada automaticamente.', max_length=15, validators=[django.core.validators.RegexValidator(message='Formato inválido. Use (XX) XXXXX-XXXX', regex='^\\(\\d{2}\\) \\d{5}-\\d{4}$')], verbose_name='Celular/WhatsApp')),
                ('data_nascimento', models.DateField(verbose_name='Data de Nascimento')),
                ('genero', models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino')], max_length=1, verbose_name='Gênero')),
                ('profissao', models.CharField(blank=True, choices=[('', '---------'), ('PROFISSIONAIS DA SAÚDE', [('fisioterapeuta', 'Fisioterapeuta'), ('fonoaudiologo', 'Fonoaudiólogo'), ('musicoterapeuta', 'Musicoterapeuta'), ('neurologista', 'Neurologista'), ('neuropsicólogo', 'Neuropsicólogo'), ('psicologo', 'Psicólogo Clínico'), ('psiquiatra', 'Psiquiatra'), ('terapeuta', 'Terapeuta Ocupacional')]), ('PROFISSIONAIS DA EDUCAÇÃO', [('assistente_social', 'Assistente Social'), ('educador_especial', 'Educador Especial (AEE)'), ('neuropsicopedagogo', 'Neuropsicopedagogo'), ('pedagogo', 'Pedagogo'), ('psicopedagogo', 'Psicopedagogo')])], max_length=50, verbose_name='Profissão')),
                ('especialidade', models.CharField(blank=True, help_text='Detalhe suas especializações', max_length=100, verbose_name='Especialidade')),
                ('registro_profissional', models.CharField(blank=True, max_length=50, verbose_name='Nº do Registro Profissional')),
                ('local_registro', models.CharField(blank=True, choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=2, verbose_name='Local do Registro')),
                ('formacao', models.TextField(blank=True, help_text='Descreva sua formação acadêmica', verbose_name='Formação')),
                ('experiencia_neurodiversidade', models.BooleanField(choices=[(True, 'Sim'), (False, 'Não')], default=False, verbose_name='Experiência em neurodiversidade')),
                ('cep', models.CharField(max_length=9, validators=[django.core.validators.RegexValidator(message='CEP inválido. Use o formato XXXXX-XXX', regex='^\\d{5}-\\d{3}$')], verbose_name='CEP')),
                ('endereco', models.CharField(max_length=200, verbose_name='Endereço')),
                ('numero', models.CharField(max_length=10, verbose_name='Número')),
                ('complemento', models.CharField(blank=True, max_length=100, verbose_name='Complemento')),
                ('bairro', models.CharField(max_length=100, verbose_name='Bairro')),
                ('cidade', models.CharField(max_length=100, verbose_name='Cidade')),
                ('estado', models.CharField(choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=2, verbose_name='Estado')),
                ('biografia', models.TextField(blank=True, help_text='Uma breve apresentação sobre você', verbose_name='Biografia')),
                ('facebook', models.URLField(blank=True, help_text='Link do seu perfil no Facebook', verbose_name='Facebook')),
                ('instagram', models.URLField(blank=True, help_text='Link do seu perfil no Instagram', verbose_name='Instagram')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientes.cliente')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profissional', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Profissional',
                'verbose_name_plural': 'Profissionais',
                'ordering': ['user__first_name', 'user__last_name'],
            },
            bases=(django_multitenant.mixins.TenantModelMixin, models.Model),
            managers=[
                ('objects', django_multitenant.models.TenantManager()),
            ],
        ),
    ]
