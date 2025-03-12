from django.db import migrations

def migrate_old_to_new_fields(apps, schema_editor):
    ChatMessage = apps.get_model('realtime', 'ChatMessage')
    for message in ChatMessage.objects.all():
        # Copia o usuário antigo para o remetente
        message.sender = message.user
        message.save()
        
        # Adiciona o destinatário baseado na sala
        # A sala contém os IDs dos usuários, então vamos pegar o outro usuário
        user_ids = message.room.split('_')
        for user_id in user_ids:
            if user_id.isdigit():
                user_id = int(user_id)
                if user_id != message.user.id:
                    message.recipients.add(user_id)
        
        # Se a mensagem foi lida, adiciona o destinatário ao read_by
        if message.read:
            for recipient in message.recipients.all():
                message.read_by.add(recipient)

class Migration(migrations.Migration):
    dependencies = [
        ('realtime', '0003_alter_chatmessage_options_and_more'),
    ]

    operations = [
        migrations.RunPython(migrate_old_to_new_fields),
    ]
