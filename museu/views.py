from rest_framework import viewsets

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


class FuncionarioViewSet(viewsets.ModelViewSet):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer


class VisitanteViewSet(viewsets.ModelViewSet):
    queryset = Visitante.objects.all()
    serializer_class = VisitanteSerializer


class ArtistaViewSet(viewsets.ModelViewSet):
    queryset = Artista.objects.all()
    serializer_class = ArtistaSerializer


class GaleriaViewSet(viewsets.ModelViewSet):
    queryset = Galeria.objects.all()
    serializer_class = GaleriaSerializer


class CategoriaObraViewSet(viewsets.ModelViewSet):
    queryset = CategoriaObra.objects.all()
    serializer_class = CategoriaObraSerializer


class ObraArteViewSet(viewsets.ModelViewSet):
    queryset = ObraArte.objects.all()
    serializer_class = ObraArteSerializer


class CertificadoAutenticidadeViewSet(viewsets.ModelViewSet):
    queryset = CertificadoAutenticidade.objects.all()
    serializer_class = CertificadoAutenticidadeSerializer


class ExposicaoViewSet(viewsets.ModelViewSet):
    queryset = Exposicao.objects.all()
    serializer_class = ExposicaoSerializer


class ExposicaoObraViewSet(viewsets.ModelViewSet):
    queryset = ExposicaoObra.objects.all()
    serializer_class = ExposicaoObraSerializer


class ArtistaObraViewSet(viewsets.ModelViewSet):
    queryset = ArtistaObra.objects.all()
    serializer_class = ArtistaObraSerializer


class RestauracaoViewSet(viewsets.ModelViewSet):
    queryset = Restauracao.objects.all()
    serializer_class = RestauracaoSerializer


class PagamentoViewSet(viewsets.ModelViewSet):
    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer


class IngressoViewSet(viewsets.ModelViewSet):
    queryset = Ingresso.objects.all()
    serializer_class = IngressoSerializer


class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer


class AvaliacaoViewSet(viewsets.ModelViewSet):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer
