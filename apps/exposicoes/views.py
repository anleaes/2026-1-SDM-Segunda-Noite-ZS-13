from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from .filters import ExposicaoFilter
from .models import Exposicao, ExposicaoObra
from .serializers import ExposicaoObraSerializer, ExposicaoSerializer


class ExposicaoViewSet(viewsets.ModelViewSet):
    queryset = Exposicao.objects.select_related('galeria')
    serializer_class = ExposicaoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ExposicaoFilter
    search_fields = ['titulo', 'descricao', 'galeria__nome']
    ordering_fields = ['titulo', 'data_inicio', 'data_fim', 'status']


class ExposicaoObraViewSet(viewsets.ModelViewSet):
    queryset = ExposicaoObra.objects.select_related('exposicao', 'obra')
    serializer_class = ExposicaoObraSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['exposicao', 'obra', 'status_conservacao']
    search_fields = ['exposicao__titulo', 'obra__titulo', 'posicao_sala']
    ordering_fields = ['data_entrada']
