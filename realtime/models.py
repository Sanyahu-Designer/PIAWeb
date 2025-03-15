from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def validate_message_length(value):
    max_length = getattr(settings, 'MAX_MESSAGE_LENGTH', 10000)
    if len(value) > max_length:
        raise ValidationError(f'A mensagem não pode ter mais que {max_length} caracteres.')

class PrivateMessage(models.Model):
    STATUS_CHOICES = (
        ('active', 'Ativa'),
        ('deleted', 'Excluída'),
        ('archived', 'Arquivada'),
    )
    
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
    status = models.CharField('Status', max_length=10, default='active')
    delivered_at = models.DateTimeField('Entregue em', null=True, blank=True)
    read_at = models.DateTimeField('Lida em', null=True, blank=True)
    reply_to = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name='Resposta para'
    )
    has_notification = models.BooleanField('Tem notificação', default=False)
    deleted_by_sender = models.BooleanField(default=False)
    deleted_by_recipient = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Mensagem'
        verbose_name_plural = 'Mensagens'
        indexes = [
            models.Index(fields=['sender', 'recipient']),
            models.Index(fields=['recipient', 'is_read'])
        ]

    def __str__(self):
        return f'{self.message[:50]}...' if len(self.message) > 50 else self.message

    def mark_as_deleted_for_user(self, user):
        """Marca a mensagem como excluída para um usuário específico"""
        if user == self.sender:
            self.deleted_by_sender = True
            self.save(update_fields=['deleted_by_sender'])
            return True
        elif user == self.recipient:
            self.deleted_by_recipient = True
            self.save(update_fields=['deleted_by_recipient'])
            return True
        return False
    
    def is_deleted_for_user(self, user):
        """Verifica se a mensagem está excluída para um usuário específico"""
        if user == self.sender:
            return self.deleted_by_sender
        elif user == self.recipient:
            return self.deleted_by_recipient
        return False
