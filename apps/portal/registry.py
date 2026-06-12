from categorias.models import CategoriaObra
from contas.models import Artista, Funcionario, Usuario, Visitante
from exposicoes.models import Exposicao, ExposicaoObra
from galerias.models import Galeria
from obras.models import ArtistaObra, CertificadoAutenticidade, ObraArte, Restauracao
from visitacao.models import Avaliacao, Ingresso, Pagamento, Reserva


def _section(
    slug,
    title,
    model,
    api_path,
    list_fields,
    allow_crud=True,
    form_exclude=None,
):
    return {
        'slug': slug,
        'title': title,
        'title_plural': title + 's' if not title.endswith('ão') else title.replace('ão', 'ões'),
        'model': model,
        'model_name': model.__name__,
        'db_table': model._meta.db_table,
        'api_path': api_path,
        'list_fields': list_fields,
        'allow_crud': allow_crud,
        'form_exclude': form_exclude or [],
    }


SECTIONS = [
    _section('galerias', 'Galeria', Galeria, '/api/galerias/', ['id', 'nome', 'endereco', 'aberta']),
    _section(
        'categorias',
        'Categoria de Obra',
        CategoriaObra,
        '/api/categorias-obra/',
        ['id', 'nome', 'descricao'],
    ),
    _section(
        'obras',
        'Obra de Arte',
        ObraArte,
        '/api/obras/',
        ['id', 'titulo', 'tecnica', 'ano_criacao', 'categoria'],
    ),
    _section(
        'certificados',
        'Certificado',
        CertificadoAutenticidade,
        '/api/certificados/',
        ['id', 'codigo', 'obra', 'data_emissao'],
    ),
    _section(
        'artista-obras',
        'Participação Artista/Obra',
        ArtistaObra,
        '/api/artista-obras/',
        ['id', 'artista', 'obra', 'funcao'],
    ),
    _section(
        'restauracoes',
        'Restauração',
        Restauracao,
        '/api/restauracoes/',
        ['id', 'obra', 'funcionario', 'data_inicio', 'custo'],
    ),
    _section(
        'exposicoes',
        'Exposição',
        Exposicao,
        '/api/exposicoes/',
        ['id', 'titulo', 'galeria', 'status', 'data_inicio', 'data_fim'],
    ),
    _section(
        'exposicao-obras',
        'Obra na Exposição',
        ExposicaoObra,
        '/api/exposicao-obras/',
        ['id', 'exposicao', 'obra', 'posicao_sala'],
    ),
    _section(
        'usuarios',
        'Usuário',
        Usuario,
        '/api/usuarios/',
        ['id', 'username', 'email', 'cpf', 'is_active'],
        allow_crud=False,
    ),
    _section(
        'funcionarios',
        'Funcionário',
        Funcionario,
        '/api/funcionarios/',
        ['id', 'username', 'cargo', 'galeria'],
        allow_crud=False,
    ),
    _section(
        'visitantes',
        'Visitante',
        Visitante,
        '/api/visitantes/',
        ['id', 'username', 'email', 'data_cadastro'],
        allow_crud=False,
    ),
    _section(
        'artistas',
        'Artista',
        Artista,
        '/api/artistas/',
        ['id', 'username', 'nacionalidade', 'estilo_artistico'],
        allow_crud=False,
    ),
    _section(
        'ingressos',
        'Ingresso',
        Ingresso,
        '/api/ingressos/',
        ['id', 'visitante', 'exposicao', 'tipo', 'valor', 'status'],
    ),
    _section(
        'reservas',
        'Reserva',
        Reserva,
        '/api/reservas/',
        ['id', 'visitante', 'exposicao', 'data_reserva', 'status'],
    ),
    _section(
        'avaliacoes',
        'Avaliação',
        Avaliacao,
        '/api/avaliacoes/',
        ['id', 'visitante', 'exposicao', 'nota', 'data_avaliacao'],
    ),
    _section(
        'pagamentos',
        'Pagamento',
        Pagamento,
        '/api/pagamentos/',
        ['id', 'valor', 'metodo', 'status', 'data_pagamento'],
        allow_crud=False,
    ),
]

SECTIONS_BY_SLUG = {s['slug']: s for s in SECTIONS}


def get_section(slug):
    return SECTIONS_BY_SLUG.get(slug)
