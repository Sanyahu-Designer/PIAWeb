from django.apps import AppConfig

class NeurodivergentesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'neurodivergentes'
    verbose_name = 'Aluno/Paciente'

    def ready(self):
        import neurodivergentes.signals