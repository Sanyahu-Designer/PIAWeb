from django.db import migrations, models
import django.utils.timezone

class Migration(migrations.Migration):

    dependencies = [
        ('neurodivergentes', '0026_fix_mes_ano'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='monitoramento',
            options={'ordering': ['-ano', '-mes'], 'verbose_name': 'PEI', 'verbose_name_plural': 'PEI'},
        ),
    ]
