from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import AlumnoSeccion, DocenteSeccion
from .serializers import (
    AlumnoSeccionSerializer,
    AlumnoSeccionDetalleSerializer,
    DocenteSeccionSerializer,
    DocenteSeccionDetalleSerializer,
    DocenteCursoSerializer
)
from src.module.usuarios.permissions import IsDocenteOrAlumno

class AlumnoSeccionViewSet(viewsets.ModelViewSet):
    queryset = AlumnoSeccion.objects.all()
    permission_classes = [IsDocenteOrAlumno]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return AlumnoSeccionDetalleSerializer
        return AlumnoSeccionSerializer

    def get_queryset(self):
        queryset = AlumnoSeccion.objects.all()
        alumno_id = self.request.query_params.get('alumno_id', None)
        seccion_id = self.request.query_params.get('seccion_id', None)
        activo = self.request.query_params.get('activo', None)

        if alumno_id is not None:
            queryset = queryset.filter(str_idAlumno=alumno_id)
        if seccion_id is not None:
            queryset = queryset.filter(int_idSeccion=seccion_id)
        if activo is not None:
            queryset = queryset.filter(bool_activo=activo.lower() == 'true')

        return queryset

class DocenteSeccionViewSet(viewsets.ModelViewSet):
    queryset = DocenteSeccion.objects.all()
    permission_classes = [IsDocenteOrAlumno]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DocenteSeccionDetalleSerializer
        elif self.action == 'cursos_docente':
            return DocenteCursoSerializer
        return DocenteSeccionSerializer

    def get_queryset(self):
        queryset = DocenteSeccion.objects.all()
        docente_id = self.request.query_params.get('docente_id', None)
        seccion_id = self.request.query_params.get('seccion_id', None)
        tipo = self.request.query_params.get('tipo', None)
        activo = self.request.query_params.get('activo', None)

        if docente_id is not None:
            queryset = queryset.filter(str_idDocente=docente_id)
        if seccion_id is not None:
            queryset = queryset.filter(int_idSeccion=seccion_id)
        if tipo is not None:
            queryset = queryset.filter(str_tipo=tipo)
        if activo is not None:
            queryset = queryset.filter(bool_activo=activo.lower() == 'true')

        return queryset

    @action(detail=False, methods=['get'], url_path='cursos-docente/(?P<docente_id>[^/.]+)')
    def cursos_docente(self, request, docente_id=None):
        """
        Endpoint para obtener los cursos asignados a un docente con información detallada.
        """
        if not docente_id:
            return Response(
                {"error": "Se requiere el ID del docente"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Filtrar las asignaciones del docente
        queryset = DocenteSeccion.objects.filter(
            str_idDocente=docente_id,
            bool_activo=True
        ).select_related(
            'int_idSeccion',
            'int_idSeccion__str_idCurso',
            'str_idCicloAcademico'
        )

        # Serializar los resultados
        serializer = DocenteCursoSerializer(queryset, many=True)

        return Response(serializer.data)
