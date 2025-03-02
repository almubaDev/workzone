from django.apps import AppConfig

class MEECETeacherManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MEECETeacherManager'

    def ready(self):
        import MEECETeacherManager.signals  # Importar las señales