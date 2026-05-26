from rest_framework import serializers

from .models import Avaliacao, Ingresso, Pagamento, Reserva


class IngressoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingresso
        fields = '__all__'


class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'


class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = '__all__'

    def validate_nota(self, valor):
        if valor < 1 or valor > 5:
            raise serializers.ValidationError('A nota deve estar entre 1 e 5.')
        return valor


class PagamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pagamento
        fields = '__all__'

    def validate(self, attrs):
        ingresso = attrs.get('ingresso')
        reserva = attrs.get('reserva')
        restauracao = attrs.get('restauracao')

        if self.instance:
            if 'ingresso' not in attrs:
                ingresso = self.instance.ingresso
            if 'reserva' not in attrs:
                reserva = self.instance.reserva
            if 'restauracao' not in attrs:
                restauracao = self.instance.restauracao

        vinculos = [ingresso, reserva, restauracao]
        preenchidos = sum(1 for vinculo in vinculos if vinculo is not None)
        if preenchidos != 1:
            raise serializers.ValidationError(
                'Informe exatamente um vínculo: ingresso, reserva ou restauração.'
            )
        return attrs
