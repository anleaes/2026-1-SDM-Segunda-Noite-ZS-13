from django.db import models


class CategoriaObra(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

    class Meta:
        db_table = 'museu_categoriaobra'
        verbose_name = 'Categoria de Obra'
        verbose_name_plural = 'Categorias de Obra'

    def __str__(self):
        return self.nome

    def cadastrar_categoria(self):
        self.save()
