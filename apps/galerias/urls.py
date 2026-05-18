from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

app_name = 'galerias'

router = SimpleRouter()
router.register('', views.GaleriaViewSet, basename='galerias')

urlpatterns = [
    path('', include(router.urls)),
]
