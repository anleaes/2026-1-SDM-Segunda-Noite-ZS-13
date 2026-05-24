from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('usuarios', views.UsuarioViewSet)
router.register('funcionarios', views.FuncionarioViewSet)
router.register('visitantes', views.VisitanteViewSet)
router.register('artistas', views.ArtistaViewSet)
router.register('galerias', views.GaleriaViewSet)
router.register('categorias-obra', views.CategoriaObraViewSet)
router.register('obras', views.ObraArteViewSet)
router.register('certificados', views.CertificadoAutenticidadeViewSet)
router.register('exposicoes', views.ExposicaoViewSet)
router.register('exposicao-obras', views.ExposicaoObraViewSet)
router.register('artista-obras', views.ArtistaObraViewSet)
router.register('restauracoes', views.RestauracaoViewSet)
router.register('pagamentos', views.PagamentoViewSet)
router.register('ingressos', views.IngressoViewSet)
router.register('reservas', views.ReservaViewSet)
router.register('avaliacoes', views.AvaliacaoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
