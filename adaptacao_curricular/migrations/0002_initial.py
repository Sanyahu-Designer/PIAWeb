# Generated by Django 5.1.2 on 2025-04-27 22:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('adaptacao_curricular', '0001_initial'),
        ('clientes', '__first__'),
        ('escola', '0001_initial'),
        ('neurodivergentes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='adaptacaocurricularindividualizada',
            name='aluno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='neurodivergentes.neurodivergente', verbose_name='Aluno/Paciente'),
        ),
        migrations.AddField(
            model_name='adaptacaocurricularindividualizada',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientes.cliente'),
        ),
        migrations.AddField(
            model_name='adaptacaocurricularindividualizada',
            name='escola',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='escola.escola'),
        ),
    ]
