from django.contrib import admin

from .models import Avaliacao, Ingresso, Pagamento, Reserva


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
