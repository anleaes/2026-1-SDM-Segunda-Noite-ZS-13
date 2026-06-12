from django.db.models.deletion import ProtectedError
from rest_framework import status, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from .models import CategoriaObra
from .serializers import CategoriaObraSerializer


class CategoriaObraViewSet(viewsets.ModelViewSet):
    queryset = CategoriaObra.objects.all()
    serializer_class = CategoriaObraSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['nome', 'descricao']
    ordering_fields = ['nome']

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {
                    'detail': (
                        'Nao e possivel excluir: existem obras vinculadas a esta categoria.'
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
