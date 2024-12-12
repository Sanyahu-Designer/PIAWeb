from django.apps import AppConfig

class ProfissionaisAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profissionais_app'
    verbose_name = 'Profissionais'

    def ready(self):
        import profissionais_app.signals