from django.db import models

class RotinaAtividade(models.Model):
    anamnese = models.ForeignKey(
        'neurodivergentes.Anamnese',
        on_delete=models.CASCADE,
        related_name='rotinas'
    )
    horario = models.TimeField('Horário')
    atividade = models.CharField('Atividade', max_length=200)
    observacoes = models.TextField('Observações', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Atividade da Rotina'
        verbose_name_plural = 'Atividades da Rotina'
        ordering = ['horario']

    def __str__(self):
        return f"{self.horario.strftime('%H:%M')} - {self.atividade}"