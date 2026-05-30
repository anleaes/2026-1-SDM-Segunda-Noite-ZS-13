import django_filters

from .models import ObraArte


class ObraArteFilter(django_filters.FilterSet):
    categoria = django_filters.NumberFilter(field_name='categoria_id')
    ano_criacao = django_filters.NumberFilter()

    class Meta:
        model = ObraArte
        fields = ['categoria', 'ano_criacao', 'tecnica']
