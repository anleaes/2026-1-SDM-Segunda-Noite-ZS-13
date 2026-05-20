from django.contrib import admin

from .models import ArtistaObra, CertificadoAutenticidade, ObraArte, Restauracao


@admin.register(ObraArte)
class ObraArteAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'tecnica', 'ano_criacao', 'valor_estimado')
    search_fields = ('titulo', 'tecnica')
    list_filter = ('categoria', 'ano_criacao', 'tecnica')
    autocomplete_fields = ('categoria',)


@admin.register(CertificadoAutenticidade)
class CertificadoAutenticidadeAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'obra', 'data_emissao', 'orgao_responsavel')
    search_fields = ('codigo', 'orgao_responsavel', 'obra__titulo')
    list_filter = ('data_emissao', 'orgao_responsavel')
    autocomplete_fields = ('obra',)


@admin.register(ArtistaObra)
class ArtistaObraAdmin(admin.ModelAdmin):
    list_display = ('artista', 'obra', 'funcao', 'data_participacao')
    search_fields = ('artista__username', 'obra__titulo', 'funcao')
    list_filter = ('funcao', 'data_participacao')
    autocomplete_fields = ('artista', 'obra')


@admin.register(Restauracao)
class RestauracaoAdmin(admin.ModelAdmin):
    list_display = ('obra', 'funcionario', 'data_inicio', 'data_fim', 'custo')
    search_fields = ('obra__titulo', 'funcionario__username', 'descricao')
    list_filter = ('data_inicio', 'data_fim')
    autocomplete_fields = ('obra', 'funcionario')
