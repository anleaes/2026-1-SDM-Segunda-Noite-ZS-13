from rest_framework import serializers

from .models import CategoriaObra


class CategoriaObraSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaObra
        fields = '__all__'
