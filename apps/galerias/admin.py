from django.contrib import admin

from .models import Galeria


@admin.register(Galeria)
class GaleriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'endereco', 'aberta')
    search_fields = ('nome', 'endereco', 'descricao')
    list_filter = ('aberta',)
