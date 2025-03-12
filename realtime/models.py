from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.conf import settings

def validate_message_length(value):
    max_length = getattr(settings, 'MAX_MESSAGE_LENGTH', 10000)
    if len(value) > max_length:
        raise ValidationError(f'A mensagem não pode ter mais que {max_length} caracteres.')

def validate_different_users(sender_id, recipient_id):
    if sender_id == recipient_id:
        raise ValidationError('Você não pode enviar mensagem para si mesmo.')

class PrivateMessage(models.Model):
    sender = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name='Remetente',
        related_name='sent_messages'
    )
    recipient = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name='Destinatário', 
        related_name='received_messages'
    )
    message = models.TextField('Mensagem', validators=[validate_message_length])
    timestamp = models.DateTimeField('Data/Hora', default=timezone.now)
    is_read = models.BooleanField('Lida', default=False)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Mensagem'
        verbose_name_plural = 'Mensagens'
        indexes = [
            models.Index(fields=['sender', 'recipient']),
            models.Index(fields=['recipient', 'is_read'])
        ]

    def clean(self):
        try:
            # Verifica se os campos existem e não são None antes de validar
            if hasattr(self, 'sender_id') and hasattr(self, 'recipient_id') and self.sender_id and self.recipient_id:
                validate_different_users(self.sender_id, self.recipient_id)
            
            if not self.message or not self.message.strip():
                raise ValidationError('A mensagem não pode estar vazia.')
        except Exception as e:
            raise ValidationError(str(e))

    def save(self, *args, **kwargs):
        self.full_clean()
        self.message = self.message.strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.message[:50]}...' if len(self.message) > 50 else self.message
