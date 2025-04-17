from django.apps import AppConfig


class AdaptacaoCurricularConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adaptacao_curricular'
    verbose_name = 'Plano Educacional Individualizado (PEI)'
    verbose_name_plural = 'Planos Educacionais Individualizados (PEIs)'
    label = 'adaptacao_curricular'
