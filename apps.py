from django.apps import AppConfig

class CareerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'career'

    def ready(self):
        import career.models  # Ensures signals run
