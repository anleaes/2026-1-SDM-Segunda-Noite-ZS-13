import django_filters

from .models import Exposicao, Galeria, Ingresso, ObraArte, Pagamento, Reserva


class GaleriaFilter(django_filters.FilterSet):
    aberta = django_filters.BooleanFilter()

    class Meta:
        model = Galeria
        fields = ['aberta']


class ObraArteFilter(django_filters.FilterSet):
    categoria = django_filters.NumberFilter(field_name='categoria_id')
    ano_criacao = django_filters.NumberFilter()

    class Meta:
        model = ObraArte
        fields = ['categoria', 'ano_criacao', 'tecnica']


class ExposicaoFilter(django_filters.FilterSet):
    status = django_filters.CharFilter()
    galeria = django_filters.NumberFilter(field_name='galeria_id')

    class Meta:
        model = Exposicao
        fields = ['status', 'galeria']


class IngressoFilter(django_filters.FilterSet):
    status = django_filters.CharFilter()
    tipo = django_filters.CharFilter()
    exposicao = django_filters.NumberFilter(field_name='exposicao_id')

    class Meta:
        model = Ingresso
        fields = ['status', 'tipo', 'exposicao']


class ReservaFilter(django_filters.FilterSet):
    status = django_filters.CharFilter()
    exposicao = django_filters.NumberFilter(field_name='exposicao_id')

    class Meta:
        model = Reserva
        fields = ['status', 'exposicao']


class PagamentoFilter(django_filters.FilterSet):
    status = django_filters.CharFilter()
    metodo = django_filters.CharFilter()

    class Meta:
        model = Pagamento
        fields = ['status', 'metodo']
