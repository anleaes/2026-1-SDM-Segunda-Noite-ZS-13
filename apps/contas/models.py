from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Usuario(AbstractUser):
    data_nascimento = models.DateField(null=True, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    cpf = models.CharField(max_length=14, unique=True)

    class Meta:
        db_table = 'museu_usuario'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def cadastrar_usuario(self):
        self.save()

    def atualizar_usuario(self, **dados):
        for campo, valor in dados.items():
            setattr(self, campo, valor)
        self.save()

    def excluir_usuario(self):
        self.delete()


class Funcionario(Usuario):
    cargo = models.CharField(max_length=100)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    data_admissao = models.DateField()
    galeria = models.ForeignKey(
        'galerias.Galeria',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='funcionarios',
    )

    class Meta:
        db_table = 'museu_funcionario'
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'

    def gerenciar_exposicao(self, exposicao, novo_status):
        exposicao.status = novo_status
        exposicao.save()

    def cadastrar_obra(self, obra):
        obra.save()

    def gerar_relatorio(self):
        return {
            'funcionario': self.get_full_name() or self.username,
            'cargo': self.cargo,
            'galeria': self.galeria.nome if self.galeria else None,
        }


class Visitante(Usuario):
    data_cadastro = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'museu_visitante'
        verbose_name = 'Visitante'
        verbose_name_plural = 'Visitantes'

    def comprar_ingresso(self, exposicao, tipo, valor):
        from visitacao.models import Ingresso

        return Ingresso.objects.create(
            visitante=self,
            exposicao=exposicao,
            tipo=tipo,
            valor=valor,
        )

    def realizar_reserva(self, exposicao, quantidade_pessoas, data_reserva=None):
        from visitacao.models import Reserva

        if data_reserva is None:
            data_reserva = timezone.now().date()
        return Reserva.objects.create(
            visitante=self,
            exposicao=exposicao,
            data_reserva=data_reserva,
            quantidade_pessoas=quantidade_pessoas,
        )


class Artista(Usuario):
    nacionalidade = models.CharField(max_length=100)
    estilo_artistico = models.CharField(max_length=100)

    class Meta:
        db_table = 'museu_artista'
        verbose_name = 'Artista'
        verbose_name_plural = 'Artistas'

    def cadastrar_artista(self):
        self.save()

    def atualizar_portfolio(self):
        return self.obras_artista.select_related('obra').all()
