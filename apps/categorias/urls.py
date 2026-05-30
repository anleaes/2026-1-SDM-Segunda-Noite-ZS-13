from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

app_name = 'categorias'

router = SimpleRouter()
router.register('', views.CategoriaObraViewSet, basename='categorias-obra')

urlpatterns = [
    path('', include(router.urls)),
]
