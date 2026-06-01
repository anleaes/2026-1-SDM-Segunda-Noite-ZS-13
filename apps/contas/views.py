"""Views de autenticação, cadastro e gestão de contas (API REST)."""

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
    """CRUD de usuários base."""

    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username', 'email', 'cpf', 'first_name', 'last_name']
    ordering_fields = ['username', 'email']


class FuncionarioViewSet(viewsets.ModelViewSet):
    """CRUD de funcionários."""

    queryset = Funcionario.objects.select_related('galeria')
    serializer_class = FuncionarioSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['cargo', 'galeria']
    search_fields = ['username', 'first_name', 'last_name', 'cargo']
    ordering_fields = ['username', 'data_admissao', 'salario']


class VisitanteViewSet(viewsets.ModelViewSet):
    """CRUD de visitantes."""

    queryset = Visitante.objects.all()
    serializer_class = VisitanteSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username', 'email', 'cpf', 'first_name', 'last_name']
    ordering_fields = ['username', 'data_cadastro']


class ArtistaViewSet(viewsets.ModelViewSet):
    """CRUD de artistas."""

    queryset = Artista.objects.all()
    serializer_class = ArtistaSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['nacionalidade', 'estilo_artistico']
    search_fields = ['username', 'first_name', 'last_name', 'nacionalidade']
    ordering_fields = ['username', 'nacionalidade']


_PROFILE_MODELS = (Artista, Funcionario, Visitante)


def _detect_role(user):
    if user.is_superuser:
        return 'admin'
    if isinstance(user, Artista):
        return 'artista'
    if isinstance(user, Funcionario):
        return 'funcionario'
    if isinstance(user, Visitante):
        return 'visitante'
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

    if isinstance(user, Visitante):
        payload['data_cadastro'] = user.data_cadastro
    elif isinstance(user, Funcionario):
        payload.update({
            'cargo': user.cargo,
            'salario': str(user.salario),
            'data_admissao': user.data_admissao,
            'galeria': user.galeria_id,
            'galeria_nome': user.galeria.nome if user.galeria else None,
        })
    elif isinstance(user, Artista):
        payload.update({
            'nacionalidade': user.nacionalidade,
            'estilo_artistico': user.estilo_artistico,
        })

    return payload


def _get_user_instance(user_id):
    for model in _PROFILE_MODELS:
        try:
            queryset = model.objects.all()
            if model is Funcionario:
                queryset = queryset.select_related('galeria')
            return queryset.get(pk=user_id)
        except model.DoesNotExist:
            continue
    try:
        return Usuario.objects.get(pk=user_id)
    except Usuario.DoesNotExist:
        return None


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    """Autenticação por username e senha."""

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

        if isinstance(user, Funcionario):
            user = Funcionario.objects.select_related('galeria').get(pk=user.pk)

        return Response(_user_payload(user))


@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    """Cadastro de novo visitante."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterVisitanteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        visitante = serializer.save()
        return Response(_user_payload(visitante), status=status.HTTP_201_CREATED)


@method_decorator(csrf_exempt, name='dispatch')
class AccountView(APIView):
    """Consulta, atualização e exclusão de conta por ID."""

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
    """Alteração de senha com validação da senha atual."""

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
