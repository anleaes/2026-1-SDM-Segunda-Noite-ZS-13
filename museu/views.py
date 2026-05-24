from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import viewsets

from .filters import (
    ExposicaoFilter,
    GaleriaFilter,
    IngressoFilter,
    ObraArteFilter,
    PagamentoFilter,
    ReservaFilter,
)
from .models import (
    Artista,
    ArtistaObra,
    Avaliacao,
    CategoriaObra,
    CertificadoAutenticidade,
    Exposicao,
    ExposicaoObra,
    Funcionario,
    Galeria,
    Ingresso,
    ObraArte,
    Pagamento,
    Reserva,
    Restauracao,
    Usuario,
    Visitante,
)
from .serializers import (
    ArtistaObraSerializer,
    ArtistaSerializer,
    AvaliacaoSerializer,
    CategoriaObraSerializer,
    CertificadoAutenticidadeSerializer,
    ExposicaoObraSerializer,
    ExposicaoSerializer,
    FuncionarioSerializer,
    GaleriaSerializer,
    IngressoSerializer,
    ObraArteSerializer,
    PagamentoSerializer,
    ReservaSerializer,
    RestauracaoSerializer,
    UsuarioSerializer,
    VisitanteSerializer,
)


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username', 'email', 'cpf', 'first_name', 'last_name']
    ordering_fields = ['username', 'email']


class FuncionarioViewSet(viewsets.ModelViewSet):
    queryset = Funcionario.objects.select_related('galeria')
    serializer_class = FuncionarioSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['cargo', 'galeria']
    search_fields = ['username', 'first_name', 'last_name', 'cargo']
    ordering_fields = ['username', 'data_admissao', 'salario']


class VisitanteViewSet(viewsets.ModelViewSet):
    queryset = Visitante.objects.all()
    serializer_class = VisitanteSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username', 'email', 'cpf', 'first_name', 'last_name']
    ordering_fields = ['username', 'data_cadastro']


class ArtistaViewSet(viewsets.ModelViewSet):
    queryset = Artista.objects.all()
    serializer_class = ArtistaSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['nacionalidade', 'estilo_artistico']
    search_fields = ['username', 'first_name', 'last_name', 'nacionalidade']
    ordering_fields = ['username', 'nacionalidade']


class GaleriaViewSet(viewsets.ModelViewSet):
    queryset = Galeria.objects.all()
    serializer_class = GaleriaSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = GaleriaFilter
    search_fields = ['nome', 'endereco', 'descricao']
    ordering_fields = ['nome']


class CategoriaObraViewSet(viewsets.ModelViewSet):
    queryset = CategoriaObra.objects.all()
    serializer_class = CategoriaObraSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome']


class ObraArteViewSet(viewsets.ModelViewSet):
    queryset = ObraArte.objects.select_related('categoria')
    serializer_class = ObraArteSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ObraArteFilter
    search_fields = ['titulo', 'tecnica']
    ordering_fields = ['titulo', 'ano_criacao', 'valor_estimado']


class CertificadoAutenticidadeViewSet(viewsets.ModelViewSet):
    queryset = CertificadoAutenticidade.objects.select_related('obra')
    serializer_class = CertificadoAutenticidadeSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['codigo', 'orgao_responsavel', 'obra__titulo']
    ordering_fields = ['data_emissao', 'codigo']


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


class ArtistaObraViewSet(viewsets.ModelViewSet):
    queryset = ArtistaObra.objects.select_related('artista', 'obra')
    serializer_class = ArtistaObraSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['artista', 'obra', 'funcao']
    search_fields = ['artista__username', 'obra__titulo', 'funcao']
    ordering_fields = ['data_participacao']


class RestauracaoViewSet(viewsets.ModelViewSet):
    queryset = Restauracao.objects.select_related('obra', 'funcionario')
    serializer_class = RestauracaoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['obra', 'funcionario']
    search_fields = ['obra__titulo', 'funcionario__username', 'descricao']
    ordering_fields = ['data_inicio', 'data_fim', 'custo']


class PagamentoViewSet(viewsets.ModelViewSet):
    queryset = Pagamento.objects.select_related('ingresso', 'reserva', 'restauracao')
    serializer_class = PagamentoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PagamentoFilter
    ordering_fields = ['data_pagamento', 'valor', 'status']


class IngressoViewSet(viewsets.ModelViewSet):
    queryset = Ingresso.objects.select_related('visitante', 'exposicao')
    serializer_class = IngressoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = IngressoFilter
    search_fields = ['visitante__username', 'exposicao__titulo']
    ordering_fields = ['data_compra', 'valor']


class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.select_related('visitante', 'exposicao')
    serializer_class = ReservaSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ReservaFilter
    search_fields = ['visitante__username', 'exposicao__titulo']
    ordering_fields = ['data_reserva', 'quantidade_pessoas']


class AvaliacaoViewSet(viewsets.ModelViewSet):
    queryset = Avaliacao.objects.select_related('visitante', 'exposicao')
    serializer_class = AvaliacaoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['exposicao', 'visitante', 'nota']
    search_fields = ['visitante__username', 'exposicao__titulo', 'comentario']
    ordering_fields = ['data_avaliacao', 'nota']
