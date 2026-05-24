from datetime import date

from django.core.management.base import BaseCommand
from django.db import transaction

from museu.models import (
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


class Command(BaseCommand):
    help = 'Popula o banco com dados de demonstracao do sistema de museus.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Apaga dados de demo antes de recriar (nao remove superusuario).',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options['reset']:
            self._limpar_dados()

        self._criar_superusuario()
        galeria = self._criar_galerias()
        categoria = self._criar_categorias()
        obra = self._criar_obras(categoria)
        self._criar_certificado(obra)
        exposicao = self._criar_exposicoes(galeria)
        self._criar_exposicao_obra(exposicao, obra)
        funcionario = self._criar_funcionario(galeria)
        visitante = self._criar_visitante()
        artista = self._criar_artista()
        self._criar_artista_obra(artista, obra)
        ingresso = self._criar_ingresso(visitante, exposicao)
        reserva = self._criar_reserva(visitante, exposicao)
        self._criar_pagamentos(ingresso, reserva)
        self._criar_restauracao(obra, funcionario)
        self._criar_avaliacao(visitante, exposicao)

        self.stdout.write(self.style.SUCCESS('Dados de demonstracao criados com sucesso!'))

    def _limpar_dados(self):
        Avaliacao.objects.all().delete()
        Pagamento.objects.all().delete()
        Ingresso.objects.all().delete()
        Reserva.objects.all().delete()
        Restauracao.objects.all().delete()
        ArtistaObra.objects.all().delete()
        ExposicaoObra.objects.all().delete()
        CertificadoAutenticidade.objects.all().delete()
        Exposicao.objects.all().delete()
        ObraArte.objects.all().delete()
        CategoriaObra.objects.all().delete()
        Galeria.objects.all().delete()
        Usuario.objects.filter(is_superuser=False).delete()
        self.stdout.write('Dados de demo removidos.')

    def _criar_superusuario(self):
        if Usuario.objects.filter(username='admin').exists():
            self.stdout.write('Superusuario admin ja existe.')
            return

        Usuario.objects.create_superuser(
            username='admin',
            email='admin@museu.com',
            password='admin123',
            cpf='00000000000',
            first_name='Admin',
            last_name='Sistema',
        )
        self.stdout.write(self.style.SUCCESS('Superusuario criado: admin / admin123'))

    def _criar_galerias(self):
        galeria, _ = Galeria.objects.get_or_create(
            nome='MASP',
            defaults={
                'descricao': 'Museu de Arte de Sao Paulo Assis Chateaubriand',
                'endereco': 'Av. Paulista, 1578 - Bela Vista, Sao Paulo',
                'aberta': True,
            },
        )
        Galeria.objects.get_or_create(
            nome='Pinacoteca',
            defaults={
                'descricao': 'Pinacoteca do Estado de Sao Paulo',
                'endereco': 'Praça da Luz, 2 - Luz, Sao Paulo',
                'aberta': True,
            },
        )
        return galeria

    def _criar_categorias(self):
        categoria, _ = CategoriaObra.objects.get_or_create(
            nome='Pintura',
            defaults={'descricao': 'Obras produzidas com tinta sobre tela ou madeira.'},
        )
        CategoriaObra.objects.get_or_create(
            nome='Escultura',
            defaults={'descricao': 'Obras tridimensionais em diversos materiais.'},
        )
        return categoria

    def _criar_obras(self, categoria):
        obra, _ = ObraArte.objects.get_or_create(
            titulo='Abaporu',
            defaults={
                'tecnica': 'Oleo sobre tela',
                'ano_criacao': 1928,
                'valor_estimado': 15000000.00,
                'categoria': categoria,
            },
        )
        ObraArte.objects.get_or_create(
            titulo='O Lavrador de Cafe',
            defaults={
                'tecnica': 'Oleo sobre tela',
                'ano_criacao': 1939,
                'valor_estimado': 8000000.00,
                'categoria': categoria,
            },
        )
        return obra

    def _criar_certificado(self, obra):
        CertificadoAutenticidade.objects.get_or_create(
            codigo='CERT-ABAPORU-001',
            defaults={
                'obra': obra,
                'data_emissao': date(2020, 3, 15),
                'orgao_responsavel': 'Instituto Tarsila do Amaral',
            },
        )

    def _criar_exposicoes(self, galeria):
        exposicao, _ = Exposicao.objects.get_or_create(
            titulo='Modernismo Brasileiro',
            defaults={
                'descricao': 'Mostra com obras centrais do modernismo no Brasil.',
                'data_inicio': date(2026, 6, 1),
                'data_fim': date(2026, 9, 30),
                'status': 'planejada',
                'galeria': galeria,
            },
        )
        Exposicao.objects.get_or_create(
            titulo='Arte Contemporanea',
            defaults={
                'descricao': 'Exposicao temporaria de artistas contemporaneos.',
                'data_inicio': date(2026, 10, 1),
                'data_fim': date(2026, 12, 15),
                'status': 'planejada',
                'galeria': galeria,
            },
        )
        return exposicao

    def _criar_exposicao_obra(self, exposicao, obra):
        ExposicaoObra.objects.get_or_create(
            exposicao=exposicao,
            obra=obra,
            defaults={
                'data_entrada': date(2026, 5, 28),
                'posicao_sala': 'Sala 3 - Parede central',
                'iluminacao_especial': 'Luz indireta com filtro UV',
                'status_conservacao': 'Excelente',
                'estilo_obra': 'Modernismo',
            },
        )

    def _criar_funcionario(self, galeria):
        if Funcionario.objects.filter(username='joao.curador').exists():
            return Funcionario.objects.get(username='joao.curador')

        funcionario = Funcionario(
            username='joao.curador',
            email='joao.curador@museu.com',
            cpf='11111111111',
            first_name='Joao',
            last_name='Silva',
            telefone='(11) 98888-0001',
            data_nascimento=date(1985, 4, 12),
            cargo='Curador',
            salario=8500.00,
            data_admissao=date(2018, 2, 1),
            galeria=galeria,
        )
        funcionario.set_password('demo123')
        funcionario.save()
        return funcionario

    def _criar_visitante(self):
        if Visitante.objects.filter(username='maria.visitante').exists():
            return Visitante.objects.get(username='maria.visitante')

        visitante = Visitante(
            username='maria.visitante',
            email='maria@email.com',
            cpf='22222222222',
            first_name='Maria',
            last_name='Oliveira',
            telefone='(11) 97777-0002',
            data_nascimento=date(1995, 8, 20),
        )
        visitante.set_password('demo123')
        visitante.save()
        return visitante

    def _criar_artista(self):
        if Artista.objects.filter(username='tarsila.artista').exists():
            return Artista.objects.get(username='tarsila.artista')

        artista = Artista(
            username='tarsila.artista',
            email='tarsila@arte.com',
            cpf='33333333333',
            first_name='Tarsila',
            last_name='Amaral',
            telefone='(11) 96666-0003',
            data_nascimento=date(1886, 9, 1),
            nacionalidade='Brasileira',
            estilo_artistico='Modernismo',
        )
        artista.set_password('demo123')
        artista.save()
        return artista

    def _criar_artista_obra(self, artista, obra):
        ArtistaObra.objects.get_or_create(
            artista=artista,
            obra=obra,
            defaults={
                'funcao': 'Autora',
                'data_participacao': date(1928, 1, 1),
            },
        )

    def _criar_ingresso(self, visitante, exposicao):
        ingresso, _ = Ingresso.objects.get_or_create(
            visitante=visitante,
            exposicao=exposicao,
            tipo='inteira',
            defaults={
                'valor': 60.00,
                'status': 'ativo',
            },
        )
        return ingresso

    def _criar_reserva(self, visitante, exposicao):
        reserva, _ = Reserva.objects.get_or_create(
            visitante=visitante,
            exposicao=exposicao,
            data_reserva=date(2026, 7, 10),
            defaults={
                'quantidade_pessoas': 4,
                'status': 'confirmada',
            },
        )
        return reserva

    def _criar_pagamentos(self, ingresso, reserva):
        Pagamento.objects.get_or_create(
            ingresso=ingresso,
            defaults={
                'valor': 60.00,
                'metodo': 'pix',
                'status': 'pago',
            },
        )
        Pagamento.objects.get_or_create(
            reserva=reserva,
            defaults={
                'valor': 120.00,
                'metodo': 'cartao',
                'status': 'pago',
            },
        )

    def _criar_restauracao(self, obra, funcionario):
        Restauracao.objects.get_or_create(
            obra=obra,
            funcionario=funcionario,
            data_inicio=date(2026, 4, 1),
            defaults={
                'data_fim': date(2026, 4, 20),
                'descricao': 'Limpeza superficial e consolidacao da camada pictorica.',
                'custo': 3500.00,
            },
        )

    def _criar_avaliacao(self, visitante, exposicao):
        Avaliacao.objects.get_or_create(
            visitante=visitante,
            exposicao=exposicao,
            defaults={
                'nota': 5,
                'comentario': 'Exposicao incrivel, organizacao impecavel!',
            },
        )
