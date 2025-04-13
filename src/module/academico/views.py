from rest_framework import viewsets
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

class CalendarioViewSet(viewsets.ModelViewSet):
    queryset = Calendario.objects.all()
    serializer_class = CalendarioSerializer

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

class SyllabusViewSet(viewsets.ModelViewSet):
    queryset = Syllabus.objects.all()
    serializer_class = SyllabusSerializer

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

    def get_queryset(self):
        queryset = Horario.objects.all()
        docente_seccion_id = self.request.query_params.get('docente_seccion_id', None)

        if docente_seccion_id is not None:
            queryset = queryset.filter(docente_seccion_id=docente_seccion_id)

        return queryset

class SesionClaseViewSet(viewsets.ModelViewSet):
    queryset = SesionClase.objects.all()
    serializer_class = SesionClaseSerializer

    def get_queryset(self):
        queryset = SesionClase.objects.all()
        horario_id = self.request.query_params.get('horario_id', None)
        ciclo_id = self.request.query_params.get('ciclo_id', None)
        fecha = self.request.query_params.get('fecha', None)
        estado = self.request.query_params.get('estado', None)

        if horario_id is not None:
            queryset = queryset.filter(horario_id=horario_id)
        if ciclo_id is not None:
            queryset = queryset.filter(ciclo_academico_id=ciclo_id)
        if fecha is not None:
            queryset = queryset.filter(dt_fecha=fecha)
        if estado is not None:
            queryset = queryset.filter(str_estado=estado)

        return queryset
