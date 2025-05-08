from django.db import models
from django_multitenant.models import TenantModel, TenantManager
from clientes.models import Cliente

class Medicacao(TenantModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tenant_id = 'cliente_id'  # Define o campo tenant_id necessário para o django-multitenant
    
    anamnese = models.ForeignKey(
        'neurodivergentes.Anamnese',
        on_delete=models.CASCADE,
        related_name='medicacoes'
    )
    nome = models.CharField('Nome da Medicação', max_length=100)
    dosagem = models.CharField('Dosagem', max_length=50)
    frequencia = models.CharField('Frequência', max_length=100)
    objects = TenantManager()

    class Meta:
        verbose_name = 'Medicação'
        verbose_name_plural = 'Medicações'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.dosagem}"