from django.db import models


class Galeria(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    endereco = models.CharField(max_length=300)
    aberta = models.BooleanField(default=True)

    class Meta:
        db_table = 'museu_galeria'
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
