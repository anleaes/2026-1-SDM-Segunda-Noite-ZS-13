from django.utils import timezone
from rest_framework import serializers

from .models import (
    ArtistaObra,
    CertificadoAutenticidade,
    ObraArte,
    Restauracao,
)


class ObraArteSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)

    class Meta:
        model = ObraArte
        fields = '__all__'

    def validate_ano_criacao(self, value):
        ano_atual = timezone.now().year
        if value > ano_atual:
            raise serializers.ValidationError(
                'O ano de criacao nao pode ser maior que o ano atual.',
            )
        return value


class CertificadoAutenticidadeSerializer(serializers.ModelSerializer):
    obra_titulo = serializers.CharField(source='obra.titulo', read_only=True)

    class Meta:
        model = CertificadoAutenticidade
        fields = '__all__'


class ArtistaObraSerializer(serializers.ModelSerializer):
    artista_nome = serializers.CharField(source='artista.username', read_only=True)
    obra_titulo = serializers.CharField(source='obra.titulo', read_only=True)

    class Meta:
        model = ArtistaObra
        fields = '__all__'


class RestauracaoSerializer(serializers.ModelSerializer):
    obra_titulo = serializers.CharField(source='obra.titulo', read_only=True)
    funcionario_nome = serializers.CharField(source='funcionario.username', read_only=True)

    class Meta:
        model = Restauracao
        fields = '__all__'
