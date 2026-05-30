from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from .filters import IngressoFilter, PagamentoFilter, ReservaFilter
from .models import Avaliacao, Ingresso, Pagamento, Reserva
from .serializers import (
    AvaliacaoSerializer,
    IngressoSerializer,
    PagamentoSerializer,
    ReservaSerializer,
)


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


class PagamentoViewSet(viewsets.ModelViewSet):
    queryset = Pagamento.objects.select_related('ingresso', 'reserva', 'restauracao')
    serializer_class = PagamentoSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PagamentoFilter
    ordering_fields = ['data_pagamento', 'valor', 'status']
