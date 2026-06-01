"""ViewSets REST do app obras (acervo e restauração)."""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from .filters import ObraArteFilter
from .models import ArtistaObra, CertificadoAutenticidade, ObraArte, Restauracao
from .serializers import (
    ArtistaObraSerializer,
    CertificadoAutenticidadeSerializer,
    ObraArteSerializer,
    RestauracaoSerializer,
)


class ObraArteViewSet(viewsets.ModelViewSet):
    """CRUD de obras de arte com filtros, busca e ordenação."""

    queryset = ObraArte.objects.select_related('categoria')
    serializer_class = ObraArteSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ObraArteFilter
    search_fields = ['titulo', 'tecnica']
    ordering_fields = ['titulo', 'ano_criacao', 'valor_estimado']


class CertificadoAutenticidadeViewSet(viewsets.ModelViewSet):
    """CRUD de certificados de autenticidade."""

    queryset = CertificadoAutenticidade.objects.select_related('obra')
    serializer_class = CertificadoAutenticidadeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['obra']
    search_fields = ['codigo', 'orgao_responsavel', 'obra__titulo']
    ordering_fields = ['data_emissao', 'codigo']


class ArtistaObraViewSet(viewsets.ModelViewSet):
    """CRUD de vínculos entre artistas e obras."""

    queryset = ArtistaObra.objects.select_related('artista', 'obra')
    serializer_class = ArtistaObraSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['artista', 'obra', 'funcao']
    search_fields = ['artista__username', 'obra__titulo', 'funcao']
    ordering_fields = ['data_participacao']


class RestauracaoViewSet(viewsets.ModelViewSet):
    """CRUD de registros de restauração."""

    queryset = Restauracao.objects.select_related('obra', 'funcionario')
    serializer_class = RestauracaoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['obra', 'funcionario']
    search_fields = ['obra__titulo', 'funcionario__username', 'descricao']
    ordering_fields = ['data_inicio', 'data_fim', 'custo']
