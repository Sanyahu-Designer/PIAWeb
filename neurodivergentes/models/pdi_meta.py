from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class PDIMeta(models.Model):
    pdi = models.ForeignKey(
        'PDI',
        on_delete=models.CASCADE,
        related_name='metas'
    )
    meta_habilidade = models.ForeignKey(
        'MetaHabilidade',
        on_delete=models.PROTECT,
        verbose_name='Meta/Habilidade'
    )
    nivel_desenvolvimento = models.IntegerField(
        'Nível de Desenvolvimento (%)',
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ],
        default=0
    )
    ordem = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = 'Meta do PDI'
        verbose_name_plural = 'Metas do PDI'
        ordering = ['ordem']
        # Remover unique_together se não for necessário
        # unique_together = ['pdi', 'meta_habilidade']

    def __str__(self):
        return f"{self.meta_habilidade} - {self.nivel_desenvolvimento}%"

    def clean(self):
        if self.nivel_desenvolvimento > 100:
            raise ValidationError({
                'nivel_desenvolvimento': 'O nível de desenvolvimento não pode ser maior que 100%.'
            })
        elif self.nivel_desenvolvimento < 0:
            raise ValidationError({
                'nivel_desenvolvimento': 'O nível de desenvolvimento não pode ser menor que 0%.'
            })