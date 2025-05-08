from django.db import models
from django_multitenant.models import TenantModel, TenantManager
from clientes.models import Cliente

class RotinaAtividade(TenantModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tenant_id = 'cliente_id'  # Define o campo tenant_id necessário para o django-multitenant
    
    anamnese = models.ForeignKey(
        'neurodivergentes.Anamnese',
        on_delete=models.CASCADE,
        related_name='rotinas'
    )
    horario = models.TimeField('Horário')
    atividade = models.CharField('Atividade', max_length=200)
    observacoes = models.TextField('Observações', blank=True, null=True)
    objects = TenantManager()
    
    class Meta:
        verbose_name = 'Atividade da Rotina'
        verbose_name_plural = 'Atividades da Rotina'
        ordering = ['horario']

    def __str__(self):
        return f"{self.horario.strftime('%H:%M')} - {self.atividade}"