from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

app_name = 'contas'

auth_urlpatterns = [
    path('login/', views.LoginView.as_view(), name='auth-login'),
    path('register/', views.RegisterView.as_view(), name='auth-register'),
    path('account/<int:pk>/', views.AccountView.as_view(), name='auth-account'),
    path(
        'account/<int:pk>/change-password/',
        views.ChangePasswordView.as_view(),
        name='auth-change-password',
    ),
]

router_usuarios = SimpleRouter()
router_usuarios.register('', views.UsuarioViewSet, basename='usuarios')

router_funcionarios = SimpleRouter()
router_funcionarios.register('', views.FuncionarioViewSet, basename='funcionarios')

router_visitantes = SimpleRouter()
router_visitantes.register('', views.VisitanteViewSet, basename='visitantes')

router_artistas = SimpleRouter()
router_artistas.register('', views.ArtistaViewSet, basename='artistas')

usuarios_urlpatterns = [path('', include(router_usuarios.urls))]
funcionarios_urlpatterns = [path('', include(router_funcionarios.urls))]
visitantes_urlpatterns = [path('', include(router_visitantes.urls))]
artistas_urlpatterns = [path('', include(router_artistas.urls))]
