from rest_framework import serializers

from .models import Exposicao, ExposicaoObra


class ExposicaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exposicao
        fields = '__all__'

    def validate(self, attrs):
        data_inicio = attrs.get('data_inicio', getattr(self.instance, 'data_inicio', None))
        data_fim = attrs.get('data_fim', getattr(self.instance, 'data_fim', None))
        if data_inicio and data_fim and data_fim < data_inicio:
            raise serializers.ValidationError(
                'A data fim deve ser igual ou posterior à data início.'
            )
        return attrs


class ExposicaoObraSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExposicaoObra
        fields = '__all__'
