from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('neurodivergentes', '0023_alter_neurodivergente_verbose_name'),
    ]

    operations = [
        migrations.RunSQL(
            """
            -- Remover as chaves estrangeiras
            ALTER TABLE neurodivergentes_monitoramento
            DROP FOREIGN KEY IF EXISTS neurodivergentes_mon_meta_fk_id_b307e955_fk_neurodive,
            DROP FOREIGN KEY IF EXISTS neurodivergentes_mon_meta_new_id_b9c197f1_fk_neurodive,
            DROP FOREIGN KEY IF EXISTS neurodivergentes_mon_meta_nova_id_e8877c76_fk_neurodive;

            -- Remover as colunas antigas
            ALTER TABLE neurodivergentes_monitoramento
            DROP COLUMN meta_nova_id,
            DROP COLUMN meta_fk_id,
            DROP COLUMN meta_new_id;

            -- Alterar a coluna meta_id para ser bigint e aceitar NULL
            ALTER TABLE neurodivergentes_monitoramento
            MODIFY COLUMN meta_id bigint NULL;

            -- Adicionar a chave estrangeira
            ALTER TABLE neurodivergentes_monitoramento
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
