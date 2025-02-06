from django.db import models
from django.core.exceptions import ValidationError
from ..models import Neurodivergente
from escola.models import Escola

class ParecerAvaliativo(models.Model):
    neurodivergente = models.ForeignKey(
        Neurodivergente,
        on_delete=models.CASCADE,
        related_name='pareceres'
    )
    escola = models.ForeignKey(
        Escola,
        on_delete=models.PROTECT,
        related_name='pareceres'
    )
    data_avaliacao = models.DateField('Data da Avaliação')
    evolucao = models.TextField('Descrição da Evolução')
    pontos_fortes = models.TextField('Pontos Fortes Observados')
    desafios = models.TextField('Desafios Identificados')
    recomendacoes = models.TextField('Recomendações')
    conclusoes = models.TextField('Conclusões')
    anexos = models.FileField(
        'Anexos',
        upload_to='neurodivergentes/pareceres/',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Parecer'
        verbose_name_plural = 'Pareceres'
        ordering = ['-data_avaliacao']

    def __str__(self):
        return f"Parecer de {self.neurodivergente} - {self.data_avaliacao}"

    def clean(self):
        # Verificar se a escola está ativa
        if not self.escola.ativo:
            raise ValidationError({
                'escola': 'A escola selecionada não está ativa.'
            })