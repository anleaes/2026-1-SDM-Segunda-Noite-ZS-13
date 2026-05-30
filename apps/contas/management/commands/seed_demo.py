from datetime import date

from django.core.management.base import BaseCommand
from django.db import transaction

from contas.models import Artista, Funcionario, Usuario, Visitante
from categorias.models import CategoriaObra
from exposicoes.models import Exposicao, ExposicaoObra
from galerias.models import Galeria
from obras.models import (
    ArtistaObra,
    CertificadoAutenticidade,
    ObraArte,
    Restauracao,
)
from visitacao.models import Avaliacao, Ingresso, Pagamento, Reserva


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
        obra_nathan = self._criar_obra_nathan(categoria)
        self._criar_certificado_nathan(obra_nathan)
        exposicao_nathan = self._criar_exposicao_nathan(galeria)
        self._criar_exposicao_obra(
            exposicao_nathan,
            obra_nathan,
            data_entrada=date(2026, 7, 25),
            posicao_sala='Sala 1 - Entrada principal',
            iluminacao_especial='Spot LED regulavel',
            status_conservacao='Otimo',
            estilo_obra='Arte Contemporanea',
        )
        self._criar_artista_obra(artista, obra_nathan)
        ingresso = self._criar_ingresso(visitante, exposicao_nathan)
        reserva = self._criar_reserva(visitante, exposicao_nathan)
        self._criar_pagamentos(ingresso, reserva)
        self._criar_restauracao(obra_nathan, funcionario)
        self._criar_avaliacao(visitante, exposicao_nathan)

        self.stdout.write(self.style.SUCCESS('Dados de demonstracao criados com sucesso!'))
        self.stdout.write('')
        self.stdout.write('Usuarios de teste (senha: demo123):')
        self.stdout.write('  nathan.funcionario  - curador no MASP')
        self.stdout.write('  nathan.visitante    - compra ingresso e reserva')
        self.stdout.write('  nathan.artista      - autor da obra Composicao em Azul')
        self.stdout.write('  admin / admin123      - superusuario do Django Admin')

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

    def _criar_exposicao_obra(self, exposicao, obra, **extra_defaults):
        defaults = {
            'data_entrada': date(2026, 5, 28),
            'posicao_sala': 'Sala 3 - Parede central',
            'iluminacao_especial': 'Luz indireta com filtro UV',
            'status_conservacao': 'Excelente',
            'estilo_obra': 'Modernismo',
        }
        defaults.update(extra_defaults)
        ExposicaoObra.objects.get_or_create(
            exposicao=exposicao,
            obra=obra,
            defaults=defaults,
        )

    def _criar_funcionario(self, galeria):
        if Funcionario.objects.filter(username='nathan.funcionario').exists():
            return Funcionario.objects.get(username='nathan.funcionario')

        funcionario = Funcionario(
            username='nathan.funcionario',
            email='nathan.funcionario@museu.com',
            cpf='44444444444',
            first_name='Nathan',
            last_name='Neemias',
            telefone='(11) 98888-4444',
            data_nascimento=date(2000, 1, 15),
            cargo='Curador',
            salario=8500.00,
            data_admissao=date(2024, 3, 1),
            galeria=galeria,
        )
        funcionario.set_password('demo123')
        funcionario.save()
        return funcionario

    def _criar_visitante(self):
        if Visitante.objects.filter(username='nathan.visitante').exists():
            return Visitante.objects.get(username='nathan.visitante')

        visitante = Visitante(
            username='nathan.visitante',
            email='nathan.visitante@email.com',
            cpf='55555555555',
            first_name='Nathan',
            last_name='Neemias',
            telefone='(11) 97777-5555',
            data_nascimento=date(2000, 1, 15),
        )
        visitante.set_password('demo123')
        visitante.save()
        return visitante

    def _criar_artista(self):
        if Artista.objects.filter(username='nathan.artista').exists():
            return Artista.objects.get(username='nathan.artista')

        artista = Artista(
            username='nathan.artista',
            email='nathan.artista@arte.com',
            cpf='66666666666',
            first_name='Nathan',
            last_name='Neemias',
            telefone='(11) 96666-6666',
            data_nascimento=date(2000, 1, 15),
            nacionalidade='Brasileira',
            estilo_artistico='Arte Contemporanea',
        )
        artista.set_password('demo123')
        artista.save()
        return artista

    def _criar_obra_nathan(self, categoria):
        obra, _ = ObraArte.objects.get_or_create(
            titulo='Composicao em Azul',
            defaults={
                'tecnica': 'Acrilica sobre tela',
                'ano_criacao': 2024,
                'valor_estimado': 25000.00,
                'categoria': categoria,
            },
        )
        return obra

    def _criar_certificado_nathan(self, obra):
        CertificadoAutenticidade.objects.get_or_create(
            codigo='CERT-NATHAN-001',
            defaults={
                'obra': obra,
                'data_emissao': date(2025, 11, 10),
                'orgao_responsavel': 'Galeria MASP - Setor de Autenticacao',
            },
        )

    def _criar_exposicao_nathan(self, galeria):
        exposicao, _ = Exposicao.objects.get_or_create(
            titulo='Novos Olhares Contemporaneos',
            defaults={
                'descricao': 'Mostra com obras de artistas emergentes, incluindo Nathan Neemias.',
                'data_inicio': date(2026, 8, 1),
                'data_fim': date(2026, 10, 31),
                'status': 'planejada',
                'galeria': galeria,
            },
        )
        return exposicao

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
                'comentario': 'Obra Composicao em Azul ficou incrivel na exposicao!',
            },
        )
