from django.db import models
from django.core.exceptions import ValidationError
from .base import Neurodivergente, validate_future_date

class GrupoFamiliar(models.Model):
    VINCULO_CHOICES = [
        ('pai_mae', 'Pai/Mãe'),
        ('filho', 'Filho(a)'),
        ('irmao', 'Irmão(ã)'),
        ('avo', 'Avô/Avó'),
        ('tio', 'Tio(a)'),
        ('sobrinho', 'Sobrinho(a)'),
        ('primo', 'Primo(a)'),
        ('conjuge', 'Cônjuge'),
        ('companheiro', 'Companheiro(a)'),
        ('padrasto', 'Padrasto/Madrasta'),
        ('enteado', 'Enteado(a)'),
        ('cunhado', 'Cunhado(a)'),
        ('genro', 'Genro/Nora'),
        ('sogro', 'Sogro(a)'),
        ('tutor', 'Tutor(a)'),
        ('cuidador', 'Cuidador(a)'),
        ('outro', 'Outro'),
    ]
    
    neurodivergente = models.ForeignKey(
        Neurodivergente,
        on_delete=models.CASCADE,
        related_name='grupo_familiar'
    )
    primeiro_nome = models.CharField('Primeiro Nome', max_length=50)
    ultimo_nome = models.CharField('Último Nome', max_length=50)
    data_nascimento = models.DateField(
        'Data de Nascimento',
        validators=[validate_future_date]
    )
    vinculo = models.CharField(
        'Vínculo/Parentesco',
        max_length=20,
        choices=VINCULO_CHOICES
    )
    outro_vinculo = models.CharField(
        'Especificar outro vínculo',
        max_length=50,
        blank=True,
        null=True
    )
    ocupacao = models.CharField('Ocupação', max_length=100)
    
    class Meta:
        verbose_name = 'Membro do Grupo Familiar'
        verbose_name_plural = 'Grupo Familiar'
        ordering = ['neurodivergente', 'primeiro_nome']
        
    def __str__(self):
        return f"{self.primeiro_nome} {self.ultimo_nome} - {self.get_vinculo_display()}"
    
    def clean(self):
        if self.vinculo == 'outro' and not self.outro_vinculo:
            raise ValidationError({
                'outro_vinculo': 'Por favor, especifique o vínculo.'
            })