from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from .filters import GaleriaFilter
from .models import Galeria
from .serializers import GaleriaSerializer


class GaleriaViewSet(viewsets.ModelViewSet):
    queryset = Galeria.objects.all()
    serializer_class = GaleriaSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = GaleriaFilter
    search_fields = ['nome', 'endereco', 'descricao']
    ordering_fields = ['nome']
