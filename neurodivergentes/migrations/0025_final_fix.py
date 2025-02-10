from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('neurodivergentes', '0024_cleanup_meta_fields'),
    ]

    operations = [
        migrations.RunSQL(
            """
            -- Remover a chave estrangeira existente
            ALTER TABLE neurodivergentes_monitoramento
            DROP FOREIGN KEY IF EXISTS fk_meta_habilidade;
            
            -- Alterar a coluna meta_id para NOT NULL e adicionar a chave estrangeira
            ALTER TABLE neurodivergentes_monitoramento
            MODIFY COLUMN meta_id bigint NOT NULL,
            ADD CONSTRAINT fk_meta_habilidade 
            FOREIGN KEY (meta_id) 
            REFERENCES neurodivergentes_metahabilidade(id);
            """,
            reverse_sql="""
            ALTER TABLE neurodivergentes_monitoramento
            DROP FOREIGN KEY fk_meta_habilidade;
            """
        ),
    ]
