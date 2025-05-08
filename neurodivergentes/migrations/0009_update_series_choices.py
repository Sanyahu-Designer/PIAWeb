from django.db import migrations

def update_maternal_series(apps, schema_editor):
    SeriesCursadas = apps.get_model('neurodivergentes', 'SeriesCursadas')
    
    # Atualizar registros existentes
    # Alterar 'maternal' para 'maternal1'
    for serie in SeriesCursadas.objects.filter(nome='maternal'):
        serie.nome = 'maternal1'
        serie.save()

class Migration(migrations.Migration):

    dependencies = [
        ('neurodivergentes', '0008_alter_monitoramento_mes_alter_seriescursadas_nome_and_more'),
    ]

    operations = [
        migrations.RunPython(update_maternal_series),
    ]
