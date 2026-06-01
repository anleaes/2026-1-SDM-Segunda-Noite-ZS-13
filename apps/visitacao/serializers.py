from rest_framework import serializers

from .models import Avaliacao, Ingresso, Pagamento, Reserva


def _nome_visitante(visitante):
    return visitante.get_full_name() or visitante.username


class IngressoSerializer(serializers.ModelSerializer):
    visitante_nome = serializers.SerializerMethodField()
    exposicao_titulo = serializers.CharField(source='exposicao.titulo', read_only=True)

    class Meta:
        model = Ingresso
        fields = '__all__'

    def get_visitante_nome(self, obj):
        return _nome_visitante(obj.visitante)


class ReservaSerializer(serializers.ModelSerializer):
    visitante_nome = serializers.SerializerMethodField()
    exposicao_titulo = serializers.CharField(source='exposicao.titulo', read_only=True)

    class Meta:
        model = Reserva
        fields = '__all__'

    def get_visitante_nome(self, obj):
        return _nome_visitante(obj.visitante)


class AvaliacaoSerializer(serializers.ModelSerializer):
    visitante_nome = serializers.SerializerMethodField()
    exposicao_titulo = serializers.CharField(source='exposicao.titulo', read_only=True)

    class Meta:
        model = Avaliacao
        fields = '__all__'

    def validate_nota(self, valor):
        if valor < 1 or valor > 5:
            raise serializers.ValidationError('A nota deve estar entre 1 e 5.')
        return valor

    def get_visitante_nome(self, obj):
        return _nome_visitante(obj.visitante)


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
                'Informe exatamente um vínculo: ingresso, reserva ou restauração.',
            )
        return attrs
