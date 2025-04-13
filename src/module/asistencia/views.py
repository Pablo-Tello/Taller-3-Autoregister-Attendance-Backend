from rest_framework import viewsets
from .models import Asistencia
from .serializers import AsistenciaSerializer, AsistenciaDetalleSerializer

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
