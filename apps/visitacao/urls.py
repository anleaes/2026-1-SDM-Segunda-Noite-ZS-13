from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

app_name = 'visitacao'

router_ingressos = SimpleRouter()
router_ingressos.register('', views.IngressoViewSet, basename='ingressos')

router_reservas = SimpleRouter()
router_reservas.register('', views.ReservaViewSet, basename='reservas')

router_avaliacoes = SimpleRouter()
router_avaliacoes.register('', views.AvaliacaoViewSet, basename='avaliacoes')

router_pagamentos = SimpleRouter()
router_pagamentos.register('', views.PagamentoViewSet, basename='pagamentos')

ingressos_urlpatterns = [path('', include(router_ingressos.urls))]
reservas_urlpatterns = [path('', include(router_reservas.urls))]
avaliacoes_urlpatterns = [path('', include(router_avaliacoes.urls))]
pagamentos_urlpatterns = [path('', include(router_pagamentos.urls))]
