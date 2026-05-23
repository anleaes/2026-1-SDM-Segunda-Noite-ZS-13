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
