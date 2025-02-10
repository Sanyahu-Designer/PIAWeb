from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('neurodivergentes', '0027_fix_monitoramento_dates'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monitoramento',
            name='nivel',
        ),
    ]
