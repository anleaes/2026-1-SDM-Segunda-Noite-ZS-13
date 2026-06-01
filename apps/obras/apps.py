from django.apps import AppConfig


class ObrasConfig(AppConfig):
    """Configuração do app de obras e restauração."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'obras'
    verbose_name = 'Obras de arte'
