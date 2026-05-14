from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView

from contas import urls as contas_urls
from exposicoes import urls as exposicoes_urls
from obras import urls as obras_urls
from visitacao import urls as visitacao_urls

admin.site.site_header = 'Museu & Galeria'
admin.site.site_title = 'Museu & Galeria'
admin.site.index_title = 'Administração'
admin.site.site_url = settings.FRONTEND_URL

urlpatterns = [
    path('', RedirectView.as_view(url=settings.FRONTEND_URL, permanent=False)),
    path('admin/', admin.site.urls),
    path('api/auth/', include(contas_urls.auth_urlpatterns)),
    path('api/usuarios/', include(contas_urls.usuarios_urlpatterns)),
    path('api/funcionarios/', include(contas_urls.funcionarios_urlpatterns)),
    path('api/visitantes/', include(contas_urls.visitantes_urlpatterns)),
    path('api/artistas/', include(contas_urls.artistas_urlpatterns)),
    path('api/galerias/', include('galerias.urls')),
    path('api/categorias-obra/', include('categorias.urls')),
    path('api/obras/', include(obras_urls.urlpatterns)),
    path('api/certificados/', include(obras_urls.certificados_urlpatterns)),
    path('api/artista-obras/', include(obras_urls.artista_obras_urlpatterns)),
    path('api/restauracoes/', include(obras_urls.restauracoes_urlpatterns)),
    path('api/exposicoes/', include(exposicoes_urls.urlpatterns)),
    path('api/exposicao-obras/', include(exposicoes_urls.exposicao_obras_urlpatterns)),
    path('api/ingressos/', include(visitacao_urls.ingressos_urlpatterns)),
    path('api/reservas/', include(visitacao_urls.reservas_urlpatterns)),
    path('api/avaliacoes/', include(visitacao_urls.avaliacoes_urlpatterns)),
    path('api/pagamentos/', include(visitacao_urls.pagamentos_urlpatterns)),
]
