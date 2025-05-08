from django.db import models
from django_multitenant.models import TenantModel, TenantManager
from clientes.models import Cliente


class CategoriaNeurodivergente(TenantModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tenant_id = 'cliente_id'  # Define o campo tenant_id necessário para o django-multitenant
    
    nome = models.CharField('Nome', max_length=100)
    descricao = models.TextField('Descrição', blank=True)
    ordem = models.IntegerField('Ordem de exibição', default=0)
    
    objects = TenantManager()
    
    class Meta:
        verbose_name = 'Categoria Neurodivergente'
        verbose_name_plural = 'Categorias Neurodivergentes'
        ordering = ['ordem', 'nome']
        unique_together = ['cliente', 'nome']
    
    def __str__(self):
        return self.nome


class CondicaoNeurodivergente(TenantModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tenant_id = 'cliente_id'  # Define o campo tenant_id necessário para o django-multitenant
    
    nome = models.CharField('Nome', max_length=100)
    cid_10 = models.CharField('CID-10', max_length=10)
    descricao = models.TextField('Descrição', blank=True)
    ativo = models.BooleanField('Ativo', default=True)
    categoria = models.ForeignKey(
        CategoriaNeurodivergente, 
        on_delete=models.CASCADE,
        related_name='condicoes',
        verbose_name='Categoria'
    )
    
    objects = TenantManager()
    
    class Meta:
        verbose_name = 'Condição Neurodivergente'
        verbose_name_plural = 'Condições Neurodivergentes'
        ordering = ['categoria__ordem', 'nome']
        unique_together = ['cliente', 'cid_10']
    
    def __str__(self):
        return f"{self.nome} ({self.cid_10})"
