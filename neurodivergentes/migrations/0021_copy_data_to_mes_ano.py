from django.db import migrations

def copiar_data_para_mes_ano(apps, schema_editor):
    Monitoramento = apps.get_model('neurodivergentes', 'Monitoramento')
    for monitoramento in Monitoramento.objects.all():
        # Copia a data existente para mes_ano, garantindo que o dia seja 1
        monitoramento.mes_ano = monitoramento.data.replace(day=1)
        monitoramento.save()

class Migration(migrations.Migration):

    dependencies = [
        ('neurodivergentes', '0020_add_mes_ano_to_monitoramento'),
    ]

    operations = [
        migrations.RunPython(copiar_data_para_mes_ano),
    ]
