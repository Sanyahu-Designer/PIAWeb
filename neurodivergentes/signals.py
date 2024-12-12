from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Neurodivergente, PDI, RegistroEvolucao

@receiver(post_save, sender=Neurodivergente)
def neurodivergente_saved(sender, instance, **kwargs):
    # Clear cache when a neurodivergente is saved
    cache.delete(f'neurodivergente_{instance.id}')
    cache.delete('neurodivergentes_ativos')

@receiver(post_delete, sender=Neurodivergente)
def neurodivergente_deleted(sender, instance, **kwargs):
    # Clear cache when a neurodivergente is deleted
    cache.delete(f'neurodivergente_{instance.id}')
    cache.delete('neurodivergentes_ativos')

@receiver(post_save, sender=PDI)
def pdi_saved(sender, instance, **kwargs):
    # Clear cache when a PDI is saved
    cache.delete(f'pdi_{instance.id}')
    cache.delete(f'pdis_neurodivergente_{instance.neurodivergente_id}')

@receiver(post_save, sender=RegistroEvolucao)
def evolucao_saved(sender, instance, **kwargs):
    # Clear cache when an evolution record is saved
    cache.delete(f'evolucao_{instance.id}')
    cache.delete(f'evolucoes_neurodivergente_{instance.neurodivergente_id}')