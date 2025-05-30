# Generated by Django 5.1.6 on 2025-04-29 14:23

import encrypted_model_fields.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('neurodivergentes', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anamnese',
            name='aspectos_cognitivos',
            field=encrypted_model_fields.fields.EncryptedTextField(verbose_name='Aspectos Cognitivos'),
        ),
        migrations.AlterField(
            model_name='anamnese',
            name='aspectos_emocionais',
            field=encrypted_model_fields.fields.EncryptedTextField(verbose_name='Aspectos Emocionais/Sociais'),
        ),
        migrations.AlterField(
            model_name='anamnese',
            name='aspectos_psicomotores',
            field=encrypted_model_fields.fields.EncryptedTextField(verbose_name='Aspectos Psicomotores'),
        ),
        migrations.AlterField(
            model_name='anamnese',
            name='aspectos_sensoriais',
            field=encrypted_model_fields.fields.EncryptedTextField(verbose_name='Aspectos Sensoriais'),
        ),
        migrations.AlterField(
            model_name='anamnese',
            name='autonomia',
            field=encrypted_model_fields.fields.EncryptedTextField(verbose_name='Autonomia'),
        ),
        migrations.AlterField(
            model_name='anamnese',
            name='comportamento_familiar',
            field=encrypted_model_fields.fields.EncryptedTextField(blank=True, verbose_name='Comportamento no Ambiente Familiar'),
        ),
        migrations.AlterField(
            model_name='anamnese',
            name='comportamento_social',
            field=encrypted_model_fields.fields.EncryptedTextField(blank=True, verbose_name='Comportamento no Ambiente Social e Escolar'),
        ),
        migrations.AlterField(
            model_name='anamnese',
            name='comunicacao',
            field=encrypted_model_fields.fields.EncryptedTextField(verbose_name='Comunicação'),
        ),
        migrations.AlterField(
            model_name='anamnese',
            name='descricao_restricoes',
            field=encrypted_model_fields.fields.EncryptedTextField(blank=True, null=True, verbose_name='Descrição das Restrições Alimentares'),
        ),
        migrations.AlterField(
            model_name='anamnese',
            name='historia_vida',
            field=encrypted_model_fields.fields.EncryptedTextField(verbose_name='História de Vida'),
        ),
        migrations.AlterField(
            model_name='anamnese',
            name='observacoes_parto',
            field=encrypted_model_fields.fields.EncryptedTextField(blank=True, verbose_name='Observações sobre o Parto'),
        ),
        migrations.AlterField(
            model_name='anamnese',
            name='queixa_inicial',
            field=encrypted_model_fields.fields.EncryptedTextField(verbose_name='Queixa Inicial'),
        ),
        migrations.AlterField(
            model_name='rotinaatividade',
            name='observacoes',
            field=encrypted_model_fields.fields.EncryptedTextField(blank=True, null=True, verbose_name='Observações'),
        ),
    ]
