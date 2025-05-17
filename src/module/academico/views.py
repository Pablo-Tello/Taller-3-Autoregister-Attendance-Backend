from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from src.module.usuarios.permissions import IsDocenteOrAlumno

from .models import CicloAcademico, Calendario, Curso, Syllabus, Seccion, SesionClase, Horario
from .serializers import (
    CicloAcademicoSerializer,
    CalendarioSerializer,
    CursoSerializer,
    SyllabusSerializer,
    SeccionSerializer,
    SeccionDetalleSerializer,
    SesionClaseSerializer,
    HorarioSerializer
)

class CicloAcademicoViewSet(viewsets.ModelViewSet):
    queryset = CicloAcademico.objects.all()
    serializer_class = CicloAcademicoSerializer
    permission_classes = [IsDocenteOrAlumno]

class CalendarioViewSet(viewsets.ModelViewSet):
    queryset = Calendario.objects.all()
    serializer_class = CalendarioSerializer
    permission_classes = [IsDocenteOrAlumno]

    def get_queryset(self):
        queryset = Calendario.objects.all()
        fecha = self.request.query_params.get('fecha', None)
        tipo_dia = self.request.query_params.get('tipo_dia', None)
        laborable = self.request.query_params.get('laborable', None)

        if fecha is not None:
            queryset = queryset.filter(dt_fecha=fecha)
        if tipo_dia is not None:
            queryset = queryset.filter(str_tipo_dia=tipo_dia)
        if laborable is not None:
            queryset = queryset.filter(bool_laborable=laborable.lower() == 'true')
        return queryset

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    permission_classes = [IsDocenteOrAlumno]

class SyllabusViewSet(viewsets.ModelViewSet):
    queryset = Syllabus.objects.all()
    serializer_class = SyllabusSerializer
    permission_classes = [IsDocenteOrAlumno]

    def get_queryset(self):
        queryset = Syllabus.objects.all()
        curso_id = self.request.query_params.get('curso_id', None)
        ciclo_id = self.request.query_params.get('ciclo_id', None)

        if curso_id is not None:
            queryset = queryset.filter(curso_id=curso_id)
        if ciclo_id is not None:
            queryset = queryset.filter(ciclo_academico_id=ciclo_id)

        return queryset

class SeccionViewSet(viewsets.ModelViewSet):
    queryset = Seccion.objects.all()
    permission_classes = [IsDocenteOrAlumno]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SeccionDetalleSerializer
        return SeccionSerializer

    def get_queryset(self):
        queryset = Seccion.objects.all()
        curso_id = self.request.query_params.get('curso_id', None)
        ciclo_id = self.request.query_params.get('ciclo_id', None)

        if curso_id is not None:
            queryset = queryset.filter(curso_id=curso_id)
        if ciclo_id is not None:
            queryset = queryset.filter(ciclo_academico_id=ciclo_id)

        return queryset

class HorarioViewSet(viewsets.ModelViewSet):
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer
    permission_classes = [IsDocenteOrAlumno]

    def get_queryset(self):
        queryset = Horario.objects.all()
        docente_seccion_id = self.request.query_params.get('docente_seccion_id', None)

        if docente_seccion_id is not None:
            queryset = queryset.filter(docente_seccion_id=docente_seccion_id)

        return queryset

class SesionClaseViewSet(viewsets.ModelViewSet):
    queryset = SesionClase.objects.all()
    serializer_class = SesionClaseSerializer
    permission_classes = [IsDocenteOrAlumno]
    # pagination_class = None  # Desactivar paginación para este ViewSet

    def get_queryset(self):
        queryset = SesionClase.objects.all()
        horario_id = self.request.query_params.get('horario_id', None)
        ciclo_id = self.request.query_params.get('ciclo_id', None)
        fecha = self.request.query_params.get('fecha', None)
        estado = self.request.query_params.get('estado', None)

        if horario_id is not None:
            queryset = queryset.filter(int_idHorario=horario_id)
        if ciclo_id is not None:
            queryset = queryset.filter(str_idCicloAcademico=ciclo_id)
        if fecha is not None:
            queryset = queryset.filter(dt_fecha=fecha)
        if estado is not None:
            queryset = queryset.filter(str_estado=estado)

        return queryset

    @action(detail=False, methods=['get'], url_path='seccion/(?P<seccion_id>[^/.]+)')
    def sesiones_por_seccion(self, request, seccion_id=None):
        """
        Endpoint para obtener las sesiones de clase de una sección específica.
        """
        if not seccion_id:
            return Response(
                {"error": "Se requiere el ID de la sección"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Filtrar sesiones por sección
        queryset = SesionClase.objects.filter(
            int_idHorario__int_idDocenteSeccion__int_idSeccion=seccion_id
        )

        # Serializar los resultados
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['dt_fecha', 'int_idHorario', 'str_idCicloAcademico'],
            properties={
                'dt_fecha': openapi.Schema(type=openapi.TYPE_STRING, format='date', description='Fecha de la sesión'),
                'str_estado': openapi.Schema(type=openapi.TYPE_STRING, description='Estado de la sesión (P: Pendiente, R: Realizada, C: Cancelada)', default='P'),
                'str_tema': openapi.Schema(type=openapi.TYPE_STRING, description='Tema de la sesión'),
                'str_observacion': openapi.Schema(type=openapi.TYPE_STRING, description='Observaciones'),
                'bool_activo': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Indica si la sesión está activa', default=True),
                'int_idHorario': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del horario'),
                'str_idCicloAcademico': openapi.Schema(type=openapi.TYPE_STRING, description='ID del ciclo académico'),
                # int_idCalendario se determina automáticamente a partir de dt_fecha
            },
        ),
        operation_description='Crea una nueva sesión de clase. El campo int_idCalendario se determina automáticamente a partir de dt_fecha.',
        operation_summary='Crear sesión de clase',
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
