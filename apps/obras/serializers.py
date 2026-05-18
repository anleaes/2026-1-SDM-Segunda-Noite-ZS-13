from rest_framework import serializers

from .models import (
    ArtistaObra,
    CertificadoAutenticidade,
    ObraArte,
    Restauracao,
)


class ObraArteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObraArte
        fields = '__all__'


class CertificadoAutenticidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificadoAutenticidade
        fields = '__all__'


class ArtistaObraSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistaObra
        fields = '__all__'


class RestauracaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restauracao
        fields = '__all__'
