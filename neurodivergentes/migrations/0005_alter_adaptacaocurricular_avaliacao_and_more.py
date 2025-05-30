# Generated by Django 5.1.6 on 2025-04-29 14:29

import encrypted_model_fields.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('neurodivergentes', '0004_alter_registroevolucao_descricao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adaptacaocurricular',
            name='avaliacao',
            field=encrypted_model_fields.fields.EncryptedTextField(verbose_name='Processo Avaliativo'),
        ),
        migrations.AlterField(
            model_name='adaptacaocurricular',
            name='conteudo_adaptado',
            field=encrypted_model_fields.fields.EncryptedTextField(verbose_name='Conteúdo Adaptado'),
        ),
        migrations.AlterField(
            model_name='adaptacaocurricular',
            name='estrategias',
            field=encrypted_model_fields.fields.EncryptedTextField(verbose_name='Estratégias de Ensino'),
        ),
        migrations.AlterField(
            model_name='adaptacaocurricular',
            name='recursos',
            field=encrypted_model_fields.fields.EncryptedTextField(verbose_name='Recursos Didáticos'),
        ),
        migrations.AlterField(
            model_name='pdi',
            name='observacoes',
            field=encrypted_model_fields.fields.EncryptedTextField(blank=True, null=True, verbose_name='Diário de Classe'),
        ),
        migrations.AlterField(
            model_name='planoeducacional',
            name='estrategias',
            field=encrypted_model_fields.fields.EncryptedTextField(verbose_name='Estratégias'),
        ),
        migrations.AlterField(
            model_name='planoeducacional',
            name='objetivos',
            field=encrypted_model_fields.fields.EncryptedTextField(verbose_name='Objetivos'),
        ),
        migrations.AlterField(
            model_name='planoeducacional',
            name='recursos',
            field=encrypted_model_fields.fields.EncryptedTextField(verbose_name='Recursos Necessários'),
        ),
    ]
