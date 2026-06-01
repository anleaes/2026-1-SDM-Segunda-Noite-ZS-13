from django.apps import AppConfig


class VisitacaoConfig(AppConfig):
    """Configuração do app de visitação e pagamentos."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'visitacao'
    verbose_name = 'Visitas, ingressos e pagamentos'
