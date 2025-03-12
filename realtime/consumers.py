import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import PrivateMessage
import logging

logger = logging.getLogger(__name__)

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
            return

        self.user_group = f"notifications_{self.scope['user'].id}"
        
        try:
            await self.channel_layer.group_add(
                self.user_group,
                self.channel_name
            )
            await self.accept()
            logger.info(f"NotificationConsumer conectado para usuário {self.scope['user'].username}")
        except Exception as e:
            logger.error(f"Erro ao conectar NotificationConsumer: {str(e)}")
            await self.close()

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(
                self.user_group,
                self.channel_name
            )
            logger.info(f"NotificationConsumer desconectado para usuário {self.scope['user'].username}")
        except Exception as e:
            logger.error(f"Erro ao desconectar NotificationConsumer: {str(e)}")

    async def notification_message(self, event):
        """Envia uma notificação para o WebSocket"""
        try:
            await self.send(text_data=json.dumps({
                'type': 'notification',
                'message': event.get('message', ''),
                'count': await self.get_unread_count()
            }))
        except Exception as e:
            logger.error(f"Erro ao enviar notificação: {str(e)}")

    @database_sync_to_async
    def get_unread_count(self):
        """Retorna o número de mensagens não lidas do usuário"""
        return PrivateMessage.objects.filter(
            recipient=self.scope['user'],
            is_read=False
        ).count()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
            return

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user': self.scope["user"].username,
                }
            )
        except Exception as e:
            logger.error(f"Erro ao receber mensagem: {str(e)}")
            await self.send(text_data=json.dumps({
                'error': 'Erro ao processar mensagem'
            }))

    async def chat_message(self, event):
        try:
            await self.send(text_data=json.dumps({
                'type': 'chat_message',
                'message': event['message'],
                'user': event['user']
            }))
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem de chat: {str(e)}")
