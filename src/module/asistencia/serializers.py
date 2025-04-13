from rest_framework import serializers
from .models import Asistencia
from src.module.inscripciones.serializers import AlumnoSeccionSerializer
from src.module.academico.serializers import SesionClaseSerializer

class AsistenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asistencia
        fields = '__all__'

class AsistenciaDetalleSerializer(serializers.ModelSerializer):
    alumno_seccion = AlumnoSeccionSerializer(read_only=True)
    sesion_clase = SesionClaseSerializer(read_only=True)
    
    class Meta:
        model = Asistencia
        fields = '__all__'
