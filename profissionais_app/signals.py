from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Profissional

@receiver(post_save, sender=Profissional)
def profissional_saved(sender, instance, **kwargs):
    # Clear cache when a professional is saved
    cache.delete(f'profissional_{instance.id}')
    cache.delete('profissionais_ativos')

@receiver(post_delete, sender=Profissional)
def profissional_deleted(sender, instance, **kwargs):
    # Clear cache when a professional is deleted
    cache.delete(f'profissional_{instance.id}')
    cache.delete('profissionais_ativos')