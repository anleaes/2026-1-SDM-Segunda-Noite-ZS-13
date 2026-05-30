from rest_framework import serializers

from .models import Artista, Funcionario, Usuario, Visitante


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email',
            'data_nascimento', 'telefone', 'cpf',
        ]
        read_only_fields = ['id']


class RegisterVisitanteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = Visitante
        fields = [
            'username', 'password', 'password_confirm', 'email',
            'first_name', 'last_name', 'cpf', 'telefone', 'data_nascimento',
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password_confirm'):
            raise serializers.ValidationError({'password_confirm': 'As senhas nao conferem.'})
        return attrs

    def create(self, validated_data):
        senha = validated_data.pop('password')
        visitante = Visitante(**validated_data)
        visitante.set_password(senha)
        visitante.save()
        return visitante


class AccountUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False, max_length=150)
    last_name = serializers.CharField(required=False, max_length=150)
    email = serializers.EmailField(required=False)
    telefone = serializers.CharField(required=False, max_length=20, allow_blank=True)
    data_nascimento = serializers.DateField(required=False, allow_null=True)
    nacionalidade = serializers.CharField(required=False, max_length=100, allow_blank=True)
    estilo_artistico = serializers.CharField(required=False, max_length=100, allow_blank=True)

    def update(self, user, validated_data):
        role = None
        if Artista.objects.filter(pk=user.pk).exists():
            role = 'artista'
            profile = Artista.objects.get(pk=user.pk)
        elif Funcionario.objects.filter(pk=user.pk).exists():
            profile = user
        elif Visitante.objects.filter(pk=user.pk).exists():
            profile = user
        else:
            profile = user

        for field in ('first_name', 'last_name', 'email', 'telefone', 'data_nascimento'):
            if field in validated_data:
                setattr(profile, field, validated_data[field])

        if role == 'artista':
            for field in ('nacionalidade', 'estilo_artistico'):
                if field in validated_data:
                    setattr(profile, field, validated_data[field])

        profile.save()
        return profile


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=6)
    new_password_confirm = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError(
                {'new_password_confirm': 'As senhas nao conferem.'},
            )
        return attrs


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
