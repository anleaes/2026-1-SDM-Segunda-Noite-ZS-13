from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Artista,
    ArtistaObra,
    Avaliacao,
    CategoriaObra,
    CertificadoAutenticidade,
    Exposicao,
    ExposicaoObra,
    Funcionario,
    Galeria,
    Ingresso,
    ObraArte,
    Pagamento,
    Reserva,
    Restauracao,
    Usuario,
    Visitante,
)


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'cpf', 'first_name', 'last_name')
    search_fields = ('username', 'email', 'cpf', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Dados pessoais', {'fields': ('data_nascimento', 'telefone', 'cpf')}),
    )


@admin.register(Funcionario)
class FuncionarioAdmin(UserAdmin):
    list_display = ('username', 'cargo', 'galeria', 'salario', 'data_admissao')
    search_fields = ('username', 'first_name', 'last_name', 'cargo', 'cpf')
    list_filter = ('cargo', 'galeria')
    fieldsets = UserAdmin.fieldsets + (
        ('Dados pessoais', {'fields': ('data_nascimento', 'telefone', 'cpf')}),
        ('Trabalho', {'fields': ('cargo', 'salario', 'data_admissao', 'galeria')}),
    )


@admin.register(Visitante)
class VisitanteAdmin(UserAdmin):
    list_display = ('username', 'email', 'data_cadastro', 'telefone')
    search_fields = ('username', 'email', 'cpf', 'first_name', 'last_name')
    list_filter = ('data_cadastro',)
    fieldsets = UserAdmin.fieldsets + (
        ('Dados pessoais', {'fields': ('data_nascimento', 'telefone', 'cpf', 'data_cadastro')}),
    )
    readonly_fields = ('data_cadastro',)


@admin.register(Artista)
class ArtistaAdmin(UserAdmin):
    list_display = ('username', 'nacionalidade', 'estilo_artistico')
    search_fields = ('username', 'first_name', 'last_name', 'nacionalidade', 'estilo_artistico')
    list_filter = ('nacionalidade', 'estilo_artistico')
    fieldsets = UserAdmin.fieldsets + (
        ('Dados pessoais', {'fields': ('data_nascimento', 'telefone', 'cpf')}),
        ('Perfil artístico', {'fields': ('nacionalidade', 'estilo_artistico')}),
    )


@admin.register(Galeria)
class GaleriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'endereco', 'aberta')
    search_fields = ('nome', 'endereco', 'descricao')
    list_filter = ('aberta',)


@admin.register(CategoriaObra)
class CategoriaObraAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    search_fields = ('nome', 'descricao')


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


@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'valor', 'metodo', 'status', 'data_pagamento', 'tipo_vinculo')
    search_fields = ('id',)
    list_filter = ('metodo', 'status', 'data_pagamento')

    @admin.display(description='Vínculo')
    def tipo_vinculo(self, obj):
        if obj.ingresso_id:
            return f'Ingresso #{obj.ingresso_id}'
        if obj.reserva_id:
            return f'Reserva #{obj.reserva_id}'
        if obj.restauracao_id:
            return f'Restauração #{obj.restauracao_id}'
        return '-'


@admin.register(Ingresso)
class IngressoAdmin(admin.ModelAdmin):
    list_display = ('id', 'visitante', 'exposicao', 'tipo', 'valor', 'status', 'data_compra')
    search_fields = ('visitante__username', 'exposicao__titulo')
    list_filter = ('tipo', 'status', 'data_compra')
    autocomplete_fields = ('visitante', 'exposicao')


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'visitante', 'exposicao', 'data_reserva', 'quantidade_pessoas', 'status')
    search_fields = ('visitante__username', 'exposicao__titulo')
    list_filter = ('status', 'data_reserva')
    autocomplete_fields = ('visitante', 'exposicao')


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('visitante', 'exposicao', 'nota', 'data_avaliacao')
    search_fields = ('visitante__username', 'exposicao__titulo', 'comentario')
    list_filter = ('nota', 'data_avaliacao')
    autocomplete_fields = ('visitante', 'exposicao')
