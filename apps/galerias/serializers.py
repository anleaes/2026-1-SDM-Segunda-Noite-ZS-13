from rest_framework import serializers

from .models import Galeria


class GaleriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Galeria
        fields = '__all__'
