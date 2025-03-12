from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import ChatMessage
from django.contrib.auth.models import User

def save_chat_message(room: str, user: User, message: str) -> ChatMessage:
    """
    Salva uma mensagem de chat no banco de dados e notifica os participantes
    
    Args:
        room: Nome da sala de chat
        user: Usuário que enviou a mensagem
        message: Conteúdo da mensagem
    
    Returns:
        Instância de ChatMessage criada
    """
    chat_message = ChatMessage.objects.create(
        room=room,
        user=user,
        message=message
    )
    
    # Envia a mensagem via WebSocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"chat_{room}",
        {
            "type": "chat_message",
            "message": message,
            "user": user.username,
            "timestamp": chat_message.timestamp.isoformat()
        }
    )
    
    return chat_message
