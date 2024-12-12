from django.db import models
from django.core.exceptions import ValidationError
from profissionais_app.models import Profissional

class PlanoEducacional(models.Model):
    pdi = models.OneToOneField(
        'PDI',
        on_delete=models.CASCADE,
        related_name='plano_educacional',
        verbose_name='PDI'
    )
    data_inicio = models.DateField('Data de Início')
    data_fim = models.DateField('Data de Finalização')
    pedagogo_responsavel = models.ForeignKey(
        Profissional,
        on_delete=models.PROTECT,
        related_name='planos_educacionais',
        limit_choices_to={'profissao__startswith': 'educador'}
    )
    objetivos = models.TextField('Objetivos')
    estrategias = models.TextField('Estratégias')
    recursos = models.TextField('Recursos Necessários')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Adaptação Curricular Individualizada'
        verbose_name_plural = 'Adaptações Curriculares Individualizadas'

    def __str__(self):
        return f"ACI de {self.pdi.neurodivergente}"

    def clean(self):
        if self.data_fim and self.data_inicio and self.data_fim < self.data_inicio:
            raise ValidationError({
                'data_fim': 'A data de finalização não pode ser anterior à data de início.'
            })

class AdaptacaoCurricular(models.Model):
    plano_educacional = models.ForeignKey(
        PlanoEducacional,
        on_delete=models.CASCADE,
        related_name='adaptacoes'
    )
    data_inicio = models.DateField('Data de Início')
    data_fim = models.DateField('Data de Finalização')
    professor_responsavel = models.ForeignKey(
        Profissional,
        on_delete=models.PROTECT,
        related_name='adaptacoes_curriculares',
        limit_choices_to={'profissao__startswith': 'educador'}
    )
    componente_curricular = models.CharField('Componente Curricular', max_length=100)
    conteudo_adaptado = models.TextField('Conteúdo Adaptado')
    estrategias = models.TextField('Estratégias de Ensino')
    recursos = models.TextField('Recursos Didáticos')
    avaliacao = models.TextField('Processo Avaliativo')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Adaptação Curricular'
        verbose_name_plural = 'Adaptações Curriculares'
        ordering = ['-data_inicio']

    def __str__(self):
        return f"Adaptação em {self.componente_curricular} para {self.plano_educacional.pdi.neurodivergente}"

    def clean(self):
        if self.data_fim and self.data_inicio and self.data_fim < self.data_inicio:
            raise ValidationError({
                'data_fim': 'A data de finalização não pode ser anterior à data de início.'
            })