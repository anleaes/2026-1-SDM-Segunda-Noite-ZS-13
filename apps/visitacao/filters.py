import django_filters

from .models import Ingresso, Pagamento, Reserva


class IngressoFilter(django_filters.FilterSet):
    status = django_filters.CharFilter()
    tipo = django_filters.CharFilter()
    exposicao = django_filters.NumberFilter(field_name='exposicao_id')
    visitante = django_filters.NumberFilter(field_name='visitante_id')

    class Meta:
        model = Ingresso
        fields = ['status', 'tipo', 'exposicao', 'visitante']


class ReservaFilter(django_filters.FilterSet):
    status = django_filters.CharFilter()
    exposicao = django_filters.NumberFilter(field_name='exposicao_id')
    visitante = django_filters.NumberFilter(field_name='visitante_id')

    class Meta:
        model = Reserva
        fields = ['status', 'exposicao', 'visitante']


class PagamentoFilter(django_filters.FilterSet):
    status = django_filters.CharFilter()
    metodo = django_filters.CharFilter()

    class Meta:
        model = Pagamento
        fields = ['status', 'metodo']
