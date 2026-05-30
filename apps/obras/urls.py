from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

app_name = 'obras'

router_obras = SimpleRouter()
router_obras.register('', views.ObraArteViewSet, basename='obras')

router_certificados = SimpleRouter()
router_certificados.register('', views.CertificadoAutenticidadeViewSet, basename='certificados')

router_artista_obras = SimpleRouter()
router_artista_obras.register('', views.ArtistaObraViewSet, basename='artista-obras')

router_restauracoes = SimpleRouter()
router_restauracoes.register('', views.RestauracaoViewSet, basename='restauracoes')

urlpatterns = [
    path('', include(router_obras.urls)),
]

certificados_urlpatterns = [
    path('', include(router_certificados.urls)),
]

artista_obras_urlpatterns = [
    path('', include(router_artista_obras.urls)),
]

restauracoes_urlpatterns = [
    path('', include(router_restauracoes.urls)),
]
