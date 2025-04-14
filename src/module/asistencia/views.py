import uuid
import base64
from io import BytesIO

from django.utils import timezone
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

try:
    import qrcode
    from qrcode.image.pure import PymagingImage
    QRCODE_AVAILABLE = True
except ImportError:
    QRCODE_AVAILABLE = False

from .models import Asistencia, CodigoQR
from src.module.usuarios.models import Alumno, Docente
from src.module.inscripciones.models import AlumnoSeccion
from src.module.academico.models import SesionClase
from .serializers import (
    AsistenciaSerializer,
    AsistenciaDetalleSerializer,
    CodigoQRSerializer,
    CodigoQRCreateSerializer,
    CodigoQRDetalleSerializer,
    VerificarCodigoQRSerializer
)

class AsistenciaViewSet(viewsets.ModelViewSet):
    queryset = Asistencia.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AsistenciaDetalleSerializer
        return AsistenciaSerializer

    def get_queryset(self):
        queryset = Asistencia.objects.all()
        alumno_seccion_id = self.request.query_params.get('alumno_seccion_id', None)
        sesion_clase_id = self.request.query_params.get('sesion_clase_id', None)
        fecha = self.request.query_params.get('fecha', None)
        estado = self.request.query_params.get('estado', None)

        if alumno_seccion_id is not None:
            queryset = queryset.filter(int_idAlumnoSeccion=alumno_seccion_id)
        if sesion_clase_id is not None:
            queryset = queryset.filter(int_idSesionClase=sesion_clase_id)
        if fecha is not None:
            queryset = queryset.filter(dt_fecha=fecha)
        if estado is not None:
            queryset = queryset.filter(str_estado=estado)

        return queryset


