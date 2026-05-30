import django_filters

from .models import Galeria


class GaleriaFilter(django_filters.FilterSet):
    aberta = django_filters.BooleanFilter()

    class Meta:
        model = Galeria
        fields = ['aberta']
