from django.core.exceptions import ValidationError
from django.db import models


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
        'galerias.Galeria',
        on_delete=models.CASCADE,
        related_name='exposicoes',
    )

    class Meta:
        db_table = 'museu_exposicao'
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

    def clean(self):
        if self.data_fim and self.data_inicio and self.data_fim < self.data_inicio:
            raise ValidationError('A data fim deve ser igual ou posterior à data início.')


class ExposicaoObra(models.Model):
    exposicao = models.ForeignKey(
        Exposicao,
        on_delete=models.CASCADE,
        related_name='obras_exposicao',
    )
    obra = models.ForeignKey(
        'obras.ObraArte',
        on_delete=models.CASCADE,
        related_name='exposicoes_obra',
    )
    data_entrada = models.DateField()
    posicao_sala = models.CharField(max_length=100)
    iluminacao_especial = models.CharField(max_length=100, blank=True)
    status_conservacao = models.CharField(max_length=100)
    estilo_obra = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'museu_exposicaoobra'
        verbose_name = 'Obra na Exposição'
        verbose_name_plural = 'Obras na Exposição'
        unique_together = ('exposicao', 'obra')

    def __str__(self):
        return f'{self.obra.titulo} em {self.exposicao.titulo}'
