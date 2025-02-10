from django.db import migrations, models

def copy_meta_to_metas(apps, schema_editor):
    Monitoramento = apps.get_model('neurodivergentes', 'Monitoramento')
    MonitoramentoMeta = apps.get_model('neurodivergentes', 'MonitoramentoMeta')
    db_alias = schema_editor.connection.alias
    
    for monitoramento in Monitoramento.objects.using(db_alias).all():
        if monitoramento.meta_id:
            MonitoramentoMeta.objects.using(db_alias).create(
                monitoramento=monitoramento,
                meta_id=monitoramento.meta_id
            )

class Migration(migrations.Migration):

    dependencies = [
        ('neurodivergentes', '0029_alter_observacoes'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonitoramentoMeta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='monitoramento_metas', to='neurodivergentes.metahabilidade')),
                ('monitoramento', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='monitoramento_metas', to='neurodivergentes.monitoramento')),
            ],
            options={
                'db_table': 'neurodivergentes_monitoramento_metas',
                'unique_together': {('monitoramento', 'meta')},
            },
        ),
        migrations.AddField(
            model_name='monitoramento',
            name='metas',
            field=models.ManyToManyField(help_text='Selecione uma ou mais metas/habilidades para este planejamento', through='neurodivergentes.MonitoramentoMeta', to='neurodivergentes.metahabilidade', verbose_name='Metas/Habilidades'),
        ),
        migrations.RunPython(copy_meta_to_metas),
        migrations.RemoveField(
            model_name='monitoramento',
            name='meta',
        ),
        migrations.AlterUniqueTogether(
            name='monitoramento',
            unique_together={('neurodivergente', 'mes', 'ano')},
        ),
    ]
