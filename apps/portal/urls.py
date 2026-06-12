from django.urls import path

from . import views

app_name = 'portal'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('arquitetura/', views.ArquiteturaView.as_view(), name='arquitetura'),
    path('<slug:slug>/', views.ModelListView.as_view(), name='list'),
    path('<slug:slug>/novo/', views.ModelCreateView.as_view(), name='create'),
    path('<slug:slug>/<int:pk>/', views.ModelDetailView.as_view(), name='detail'),
    path('<slug:slug>/<int:pk>/editar/', views.ModelUpdateView.as_view(), name='edit'),
    path('<slug:slug>/<int:pk>/excluir/', views.ModelDeleteView.as_view(), name='delete'),
]
