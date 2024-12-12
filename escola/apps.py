from django.apps import AppConfig

class EscolaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'escola'
    verbose_name = 'Escolas'

    def ready(self):
        import escola.signals