import django_filters

from .models import Exposicao


class ExposicaoFilter(django_filters.FilterSet):
    status = django_filters.CharFilter()
    galeria = django_filters.NumberFilter(field_name='galeria_id')

    class Meta:
        model = Exposicao
        fields = ['status', 'galeria']
