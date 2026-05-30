from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


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
        'contas.Visitante',
        on_delete=models.CASCADE,
        related_name='ingressos',
    )
    exposicao = models.ForeignKey(
        'exposicoes.Exposicao',
        on_delete=models.CASCADE,
        related_name='ingressos',
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    data_compra = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo')

    class Meta:
        db_table = 'museu_ingresso'
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
        'contas.Visitante',
        on_delete=models.CASCADE,
        related_name='reservas',
    )
    exposicao = models.ForeignKey(
        'exposicoes.Exposicao',
        on_delete=models.CASCADE,
        related_name='reservas',
    )
    data_reserva = models.DateField()
    quantidade_pessoas = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')

    class Meta:
        db_table = 'museu_reserva'
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
        'contas.Visitante',
        on_delete=models.CASCADE,
        related_name='avaliacoes',
    )
    exposicao = models.ForeignKey(
        'exposicoes.Exposicao',
        on_delete=models.CASCADE,
        related_name='avaliacoes',
    )
    nota = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    comentario = models.TextField(blank=True)
    data_avaliacao = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'museu_avaliacao'
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'
        constraints = [
            models.UniqueConstraint(
                fields=['visitante', 'exposicao'],
                name='unique_avaliacao_por_visitante',
            ),
        ]

    def __str__(self):
        return f'Avaliação {self.nota} - {self.exposicao.titulo}'

    def avaliar_exposicao(self):
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
        Ingresso,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='pagamento',
    )
    reserva = models.OneToOneField(
        Reserva,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='pagamento',
    )
    restauracao = models.OneToOneField(
        'obras.Restauracao',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='pagamento',
    )

    class Meta:
        db_table = 'museu_pagamento'
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'

    def clean(self):
        vinculos = [self.ingresso_id, self.reserva_id, self.restauracao_id]
        preenchidos = sum(1 for vinculo in vinculos if vinculo is not None)
        if preenchidos != 1:
            raise ValidationError(
                'Informe exatamente um vínculo: ingresso, reserva ou restauração.'
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def realizar_pagamento(self):
        self.status = 'pago'
        self.save()

    def estornar_pagamento(self):
        self.status = 'estornado'
        self.save()
