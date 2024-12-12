from django.db import models

class Medicacao(models.Model):
    anamnese = models.ForeignKey(
        'neurodivergentes.Anamnese',
        on_delete=models.CASCADE,
        related_name='medicacoes'
    )
    nome = models.CharField('Nome da Medicação', max_length=100)
    dosagem = models.CharField('Dosagem', max_length=50)
    frequencia = models.CharField('Frequência', max_length=100)
    
    class Meta:
        verbose_name = 'Medicação'
        verbose_name_plural = 'Medicações'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.dosagem}"