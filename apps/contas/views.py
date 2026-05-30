from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Artista, Funcionario, Usuario, Visitante
from .serializers import (
    AccountUpdateSerializer,
    ArtistaSerializer,
    ChangePasswordSerializer,
    FuncionarioSerializer,
    RegisterVisitanteSerializer,
    UsuarioSerializer,
    VisitanteSerializer,
)


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username', 'email', 'cpf', 'first_name', 'last_name']
    ordering_fields = ['username', 'email']


class FuncionarioViewSet(viewsets.ModelViewSet):
    queryset = Funcionario.objects.select_related('galeria')
    serializer_class = FuncionarioSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['cargo', 'galeria']
    search_fields = ['username', 'first_name', 'last_name', 'cargo']
    ordering_fields = ['username', 'data_admissao', 'salario']


class VisitanteViewSet(viewsets.ModelViewSet):
    queryset = Visitante.objects.all()
    serializer_class = VisitanteSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username', 'email', 'cpf', 'first_name', 'last_name']
    ordering_fields = ['username', 'data_cadastro']


class ArtistaViewSet(viewsets.ModelViewSet):
    queryset = Artista.objects.all()
    serializer_class = ArtistaSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['nacionalidade', 'estilo_artistico']
    search_fields = ['username', 'first_name', 'last_name', 'nacionalidade']
    ordering_fields = ['username', 'nacionalidade']


def _detect_role(user):
    if Artista.objects.filter(pk=user.pk).exists():
        return 'artista'
    if Funcionario.objects.filter(pk=user.pk).exists():
        return 'funcionario'
    if Visitante.objects.filter(pk=user.pk).exists():
        return 'visitante'
    if user.is_superuser:
        return 'admin'
    return 'usuario'


def _user_payload(user):
    role = _detect_role(user)
    payload = {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'cpf': user.cpf,
        'telefone': user.telefone,
        'data_nascimento': user.data_nascimento,
        'role': role,
    }

    if role == 'visitante':
        visitante = Visitante.objects.filter(pk=user.pk).first()
        if visitante:
            payload['data_cadastro'] = visitante.data_cadastro
    elif role == 'funcionario':
        funcionario = Funcionario.objects.filter(pk=user.pk).select_related('galeria').first()
        if funcionario:
            payload.update({
                'cargo': funcionario.cargo,
                'salario': str(funcionario.salario),
                'data_admissao': funcionario.data_admissao,
                'galeria': funcionario.galeria_id,
                'galeria_nome': funcionario.galeria.nome if funcionario.galeria else None,
            })
    elif role == 'artista':
        artista = Artista.objects.filter(pk=user.pk).first()
        if artista:
            payload.update({
                'nacionalidade': artista.nacionalidade,
                'estilo_artistico': artista.estilo_artistico,
            })

    return payload


def _get_user_instance(user_id):
    try:
        return Usuario.objects.get(pk=user_id)
    except Usuario.DoesNotExist:
        return None


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '')

        if not username or not password:
            return Response(
                {'detail': 'Informe usuario e senha.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(username=username, password=password)
        if user is None:
            return Response(
                {'detail': 'Usuario ou senha invalidos.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response(_user_payload(user))


@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterVisitanteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        visitante = serializer.save()
        return Response(_user_payload(visitante), status=status.HTTP_201_CREATED)


@method_decorator(csrf_exempt, name='dispatch')
class AccountView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        user = _get_user_instance(pk)
        if user is None:
            return Response({'detail': 'Conta nao encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(_user_payload(user))

    def patch(self, request, pk):
        user = _get_user_instance(pk)
        if user is None:
            return Response({'detail': 'Conta nao encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AccountUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = serializer.update(user, serializer.validated_data)
        return Response(_user_payload(user))

    def delete(self, request, pk):
        user = _get_user_instance(pk)
        if user is None:
            return Response({'detail': 'Conta nao encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        if not isinstance(user, Visitante):
            return Response(
                {'detail': 'Somente contas de visitante podem ser excluidas pela API.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@method_decorator(csrf_exempt, name='dispatch')
class ChangePasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, pk):
        user = _get_user_instance(pk)
        if user is None:
            return Response({'detail': 'Conta nao encontrada.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not user.check_password(serializer.validated_data['current_password']):
            return Response(
                {'detail': 'Senha atual incorreta.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'detail': 'Senha alterada com sucesso.'})
