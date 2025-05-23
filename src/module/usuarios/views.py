from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Docente, Alumno
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    DocenteSerializer,
    DocenteCreateSerializer,
    AlumnoSerializer,
    AlumnoCreateSerializer,
    LoginSerializer,
    RefreshTokenSerializer
)
from src.utils.jwt_utils import generate_access_token, generate_refresh_token

User = get_user_model()

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['str_email', 'password'],
        properties={
            'str_email': openapi.Schema(type=openapi.TYPE_STRING, format='email', description='Email del usuario'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, format='password', description='Contraseña del usuario'),
        },
    ),
    responses={
        200: openapi.Response(
            description='Login exitoso',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'access_token': openapi.Schema(type=openapi.TYPE_STRING, description='Token JWT de acceso'),
                    'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='Token JWT de refresco'),
                    'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del usuario'),
                    'email': openapi.Schema(type=openapi.TYPE_STRING, format='email', description='Email del usuario'),
                    'is_docente': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Indica si el usuario es un docente'),
                    'is_alumno': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Indica si el usuario es un alumno'),
                    'docente_id': openapi.Schema(type=openapi.TYPE_STRING, description='ID del docente (solo si el usuario es un docente)'),
                    'alumno_id': openapi.Schema(type=openapi.TYPE_STRING, description='ID del alumno (solo si el usuario es un alumno)'),
                },
            ),
        ),
        400: 'Credenciales inválidas',
    },
    operation_description='Endpoint para iniciar sesión y obtener tokens JWT de acceso y refresco',
    operation_summary='Login',
    tags=['Autenticación'],
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']

        # Generar tokens JWT
        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        # Preparar la respuesta básica
        response_data = {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user_id': user.int_idUser,
            'email': user.str_email,
            'is_docente': hasattr(user, 'docente'),
            'is_alumno': hasattr(user, 'alumno')
        }

        # Añadir el ID del docente si el usuario es un docente
        if hasattr(user, 'docente'):
            response_data['docente_id'] = user.docente.str_idDocente

        # Añadir el ID del alumno si el usuario es un alumno
        if hasattr(user, 'alumno'):
            response_data['alumno_id'] = user.alumno.str_idAlumno

        return Response(response_data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

class DocenteViewSet(viewsets.ModelViewSet):
    queryset = Docente.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return DocenteCreateSerializer
        return DocenteSerializer

    def get_queryset(self):
        queryset = Docente.objects.all()
        activo = self.request.query_params.get('activo', None)

        if activo is not None:
            queryset = queryset.filter(bool_activo=activo.lower() == 'true')

        return queryset

class AlumnoViewSet(viewsets.ModelViewSet):
    queryset = Alumno.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return AlumnoCreateSerializer
        return AlumnoSerializer

    def get_queryset(self):
        queryset = Alumno.objects.all()
        activo = self.request.query_params.get('activo', None)

        if activo is not None:
            queryset = queryset.filter(bool_activo=activo.lower() == 'true')

        return queryset

@swagger_auto_schema(
    method='post',
    responses={
        200: openapi.Response(
            description='Logout exitoso',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'detail': openapi.Schema(type=openapi.TYPE_STRING, description='Mensaje de confirmación'),
                },
            ),
        ),
        401: 'No autenticado',
    },
    operation_description='Endpoint para cerrar sesión',
    operation_summary='Logout',
    tags=['Autenticación'],
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    # En JWT no es necesario eliminar tokens del servidor, ya que son stateless
    # El frontend debe eliminar los tokens almacenados
    return Response({'detail': 'Sesión cerrada exitosamente'}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['refresh_token'],
        properties={
            'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='Token JWT de refresco'),
        },
    ),
    responses={
        200: openapi.Response(
            description='Token refrescado exitosamente',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'access_token': openapi.Schema(type=openapi.TYPE_STRING, description='Nuevo token JWT de acceso'),
                },
            ),
        ),
        400: 'Token de refresco inválido o expirado',
    },
    operation_description='Endpoint para refrescar el token JWT de acceso usando un token de refresco',
    operation_summary='Refresh Token',
    tags=['Autenticación'],
)
@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token_view(request):
    serializer = RefreshTokenSerializer(data=request.data)
    if serializer.is_valid():
        access_token = serializer.validated_data['access_token']
        return Response({'access_token': access_token})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
