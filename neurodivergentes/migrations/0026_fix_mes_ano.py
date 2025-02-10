from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('neurodivergentes', '0025_final_fix'),
    ]

    operations = [
        migrations.RunSQL(
            """
            -- Alterar a coluna mes_ano para ter um valor padrão
            ALTER TABLE neurodivergentes_monitoramento
            MODIFY COLUMN mes_ano date NOT NULL DEFAULT (CURRENT_DATE);
            """,
            reverse_sql="""
            ALTER TABLE neurodivergentes_monitoramento
            MODIFY COLUMN mes_ano date NOT NULL;
            """
        ),
    ]
