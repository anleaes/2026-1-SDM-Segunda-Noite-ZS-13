from django.apps import AppConfig


class ContasConfig(AppConfig):
    """Configuração do app de usuários e autenticação."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contas'
    verbose_name = 'Contas e usuários'
