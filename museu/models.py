from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Usuario(AbstractUser):
    """Classe base do diagrama. Login e senha vêm do AbstractUser do Django."""

    data_nascimento = models.DateField(null=True, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    cpf = models.CharField(max_length=14, unique=True)

    class Meta:
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
        'Galeria',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='funcionarios',
    )

    class Meta:
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
        verbose_name = 'Visitante'
        verbose_name_plural = 'Visitantes'

    def comprar_ingresso(self, exposicao, tipo, valor):
        return Ingresso.objects.create(
            visitante=self,
            exposicao=exposicao,
            tipo=tipo,
            valor=valor,
        )

    def realizar_reserva(self, exposicao, quantidade_pessoas):
        return Reserva.objects.create(
            visitante=self,
            exposicao=exposicao,
            quantidade_pessoas=quantidade_pessoas,
        )


class Artista(Usuario):
    nacionalidade = models.CharField(max_length=100)
    estilo_artistico = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Artista'
        verbose_name_plural = 'Artistas'

    def cadastrar_artista(self):
        self.save()

    def atualizar_portfolio(self):
        return self.obras_artista.select_related('obra').all()


class Galeria(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    endereco = models.CharField(max_length=300)
    aberta = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Galeria'
        verbose_name_plural = 'Galerias'

    def __str__(self):
        return self.nome

    def abrir_galeria(self):
        self.aberta = True
        self.save()

    def fechar_galeria(self):
        self.aberta = False
        self.save()


class CategoriaObra(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Categoria de Obra'
        verbose_name_plural = 'Categorias de Obra'

    def __str__(self):
        return self.nome

    def cadastrar_categoria(self):
        self.save()


class ObraArte(models.Model):
    titulo = models.CharField(max_length=200)
    tecnica = models.CharField(max_length=100)
    ano_criacao = models.PositiveIntegerField()
    valor_estimado = models.DecimalField(max_digits=12, decimal_places=2)
    categoria = models.ForeignKey(
        CategoriaObra,
        on_delete=models.PROTECT,
        related_name='obras',
    )

    class Meta:
        verbose_name = 'Obra de Arte'
        verbose_name_plural = 'Obras de Arte'

    def __str__(self):
        return self.titulo

    def restaurar(self, funcionario, descricao, custo):
        return Restauracao.objects.create(
            obra=self,
            funcionario=funcionario,
            descricao=descricao,
            custo=custo,
        )

    def calcular_valor(self):
        return self.valor_estimado


class CertificadoAutenticidade(models.Model):
    obra = models.OneToOneField(
        ObraArte,
        on_delete=models.CASCADE,
        related_name='certificado',
    )
    codigo = models.CharField(max_length=50, unique=True)
    data_emissao = models.DateField()
    orgao_responsavel = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Certificado de Autenticidade'
        verbose_name_plural = 'Certificados de Autenticidade'

    def __str__(self):
        return self.codigo

    def validar_certificado(self):
        return bool(self.codigo and self.data_emissao)


class Exposicao(models.Model):
    STATUS_CHOICES = [
        ('planejada', 'Planejada'),
        ('em_andamento', 'Em andamento'),
        ('encerrada', 'Encerrada'),
    ]

    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planejada')
    galeria = models.ForeignKey(
        Galeria,
        on_delete=models.CASCADE,
        related_name='exposicoes',
    )

    class Meta:
        verbose_name = 'Exposição'
        verbose_name_plural = 'Exposições'

    def __str__(self):
        return self.titulo

    def iniciar_exposicao(self):
        self.status = 'em_andamento'
        self.save()

    def encerrar_exposicao(self):
        self.status = 'encerrada'
        self.save()


class ExposicaoObra(models.Model):
    """Classe associativa entre Exposição e Obra de Arte."""

    exposicao = models.ForeignKey(
        Exposicao,
        on_delete=models.CASCADE,
        related_name='obras_exposicao',
    )
    obra = models.ForeignKey(
        ObraArte,
        on_delete=models.CASCADE,
        related_name='exposicoes_obra',
    )
    data_entrada = models.DateField()
    posicao_sala = models.CharField(max_length=100)
    iluminacao_especial = models.CharField(max_length=100, blank=True)
    status_conservacao = models.CharField(max_length=100)
    estilo_obra = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = 'Obra na Exposição'
        verbose_name_plural = 'Obras na Exposição'
        unique_together = ('exposicao', 'obra')

    def __str__(self):
        return f'{self.obra.titulo} em {self.exposicao.titulo}'


class ArtistaObra(models.Model):
    """Classe associativa entre Artista e Obra de Arte."""

    artista = models.ForeignKey(
        Artista,
        on_delete=models.CASCADE,
        related_name='obras_artista',
    )
    obra = models.ForeignKey(
        ObraArte,
        on_delete=models.CASCADE,
        related_name='artistas_obra',
    )
    funcao = models.CharField(max_length=100)
    data_participacao = models.DateField()

    class Meta:
        verbose_name = 'Participação do Artista'
        verbose_name_plural = 'Participações dos Artistas'
        unique_together = ('artista', 'obra')

    def __str__(self):
        return f'{self.artista.username} - {self.obra.titulo}'


class Restauracao(models.Model):
    obra = models.ForeignKey(
        ObraArte,
        on_delete=models.CASCADE,
        related_name='restauracoes',
    )
    funcionario = models.ForeignKey(
        Funcionario,
        on_delete=models.PROTECT,
        related_name='restauracoes',
    )
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    descricao = models.TextField()
    custo = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Restauração'
        verbose_name_plural = 'Restaurações'

    def __str__(self):
        return f'Restauração de {self.obra.titulo}'

    def iniciar_restauracao(self):
                self.data_inicio = timezone.now().date()
        self.save()

    def finalizar_restauracao(self, data_fim):
        self.data_fim = data_fim
        self.save()


class Pagamento(models.Model):
    METODO_CHOICES = [
        ('pix', 'PIX'),
        ('cartao', 'Cartão'),
        ('dinheiro', 'Dinheiro'),
    ]
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('estornado', 'Estornado'),
    ]

    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_pagamento = models.DateTimeField(auto_now_add=True)
    metodo = models.CharField(max_length=20, choices=METODO_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    ingresso = models.OneToOneField(
        'Ingresso',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='pagamento',
    )
    reserva = models.OneToOneField(
        'Reserva',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='pagamento',
    )
    restauracao = models.OneToOneField(
        Restauracao,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='pagamento',
    )

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'

    def realizar_pagamento(self):
        self.status = 'pago'
        self.save()

    def estornar_pagamento(self):
        self.status = 'estornado'
        self.save()


class Ingresso(models.Model):
    TIPO_CHOICES = [
        ('inteira', 'Inteira'),
        ('meia', 'Meia'),
        ('cortesia', 'Cortesia'),
    ]
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('utilizado', 'Utilizado'),
        ('cancelado', 'Cancelado'),
    ]

    visitante = models.ForeignKey(
        Visitante,
        on_delete=models.CASCADE,
        related_name='ingressos',
    )
    exposicao = models.ForeignKey(
        Exposicao,
        on_delete=models.CASCADE,
        related_name='ingressos',
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    data_compra = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo')

    class Meta:
        verbose_name = 'Ingresso'
        verbose_name_plural = 'Ingressos'

    def __str__(self):
        return f'Ingresso {self.id} - {self.exposicao.titulo}'

    def gerar_ingresso(self):
        self.status = 'ativo'
        self.save()


class Reserva(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    ]

    visitante = models.ForeignKey(
        Visitante,
        on_delete=models.CASCADE,
        related_name='reservas',
    )
    exposicao = models.ForeignKey(
        Exposicao,
        on_delete=models.CASCADE,
        related_name='reservas',
    )
    data_reserva = models.DateField()
    quantidade_pessoas = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def __str__(self):
        return f'Reserva {self.id} - {self.exposicao.titulo}'

    def confirmar_reserva(self):
        self.status = 'confirmada'
        self.save()

    def cancelar_reserva(self):
        self.status = 'cancelada'
        self.save()


class Avaliacao(models.Model):
    visitante = models.ForeignKey(
        Visitante,
        on_delete=models.CASCADE,
        related_name='avaliacoes',
    )
    exposicao = models.ForeignKey(
        Exposicao,
        on_delete=models.CASCADE,
        related_name='avaliacoes',
    )
    nota = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    comentario = models.TextField(blank=True)
    data_avaliacao = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'

    def __str__(self):
        return f'Avaliação {self.nota} - {self.exposicao.titulo}'

    def avaliar_exposicao(self):
        self.save()
