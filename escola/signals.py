from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Escola

@receiver(post_save, sender=Escola)
def escola_saved(sender, instance, **kwargs):
    # Clear cache when a school is saved
    cache.delete(f'escola_{instance.id}')
    cache.delete('escolas_ativas')

@receiver(post_delete, sender=Escola)
def escola_deleted(sender, instance, **kwargs):
    # Clear cache when a school is deleted
    cache.delete(f'escola_{instance.id}')
    cache.delete('escolas_ativas')