class CodigoQRViewSet(viewsets.ModelViewSet):
    queryset = CodigoQR.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return CodigoQRCreateSerializer
        elif self.action == 'retrieve':
            return CodigoQRDetalleSerializer
        return CodigoQRSerializer

    def get_queryset(self):
        queryset = CodigoQR.objects.all()
        sesion_clase_id = self.request.query_params.get('sesion_clase_id', None)
        docente_id = self.request.query_params.get('docente_id', None)
        activo = self.request.query_params.get('activo', None)

        if sesion_clase_id is not None:
            queryset = queryset.filter(int_idSesionClase=sesion_clase_id)
        if docente_id is not None:
            queryset = queryset.filter(str_idDocente=docente_id)
        if activo is not None:
            queryset = queryset.filter(bool_activo=activo.lower() == 'true')

        return queryset

    @swagger_auto_schema(
        request_body=CodigoQRCreateSerializer,
        responses={
            201: openapi.Response('Código QR creado exitosamente', CodigoQRSerializer),
            400: 'Datos inválidos',
        },
        operation_description='Crea un nuevo código QR para una sesión de clase',
        operation_summary='Crear código QR',
    )
    def create(self, request, *args, **kwargs):
        # Desactivar códigos QR anteriores para la misma sesión
        sesion_clase_id = request.data.get('int_idSesionClase')
        if sesion_clase_id:
            CodigoQR.objects.filter(
                int_idSesionClase=sesion_clase_id,
                bool_activo=True
            ).update(bool_activo=False)

        # Crear el nuevo código QR
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(
        method='post',
        request_body=VerificarCodigoQRSerializer,
        responses={
            200: openapi.Response('Asistencia registrada exitosamente', AsistenciaSerializer),
            400: 'Datos inválidos o código QR expirado',
            404: 'Código QR no encontrado',
        },
        operation_description='Verifica un código QR y registra la asistencia del alumno',
        operation_summary='Verificar código QR y registrar asistencia',
    )
    @action(detail=False, methods=['post'], url_path='verificar')
    def verificar_codigo_qr(self, request):
        serializer = VerificarCodigoQRSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        str_codigo = serializer.validated_data['str_codigo']
        str_idAlumno = serializer.validated_data['str_idAlumno']

        # Buscar el código QR
        try:
            codigo_qr = CodigoQR.objects.get(str_codigo=str_codigo, bool_activo=True)
        except CodigoQR.DoesNotExist:
            return Response({'error': 'Código QR no encontrado o inactivo'}, status=status.HTTP_404_NOT_FOUND)

        # Verificar si el código QR es válido
        if not codigo_qr.is_valid():
            return Response({'error': 'Código QR expirado'}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener la sesión de clase
        sesion_clase = codigo_qr.int_idSesionClase

        # Buscar al alumno
        try:
            alumno = Alumno.objects.get(str_idAlumno=str_idAlumno)
        except Alumno.DoesNotExist:
            return Response({'error': 'Alumno no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        # Buscar la inscripción del alumno en la sección
        try:
            seccion = sesion_clase.int_idHorario.int_idDocenteSeccion.int_idSeccion
            alumno_seccion = AlumnoSeccion.objects.get(
                str_idAlumno=alumno,
                int_idSeccion=seccion,
                bool_activo=True
            )
        except AlumnoSeccion.DoesNotExist:
            return Response(
                {'error': 'El alumno no está inscrito en esta sección'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verificar si ya existe una asistencia para este alumno en esta sesión
        asistencia_existente = Asistencia.objects.filter(
            int_idSesionClase=sesion_clase,
            int_idAlumnoSeccion=alumno_seccion,
            str_tipo='A'
        ).first()

        with transaction.atomic():
            if asistencia_existente:
                # Actualizar la asistencia existente
                asistencia_existente.str_estado = 'P'  # Presente
                asistencia_existente.dt_hora_registro = timezone.now().time()
                asistencia_existente.save()
                asistencia = asistencia_existente
            else:
                # Crear una nueva asistencia
                asistencia = Asistencia.objects.create(
                    int_idSesionClase=sesion_clase,
                    int_idAlumnoSeccion=alumno_seccion,
                    str_tipo='A',  # Alumno
                    dt_fecha=timezone.now().date(),
                    str_estado='P',  # Presente
                )

            # Actualizar el estado de la sesión de clase si aún no está marcada como realizada
            if sesion_clase.str_estado == 'P':  # Pendiente
                sesion_clase.str_estado = 'R'  # Realizada
                sesion_clase.save()

        # Devolver la asistencia creada/actualizada
        return Response(AsistenciaSerializer(asistencia).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        method='post',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['int_idSesionClase', 'str_idDocente'],
            properties={
                'int_idSesionClase': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la sesión de clase'),
                'str_idDocente': openapi.Schema(type=openapi.TYPE_STRING, description='ID del docente'),
                'formato': openapi.Schema(type=openapi.TYPE_STRING, enum=['base64', 'png'], description='Formato de retorno del código QR'),
            },
        ),
        responses={
            200: openapi.Response('Código QR generado exitosamente',
                                 openapi.Schema(type=openapi.TYPE_OBJECT,
                                              properties={
                                                  'codigo': openapi.Schema(type=openapi.TYPE_STRING),
                                                  'qr_code': openapi.Schema(type=openapi.TYPE_STRING),
                                                  'expiracion': openapi.Schema(type=openapi.TYPE_STRING, format='date-time'),
                                              })),
            400: 'Datos inválidos o biblioteca qrcode no disponible',
        },
        operation_description='Genera un nuevo código QR para una sesión de clase con validez de 30 segundos',
        operation_summary='Generar código QR',
    )
    @action(detail=False, methods=['post'], url_path='generar')
    def generar_codigo_qr(self, request):
        # Verificar si la biblioteca qrcode está disponible
        if not QRCODE_AVAILABLE:
            return Response(
                {'error': 'La biblioteca qrcode no está instalada en el servidor'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validar datos de entrada
        int_idSesionClase = request.data.get('int_idSesionClase')
        str_idDocente = request.data.get('str_idDocente')
        formato = request.data.get('formato', 'base64')  # Por defecto, devolver como base64
        # Ignoramos el parámetro minutos_validez ya que siempre será de 30 segundos

        if not int_idSesionClase or not str_idDocente:
            return Response(
                {'error': 'Se requieren los campos int_idSesionClase y str_idDocente'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verificar que la sesión de clase y el docente existan
        try:
            sesion_clase = SesionClase.objects.get(int_idSesionClase=int_idSesionClase)
            docente = Docente.objects.get(str_idDocente=str_idDocente)
        except (SesionClase.DoesNotExist, Docente.DoesNotExist):
            return Response(
                {'error': 'Sesión de clase o docente no encontrados'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Desactivar códigos QR anteriores para la misma sesión
        CodigoQR.objects.filter(
            int_idSesionClase=sesion_clase,
            bool_activo=True
        ).update(bool_activo=False)

        # Generar un código único
        str_codigo = str(uuid.uuid4())

        # Establecer fecha de expiración fija de 30 segundos
        dt_fecha_expiracion = timezone.now() + timezone.timedelta(seconds=30)

        # Crear el nuevo código QR en la base de datos
        codigo_qr = CodigoQR.objects.create(
            int_idSesionClase=sesion_clase,
            str_idDocente=docente,
            str_codigo=str_codigo,
            dt_fecha_expiracion=dt_fecha_expiracion,
            bool_activo=True
        )

        # Generar la imagen del código QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(str_codigo)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Devolver la respuesta según el formato solicitado
        if formato == 'png':
            return HttpResponse(buffer.getvalue(), content_type="image/png")
        else:  # base64
            img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
            return Response({
                'codigo': str_codigo,
                'qr_code': f'data:image/png;base64,{img_str}',
                'expiracion': dt_fecha_expiracion.isoformat() if dt_fecha_expiracion else None,
            }, status=status.HTTP_200_OK)
