from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Artista, Funcionario, Usuario, Visitante


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
