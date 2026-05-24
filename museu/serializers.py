from rest_framework import serializers

from .models import (
    Artista,
    ArtistaObra,
    Avaliacao,
    CategoriaObra,
    CertificadoAutenticidade,
    Exposicao,
    ExposicaoObra,
    Funcionario,
    Galeria,
    Ingresso,
    ObraArte,
    Pagamento,
    Reserva,
    Restauracao,
    Usuario,
    Visitante,
)


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email',
            'data_nascimento', 'telefone', 'cpf',
        ]
        read_only_fields = ['id']


class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = [
            'id', 'username', 'password', 'first_name', 'last_name', 'email',
            'data_nascimento', 'telefone', 'cpf',
            'cargo', 'salario', 'data_admissao', 'galeria',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        senha = validated_data.pop('password')
        funcionario = Funcionario(**validated_data)
        funcionario.set_password(senha)
        funcionario.save()
        return funcionario


class VisitanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitante
        fields = [
            'id', 'username', 'password', 'first_name', 'last_name', 'email',
            'data_nascimento', 'telefone', 'cpf', 'data_cadastro',
        ]
        read_only_fields = ['data_cadastro']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        senha = validated_data.pop('password')
        visitante = Visitante(**validated_data)
        visitante.set_password(senha)
        visitante.save()
        return visitante


class ArtistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artista
        fields = [
            'id', 'username', 'password', 'first_name', 'last_name', 'email',
            'data_nascimento', 'telefone', 'cpf',
            'nacionalidade', 'estilo_artistico',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        senha = validated_data.pop('password')
        artista = Artista(**validated_data)
        artista.set_password(senha)
        artista.save()
        return artista


class GaleriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Galeria
        fields = '__all__'


class CategoriaObraSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaObra
        fields = '__all__'


class ObraArteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObraArte
        fields = '__all__'


class CertificadoAutenticidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CertificadoAutenticidade
        fields = '__all__'


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


class ArtistaObraSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtistaObra
        fields = '__all__'


class RestauracaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restauracao
        fields = '__all__'


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
