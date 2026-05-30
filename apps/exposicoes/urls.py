from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

app_name = 'exposicoes'

router_exposicoes = SimpleRouter()
router_exposicoes.register('', views.ExposicaoViewSet, basename='exposicoes')

router_exposicao_obras = SimpleRouter()
router_exposicao_obras.register('', views.ExposicaoObraViewSet, basename='exposicao-obras')

urlpatterns = [
    path('', include(router_exposicoes.urls)),
]

exposicao_obras_urlpatterns = [
    path('', include(router_exposicao_obras.urls)),
]
