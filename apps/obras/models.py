"""Models do acervo: obras, certificados, participação de artistas e restaurações."""

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class ObraArte(models.Model):
    """Obra de arte pertencente a uma categoria do acervo."""
    titulo = models.CharField(max_length=200)
    tecnica = models.CharField(max_length=100)
    ano_criacao = models.PositiveIntegerField()
    valor_estimado = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    categoria = models.ForeignKey(
        'categorias.CategoriaObra',
        on_delete=models.PROTECT,
        related_name='obras',
    )

    class Meta:
        db_table = 'museu_obraarte'
        verbose_name = 'Obra de Arte'
        verbose_name_plural = 'Obras de Arte'
        ordering = ['titulo']

    def __str__(self):
        return self.titulo

    def restaurar(self, funcionario, descricao, custo):
        """Registra uma nova restauração vinculada a esta obra."""
        return Restauracao.objects.create(
            obra=self,
            funcionario=funcionario,
            descricao=descricao,
            custo=custo,
        )

    def calcular_valor(self):
        """Retorna o valor estimado atual da obra."""
        return self.valor_estimado


class CertificadoAutenticidade(models.Model):
    """Certificado de autenticidade associado a uma única obra."""
    obra = models.OneToOneField(
        ObraArte,
        on_delete=models.CASCADE,
        related_name='certificado',
    )
    codigo = models.CharField(max_length=50, unique=True)
    data_emissao = models.DateField()
    orgao_responsavel = models.CharField(max_length=200)

    class Meta:
        db_table = 'museu_certificadoautenticidade'
        verbose_name = 'Certificado de Autenticidade'
        verbose_name_plural = 'Certificados de Autenticidade'

    def __str__(self):
        return self.codigo

    def validar_certificado(self):
        """Indica se código e data de emissão estão preenchidos."""
        return bool(self.codigo and self.data_emissao)


class ArtistaObra(models.Model):
    """Associação N:N entre artista e obra, com função e data."""
    artista = models.ForeignKey(
        'contas.Artista',
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
        db_table = 'museu_artistaobra'
        verbose_name = 'Participação do Artista'
        verbose_name_plural = 'Participações dos Artistas'
        unique_together = ('artista', 'obra')

    def __str__(self):
        return f'{self.artista.username} - {self.obra.titulo}'


class Restauracao(models.Model):
    """Processo de restauração de uma obra, conduzido por um funcionário."""

    obra = models.ForeignKey(
        ObraArte,
        on_delete=models.CASCADE,
        related_name='restauracoes',
    )
    funcionario = models.ForeignKey(
        'contas.Funcionario',
        on_delete=models.PROTECT,
        related_name='restauracoes',
    )
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    descricao = models.TextField()
    custo = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'museu_restauracao'
        verbose_name = 'Restauração'
        verbose_name_plural = 'Restaurações'

    def __str__(self):
        return f'Restauração de {self.obra.titulo}'

    def iniciar_restauracao(self):
        """Define a data de início como a data atual."""
        self.data_inicio = timezone.now().date()
        self.save()

    def finalizar_restauracao(self, data_fim):
        """Registra a data de conclusão da restauração."""
        self.data_fim = data_fim
        self.save()
