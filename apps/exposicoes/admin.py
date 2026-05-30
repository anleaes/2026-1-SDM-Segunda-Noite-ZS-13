from django.contrib import admin

from .models import Exposicao, ExposicaoObra


@admin.register(Exposicao)
class ExposicaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'galeria', 'status', 'data_inicio', 'data_fim')
    search_fields = ('titulo', 'descricao', 'galeria__nome')
    list_filter = ('status', 'galeria', 'data_inicio')
    autocomplete_fields = ('galeria',)


@admin.register(ExposicaoObra)
class ExposicaoObraAdmin(admin.ModelAdmin):
    list_display = ('exposicao', 'obra', 'posicao_sala', 'status_conservacao', 'data_entrada')
    search_fields = ('exposicao__titulo', 'obra__titulo', 'posicao_sala')
    list_filter = ('status_conservacao', 'data_entrada')
    autocomplete_fields = ('exposicao', 'obra')
