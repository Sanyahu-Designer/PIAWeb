from django.db import migrations, models
import ckeditor.fields

class Migration(migrations.Migration):

    dependencies = [
        ('neurodivergentes', '0028_remove_nivel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitoramento',
            name='observacoes',
            field=ckeditor.fields.RichTextField(
                verbose_name='Planejamento',
                help_text='Descreva o planejamento para esta meta/habilidade'
            ),
        ),
    ]
