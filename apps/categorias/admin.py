from django.contrib import admin

from .models import CategoriaObra


@admin.register(CategoriaObra)
class CategoriaObraAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    search_fields = ('nome', 'descricao')
