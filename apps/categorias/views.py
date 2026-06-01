"""ViewSets REST do app categorias."""

from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import CategoriaObra
from .serializers import CategoriaObraSerializer


class CategoriaObraViewSet(viewsets.ModelViewSet):
    """CRUD de categorias de obra."""

    queryset = CategoriaObra.objects.all()
    serializer_class = CategoriaObraSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome']
